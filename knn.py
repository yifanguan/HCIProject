import csv
import numpy as np
import sklearn
from sklearn.neighbors import KNeighborsRegressor

inputfile="whole_stats.csv"
injury_database = csv.reader(open(inputfile,'r'))


next(injury_database)
X=[]
Y=[]
clt=KNeighborsRegressor(n_neighbors=3)

for line in injury_database:
    i1=line.index("##")
    i2=line.index('&&')
    before=[float(i) for i in line[i1+2:i2-1]]
    after=[float(i) for i in line[i2+2:-1]]
    X.append(before)
    Y.append(after)

X_test=X[int(0.9*len(X)):]
Y_test=Y[int(0.9*len(Y)):]
X=X[0:int(0.9*len(X))]
Y=Y[0:int(0.9*len(Y))]
clt.fit(X,Y)
result=clt.predict(X_test)

right=0
for i in range(len(result)):
    flag=False
    for j in range(len(result[i])):
        if j!=1:
            if abs(result[i][j]-Y_test[i][j])>2:
                flag=True
                break
    if flag==False:
        right+=1
print(right/len(Y))