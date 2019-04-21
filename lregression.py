import csv
import numpy as np
import sklearn
import torch
from torch import nn
import torch.optim
import torch.nn.modules.activation as act
class LinearRegressionModel(nn.Module):

    def __init__(self, input_dim, output_dim):

        super(LinearRegressionModel, self).__init__()
        # Calling Super Class's constructor
        self.linear = nn.Linear(input_dim, 100)
        self.relu=act.ReLU()
        self.linear2=nn.Linear(100,output_dim)
        # nn.linear is defined in nn.Module

    def forward(self, x):
        # Here the forward pass is simply a linear function

        out = self.linear(x)
        out=self.relu(out)
        out=self.linear2(out)
        return out

input_dim = 23
output_dim = 23

inputfile="whole_stats.csv"
injury_database = csv.reader(open(inputfile,'r'))
title=next(injury_database)
X=[]
Y=[]
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
title=title[i1+2:i2-1]

model=LinearRegressionModel(input_dim,output_dim)
criterion=nn.MSELoss()
optimizer=torch.optim.SGD(model.parameters(),lr=0.01)

X=torch.tensor(X)
Y=torch.tensor(Y)
X_test=torch.tensor(X_test)
Y_test=torch.tensor(Y_test)
best=0
for epoch in range(500):
    optimizer.zero_grad()
    outputs=model.forward(X)
    loss=criterion(outputs,Y)
    loss.backward()
    optimizer.step()

    result=model(X_test)
    right=0
acc=[]
for j in range(len(result[0])):
    right = 0
    for i in range(len(result)):
        if abs(result[i][j] - Y_test[i][j]) <5 :
            if j == 2:
                print(result[i][j].data, Y_test[i][j].data)
            right += 1
    acc.append(right / len(Y_test))
    print(title[j], right / len(Y_test))