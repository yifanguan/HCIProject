import csv
import numpy as np
import sklearn
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
inputfile="whole_stats.csv"
injury_database = csv.reader(open(inputfile,'r'))


title=next(injury_database)
X=[]
Y=[]
best=0
bestk=-1
humanbody=['ligament', 'hand', 'footheel', 'knee', 'nose', 'rib', 'orbital', 'tooth', 'pulmonary', 'facial', 'knee',
           'Acchilles', 'muscle', 'handthumb', 'calf', 'atrial', 'heart', 'handfinger', 'back', 'arm', 'neck', 'ankle',
           'lung', 'thigh', 'leg', 'tibia', 'elbow', 'tonsils', 'appendectomy', 'jaw', 'shoulder', 'groin', 'hamstring',
           'hip', 'tendon', 'appendix', 'bicep', 'hernia', 'head', 'wrist', 'concussion', 'finger', 'foot', 'spinal', 'shin',
           'quadricep', 'kneecap', 'rotator', 'eye', 'chest', 'testicle', 'quadricep', 'face', 'abdomen', 'toe',
           'heel', 'fibula', 'Achilles', 'thumb', 'cheekbone','air pocket']

causes=['sprained', 'sore', 'strained', 'broken','blood clot','surgery','fracture','torn','injury','bruise','dislocate',
        'hyperextended','rupture','tendinitis','scar','herniated disc','damage','nerve','separated','bursitis','plantar fasci','stress reaction',
        'spasm','swelling','subluxation','enlarged']
for line in injury_database:
    i1 = line.index("##")
    i2 = line.index('&&')
    before = [float(i) for i in line[i1 + 2:i2 - 1]]
    before.append(humanbody.index(line[4].split('/')[0]))
    if line[5]!='':
        before.append(causes.index(line[5].split('/')[0]))
    else:
        before.append(-1)

    after = [float(i) for i in line[i2 + 2:-1]]
    X.append(before)
    Y.append(after)

title=title[i1+2:i2-1]

X_test = X[int(0.9 * len(X)):]
Y_test = Y[int(0.9 * len(Y)):]
X = X[0:int(0.9 * len(X))]
Y = Y[0:int(0.9 * len(Y))]
best=0
for _ in range(100):
    dt=DecisionTreeRegressor()

    dt.fit(X,Y)
    result=dt.predict(X_test)

    acc=[]
    for j in range(len(result[0])):
        right=0
        for i in range(len(result)):
            if abs(result[i][j]-Y_test[i][j])<5:
                # if j==2:
                    # print(result[i][j],Y_test[i][j])
                right+=1
        acc.append(right/len(Y_test))
        if j==2 and acc[2]>best:
            best=acc[2]
print(best)


