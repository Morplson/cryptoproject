loader_size = 3200
sample_length = 1000
taining_epochs = 9 
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


test_inout_seq = inout_seq[-test_size:]
random.shuffle(test_inout_seq)






#### TESTING

model = WeekNet()
model.load_state_dict(torch.load("D:\\xampp\\htdocs\\node\\cryptoproject\\models\\2020-06-12_52979a40801072d329c0454fc80c92a5.pt"))


model.eval()

for seq, rLable, title in test_inout_seq:

    with torch.no_grad():
        model.hidden = (
            torch.zeros(1, 1, model.hidden_layer_size),
            torch.zeros(1, 1, model.hidden_layer_size)
        )
        gLable = model(seq).item()


        pyplot.title(title)
        pyplot.ylabel('MONEY')
        pyplot.grid(True)
        pyplot.autoscale(axis='x', tight=True)
        pyplot.plot(seq)

        x = np.linspace(sample_length, sample_length+5*24)
        real = rLable * (x-sample_length)/24 + seq[-1].item()
        guess = gLable * (x-sample_length)/24 + seq[-1].item()

        pyplot.plot(x,real)
        pyplot.plot(x,guess)
        
        pyplot.legend(['GRAPH', 'Real', 'Guess'], loc=4)
        pyplot.show()