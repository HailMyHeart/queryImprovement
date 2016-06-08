from pprint import *
import copy

from collections import defaultdict
def tree(): return defaultdict(tree)
def dicts(t):
    d = {}
    for k in t.keys():
        d[k] = dicts(t[k])
    return d
def add(t, keys):
    for key in keys:
        t = t[key]
sqlTree = tree()
relationDict = {'employee':set(['ename', 'essn' ,'salary', 'bdate', 'dno']), 'department':set(['dname', 'dno']), 'works_on':set(['essn', 'pno']), 'project':set(['pno', 'pname'])}
sqlStoreList = []
sqlStr = 'projection [ ename ] ( select [ salary < 3000 ] ( employee join select [ pno = "p1" ] ( works_on join project ) ) )'
#sqlStr = 'select [ ename = "mary" & dname = "research" ] ( employee join department )'
#sqlStr = 'select [ essn = "01" ] ( projection [ essn , pname ] ( works_on join project ) )'
#sqlStr = 'projection [ bdate ] ( select [ ename = "john" & dname = "research" ] ( employee join department ) )'
sqlList = sqlStr.split()
lastToken = ' '
for i in sqlStr.split():
    if i == ')':
        break
    elif  i!='(' and i!='join':

        if lastToken == ' ':

            sqlStoreList.append([i])

        elif lastToken == '(':
            sqlStoreList[-1].append(i)

        elif lastToken == 'join':
            new = copy.deepcopy(sqlStoreList[-1])
            new.pop()
            new.append(i)
            sqlStoreList.append(new)
        else:
            sqlStoreList[-1][-1]+=i
    elif i == 'join':
        cur = sqlStoreList[-1].pop()
        sqlStoreList[-1]+=['join', cur]
    lastToken = i
for i in sqlStoreList:
    add(sqlTree, i)
relationList = []
mutualAttr = set([])
for i in sqlStoreList:
    if 'join' in i:
        i.reverse()
        curIndex = -(i.index('join'))
        i.reverse()
        relationList.append(i[curIndex+len(i)])
for i in range(len(relationList)-1):
    for j in range(i+1, len(relationList)):
        mutualAttr = mutualAttr.union(relationDict[relationList[i]] & relationDict[relationList[j]])
for i in range(len(sqlStoreList)):
    haveProjection = False
    if 'join' in sqlStoreList[i]:
        sqlStoreList[i].reverse()
        curIndex = -(sqlStoreList[i].index('join'))
        sqlStoreList[i].reverse()
        curR = sqlStoreList[i][curIndex+len(sqlStoreList[i])]
        curset = relationDict[curR]
        curProjSet = curset&mutualAttr
        curSqlList = copy.deepcopy(sqlStoreList[i])
        for j in sqlStoreList[i]:
            if 'projection' in j and curIndex+len(curSqlList)>curSqlList.index(j):
                haveProjection = True
                for k in curset:
                    if k in j:
                        curProjSet.add(k)

            elif 'select' in j and curIndex+len(curSqlList)>curSqlList.index(j):
                curSqlList.remove(j)
                curSelectList = j[7:-1].split('&')
                select = ''

                for k in curSelectList:
                    token = ''
                    if '=' in k:
                        token = '='
                    elif '<' in k:
                        token = '<'
                    if k.split(token)[0] in curset:
                        if select == '':
                            select += k
                        else:
                            select += ('&'+k)
                        if haveProjection:
                            curProjSet.add(k.split(token)[0])
                if select!='':
                    curSqlList.insert(len(curSqlList)+curIndex, 'select['+select+']')

        if haveProjection:
            curSqlList.insert(len(curSqlList)+curIndex, 'projection['+','.join(curProjSet)+']')
        sqlStoreList[i] = curSqlList

improveSqlTree = tree()
for i in sqlStoreList:
    add(improveSqlTree, i)
pprint(dicts(sqlTree))
pprint(dicts(improveSqlTree))

