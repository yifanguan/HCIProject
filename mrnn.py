import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
import torch.optim as optim
import time
import numpy as np
import csv
import pickle

class PerformancePredictionRNN(nn.Module):

    def __init__(self, feature_dim, hiddeen_dim, batch_size):
        super(PerformancePredictionRNN, self).__init__()
        self.feature_dim = feature_dim
        self.hidden_dim = hiddeen_dim
        self.batch_size = batch_size

        self.rnn = nn.RNN(input_size=feature_dim, hidden_size=hiddeen_dim, batch_first=True)
        self.linear = nn.Linear(hiddeen_dim, feature_dim)
        # TODO: might need more linear layers

    def forward(self, features): # features: batch_size * month sequence * performance metrics
        outputs, _ = self.rnn(features)
        sequence_lengths = (features != -1).int()[:,:,0].sum(dim=1) # size: batch_size
        batch_hidden_states = torch.zeros(self.batch_size, self.hidden_dim)
        for i in range(self.batch_size):
            batch_hidden_states[i] = outputs[i][sequence_lengths[i] - 1]        
        logits = self.linear(batch_hidden_states)
        return logits

class PerformancePredictionMRNN(nn.Module):

    def __init__(self, checkpoint=None, feature_dim=11, batch_size=100):
        super(PerformancePredictionMRNN, self).__init__()
        self.feature_dim = feature_dim
        self.batch_size = batch_size

        self.rnn = PerformancePredictionRNN(feature_dim=feature_dim, hiddeen_dim=100, batch_size=batch_size)
        self.rnn.load_state_dict(checkpoint['state_dict'])
        for param in self.rnn.parameters():
            param.requires_grad = False

        hidden_dim1 = 40
        hidden_dim2 = 50
        self.linear1 = nn.Linear(feature_dim, feature_dim)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(hidden_dim1, hidden_dim2)
        self.linear3 = nn.Linear(hidden_dim2, feature_dim)

    def forward(self, features): # features: batch_size * month sequence * performance metrics
        rnn_out = self.rnn(features)
        relu1 = self.relu(rnn_out)
        linear1_out = self.linear1(relu1)
        # relu2 = self.relu(linear1_out)
        # linear2_out = self.linear2(relu2)
        # relu3 = self.relu(linear2_out)
        # linear3_out = self.linear3(relu3)
        return linear1_out

def train(trainloader, devloader, net, criterion, optimizer, device, feature_dim):
    for epoch in range(200):
        start = time.time()
        running_loss = 0.0
        for i, (features, labels) in enumerate(trainloader):
            features = features.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = net(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            # print statistics
            running_loss += loss.item()
            if i % 100 == 99:
                end = time.time()
                print('[epoch %d, iter %5d] loss: %.3f eplased time %.3f' %
                      (epoch + 1, i + 1, running_loss / 100, end-start))
                start = time.time()
                running_loss = 0.0
        print('Epoch %d Dev set Accuracy:' % (epoch + 1))
        test(devloader, net, device, feature_dim)
    print('Finished Training')

def test(dataloader, net, device, feature_dim):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in dataloader:
            features, labels = data
            features = features.to(device)
            labels = labels.to(device)
            # classifier.init_hidden()
            outputs = net(features)
            total += labels.size(0)
            # print((torch.abs(outputs - labels) < 2))
            correct += ((torch.abs(outputs - labels) < 2).int()[:,0] == torch.ones(50).int()).int().sum().item()
    print('Accuracy of the classifier on specified dataset is: ' + str(100 * correct / total) + '%')

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # preprocess data for features and labels
    checkpoint = torch.load('./rnn.epoch=80.checkpoint.pth.tar')
    filename = 'rnn_data_pickle_train_examples'
    infile = open(filename,'rb')
    train_features = pickle.load(infile).float()
    infile.close()
    csv_file = csv.reader(open("whole_stats.csv",'r')) 
    next(csv_file)       
    features = []
    labels = []
    for line in csv_file:
        feature = [line[11:30]]
        for i in range(7):
            feature.append([-1] * 19)
        features.append(feature)
        labels.append(line[37:56])
    features = np.array(features).astype(np.float)
    features = torch.from_numpy(features).float()
    labels = np.array(labels).astype(np.float)
    labels = torch.from_numpy(labels).float()
    #################################################################################################
    #################################################################################################
    trainset = torch.utils.data.TensorDataset(features[:450], labels[:450])
    devset = torch.utils.data.TensorDataset(features[470:520], labels[470:520])
    # testset = torch.utils.data.TensorDataset(test_features, test_labels)
    batch_size = 50
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)
    devloader = torch.utils.data.DataLoader(devset, batch_size=50,
                                         shuffle=False)
    # testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         # shuffle=False)
    # train 
    net = PerformancePredictionMRNN(checkpoint=checkpoint, feature_dim=train_features.size()[2], batch_size=batch_size).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.0005)

    train(trainloader, devloader, net, criterion, optimizer, device, feature_dim=train_features.size()[2])
    # print('Test set Accuracy:')
    # test(testloader, classifier, device)

if __name__== "__main__":
    main()
