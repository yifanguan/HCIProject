# pretrain our rnn model
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import torch.optim as optim
import time
import numpy as np
import pickle
import os

def save_checkpoint(model, epoch, checkpoint_dir='./'):
    state = {
        'epoch': epoch,
        'state_dict': model.state_dict(),
    }

    filename = os.path.join(checkpoint_dir, 'rnn.epoch={}.checkpoint.pth.tar'.format(epoch))
    torch.save(state, filename)

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

def train(trainloader, devloader, net, criterion, optimizer, device, feature_dim):
    for epoch in range(80):
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
        save_checkpoint(net, epoch, checkpoint_dir='./')
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
            correct += ((torch.abs(outputs - labels) < 2).int().sum(dim=1) == feature_dim).int().sum().item()
    print('Accuracy of the classifier on specified dataset is: ' + str(100 * correct / total) + '%')

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # preprocess data for features and labels
    filename = 'rnn_data_pickle_train_examples'
    infile = open(filename,'rb')
    train_features = pickle.load(infile).float()
    infile.close()
    filename = 'rnn_data_pickle_labels'
    infile = open(filename,'rb')
    train_labels = pickle.load(infile).float()
    infile.close()
    #################################################################################################
    #################################################################################################
    trainset = torch.utils.data.TensorDataset(train_features, train_labels)
    devset = torch.utils.data.TensorDataset(train_features, train_labels)
    # testset = torch.utils.data.TensorDataset(test_features, test_labels)
    batch_size = 10
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)
    devloader = torch.utils.data.DataLoader(devset, batch_size=batch_size,
                                         shuffle=False)
    # testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
    #                                      shuffle=False)
    # train 
    feature_dim = train_features.size()[2]
    net = PerformancePredictionRNN(feature_dim=feature_dim, hiddeen_dim=100, batch_size=batch_size).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    train(trainloader, devloader, net, criterion, optimizer, device, feature_dim)
    # print('Test set Accuracy:')
    # test(testloader, classifier, device)

if __name__== "__main__":
    main()
