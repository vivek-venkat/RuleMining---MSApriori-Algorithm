'''
Implementation of the MS-Apriori Algorithm
@authors: Vivek Venkataraman
'''

import itertools
#Global Objects
phi = 0.0
misDict = dict() # Stores the MIS Values for each Item
itemList = list()  # Stores individual Items 
itemCountDict = dict() # Stores the Count of each Item occurrence
posMisDict = dict() # Stores the position of the items after sorting by MIS
transactionCount=0 # The total count of all Items in the transactions
initPassList=list() # This Denotes L. The initial list that is passed to the 
fList = list([] for _ in range(7)) # List of Frequent Item Sets
transactionList = list() # This is the list of transactions
cList = list([] for _ in range(7)) # List of Candidate Item Sets
cItemDict = dict() # Holds the count for the occurrence of each Item Set 
#subset=list() # Holds the subsets of k-1 while computing the k-itemset candidates

def main():
    readData()
    doInitPass()
    findFi1()
    findOtherFi()
    print('CList:',cList)
    print('FList:',fList)
    genOutPut()
    print('Finished.')
        
def findFi1():
    global fList
    if(not fList[1]):
        for i in range(len(initPassList)):
            if((itemCountDict.get(initPassList[i])/transactionCount)>=misDict.get(initPassList[i])):
                fList[1].append(initPassList[i]) 
#    print('F1: ',fList[1])
    return ''
    
def doInitPass():
    global initPassList
    for i in range(len(itemList)):
        if(i==0):initPassList.append(itemList[0])
        else:
            if((itemCountDict.get(itemList[i])/transactionCount)>=misDict.get(itemList[0])):
                initPassList.append(itemList[i])
    print('L:',initPassList)
    for i in range(len(initPassList)):
        posMisDict[initPassList[i]]=i            
    return ''
           
def readData():
    global misDict,itemList,itemCountDict,transactionCount,phi,transactionList
    '''Find the PHI Value and Populate the MIS Values in Dictionary''' 
    f1 = open('para-1.txt')
    for line in f1:
        if(line.find('SDC')!=-1):phi = float(line.replace(' ','').rstrip().split('=')[1])
        if(line.find('MIS')!=-1):
            misTemp = line.replace(' ','').replace('MIS','').replace('(','').replace(')','').rstrip().split('=')
            misDict[int(misTemp[0])] = float(misTemp[1])
    items = sorted(misDict, key=misDict.__getitem__)
    for i in items:
        itemList.append(int(i))
        itemCountDict[int(i)]=0
    print('M:',itemList)
    '''Populate Transactions List '''
    f2 = open('data-1.txt')
    for line in f2:
        transactionList.append(list())
        transString = line.replace(' ','').split(',')
        for t in transString : 
            transactionList[len(transactionList)-1].append(int(t))
            if(itemCountDict.get(int(t))!=None):
                itemCountDict[int(t)]=itemCountDict.get(int(t))+1
#    print('Transaction List: ',transactionList)
    transactionCount = len(transactionList)
    return ''

def level2CandidateGen():
    global cList
    for i in range (0,len(initPassList)):
        if (itemCountDict[initPassList[i]]/transactionCount) >= misDict[initPassList[i]]:
            for j in range (i+1, len(initPassList)):
                if (itemCountDict[initPassList[j]]/transactionCount) >= misDict[initPassList[i]] and abs(itemCountDict[initPassList[j]]/transactionCount-itemCountDict[initPassList[i]]/transactionCount) <= phi:
                    cList[2].append(list())
                    cList[2][len(cList[2])-1].append(initPassList[i])
                    cList[2][len(cList[2])-1].append(initPassList[j])
#    print('C 2 :',cList[2])
    return ''

def msCandidateGen(m):
    global cList,itemCountDict,misDict
    k=0
    for i in range(0, len(fList[m])):
        for j in range(0, len(fList[m])):
            while k < m-1 and fList[m][i][k] == fList[m][j][k]:
                k+=1
            if k == m-1:
                if posMisDict[fList[m][i][k]] < posMisDict[fList[m][j][k]] and abs(itemCountDict[fList[m][i][k]]/transactionCount - itemCountDict[fList[m][j][k]]/transactionCount) <= phi:
                    cList[m+1].append(list(fList[m][i]))
                    cList[m+1][len(cList[m+1])-1].append(fList[m][j][k])
                    subset=list(itertools.combinations(cList[m+1][len(cList[m+1])-1],m))
                    for s in range(0,len(subset)):
                        if(not cList[m+1]):
                            if (bool(cList[m+1][len(cList[m+1])-1][0]) in subset[s]) or (misDict[cList[m+1][len(cList[m+1])-1][1]] == misDict[cList[m+1][len(cList[m+1])-1][0]]):
                                if bool(subset[s]) not in fList[m]:
                                    del cList[m+1][len(cList[m+1])-1]
            k=0
#    print('C',m+1,':',cList[m+1])
    return ''
    
def findOtherFi():
    global fList,cItemDict
    k=2
    while(True):
        if(not fList[k-1]):
            break
        if(k==2):
            level2CandidateGen()
        else:
            msCandidateGen(k-1)
        for t in transactionList:
            for c in cList[k]:
                if(set(c).issubset(set(t))):
                    if(cItemDict.get(tuple(c))==None):cItemDict[tuple(c)] = 1
                    else:cItemDict[tuple(c)]=cItemDict.get(tuple(c))+1
        for c in cList[k]:
            if(cItemDict.get(tuple(c))!=None):
                if(cItemDict.get(tuple(c))/transactionCount >= misDict[c[0]]):
                    fList[k].append(c[:])
#        print('F',k,':',fList[k])
        k+=1
    return ''

def genOutPut():
    f = open('results-1.txt','w')
    f.write('Results\n')
    for i in range(len(fList)-1,-1,-1):
        if(fList[i]):
            f.write('\nNo. of length '+str(i)+' frequent itemsets: '+str(len(fList[i]))+'\n\n')
            for j in fList[i]:
                if(i==1):
                    f.write('{'+str(j)+'} : support-count = '+str(itemCountDict.get(int(j)))+'\n')  
                else:   
                    f.write('{'+str(j)+'} : support-count = '+str(cItemDict.get(tuple(j)))+'\n')
    f.close()
    return ''


if __name__ == "__main__": main()

