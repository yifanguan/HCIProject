import pickle
import torch
import csv
import numpy as np
import torch

csv_file = csv.reader(open("dirty.csv",'r'))
csv_file2 = csv.reader(open("new_data.csv",'r'))

injuried_players = set()
for line in csv_file2:
    injuried_players.add(line[3])

max_length = 8 # Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun
prev_number = '11'
current_number = '11'
train_examples = [] # all train examples in dataset.
labels = [] # last month day
train_example = [] # months of data. this is a unit to our RNN model. same number index.
month_data = [] # one row in dataset. 
next(csv_file)
for line in csv_file:
    if line[1] not in injuried_players: # we only need healthy players to train our RNN model
        current_number = line[0]
        if current_number != prev_number:
            labels.append(train_example[-1])
            length = len(train_example)
            train_example[-1] = [-1] * 19
            for i in range(max_length - length):
                train_example.append([-1] * 19)
            train_examples.append(train_example)
            train_example = []
            prev_number = current_number
        month_data = line[7:26] # pts -- fp
        train_example.append(month_data)

train_examples = np.array(train_examples).astype(np.float)
train_examples = torch.from_numpy(train_examples)
labels = np.array(labels).astype(np.float)
labels = torch.from_numpy(labels)
filename = 'rnn_data_pickle_train_examples'
outfile = open(filename,'wb')
pickle.dump(train_examples, outfile)
outfile.close()
filename = 'rnn_data_pickle_labels'
outfile = open(filename,'wb')
pickle.dump(labels, outfile)
outfile.close()