loader_size = 3200
sample_length = 1000
taining_epochs = 6
test_size = 50



####GET DATA
import pymongo #yDGTNy2WK52Bqsm


client = pymongo.MongoClient("mongodb+srv://lol:yDGTNy2WK52Bqsm@cluster0-gijx9.mongodb.net/bcdata?retryWrites=true&w=majority")
#db = client.test

db = client["bcdata"]

dlong = db["60d"]
dshort = db["kd"]

print("fetching")
x_train_raw = dlong.find().limit(loader_size) #.sort([("date",-1)])
y_train_raw = dshort.find().limit(loader_size)
print("done\n\n")

####PLOT AND RESHAPE
from matplotlib import pyplot
import numpy as np
import datetime
import random
import hashlib

from sklearn.preprocessing import MinMaxScaler

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from models import WeekNet



print(torch.cuda.is_available())

scaler = MinMaxScaler(feature_range=(-1, 1))
x_train = []
y_train = []
d_names = []

for i in range(loader_size):

    if len(x_train_raw[i]["values"])>=sample_length:
        #
        # 
        # print(x_train_raw[i]["scrape_id"])
        d_names.append(x_train_raw[i]["scrape_id"])

        x_train.append(x_train_raw[i]["values"][-sample_length:])   
        y_train.append([y_train_raw[i]["values"]["k"]])



print(str(len(x_train[0]))+":"+str(len(x_train)))
print(str(len(y_train[0]))+":"+str(len(y_train)))

x_train_tensor = torch.FloatTensor(x_train)
y_train_tensor = torch.FloatTensor(y_train)


def create_inout_sequences(data, prediction, id):
    inout_seq = []
    dLen = len(data)
    pLen = len(prediction)
    for i in range(min(dLen,pLen)):
        train_seq = data[i]
        train_label = prediction[i]
        train_id = d_names[i] 
        inout_seq.append((train_seq ,train_label, train_id))
    return inout_seq

inout_seq = create_inout_sequences(x_train_tensor, y_train_tensor, d_names)

train_inout_seq = inout_seq[:-test_size]
random.shuffle(train_inout_seq)













model = WeekNet()
loss_function = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


print("start training")


for i in range(taining_epochs):
    for seq, labels, name in train_inout_seq:
        optimizer.zero_grad()
        model.hidden_cell = (
            torch.zeros(1, 1, model.hidden_layer_size),
            torch.zeros(1, 1, model.hidden_layer_size)
        )

        y_pred = model(seq)

        single_loss = loss_function(y_pred, labels)
        single_loss.backward()
        optimizer.step()

        print(f'epoch: {i:3} loss: {single_loss.item():10.8f} {name}')

print(f'epoch: {i:3} loss: {single_loss.item():10.12f}')

print('Finished Training')

#### Save State


enc = str(random.randrange(0,10000000000000))
hash = hashlib.md5(enc.encode('ascii','ignore')).hexdigest()


date_str = datetime.datetime.now().date()
torch.save(model.state_dict(), "D:\\xampp\\htdocs\\node\\cryptoproject\\models\\"+str(date_str)+"_"+str(hash)+".pt")
