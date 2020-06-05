loader_size = 50



####GET DATA
import pymongo #yDGTNy2WK52Bqsm


client = pymongo.MongoClient("mongodb+srv://lol:yDGTNy2WK52Bqsm@cluster0-gijx9.mongodb.net/bcdata?retryWrites=true&w=majority")
#db = client.test

db = client["bcdata"]

dlong = db["60d"]
dshort = db["kd"]

print("fetching")
x_train_raw = dlong.find().sort([("date",-1)]).limit(loader_size)
y_train_raw = dshort.find().sort([("date",-1)]).limit(loader_size)
print("done\n\n")

####PLOT AND RESHAPE
from matplotlib import pyplot
import numpy as np

x_train = []
y_train = []

for i in range(loader_size):

    if len(x_train_raw[i]["values"])>=1000:
        print(x_train_raw[i]["scrape_id"])
        
        x_train.append(x_train_raw[i]["values"][-1000:])   
        
        y_train.append([
            y_train_raw[i]["values"]["k"],
            y_train_raw[i]["values"]["d"]
        ])

print(str(len(x_train[0]))+":"+str(len(x_train)))


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


from torch.utils.tensorboard import SummaryWriter

tensor_x = torch.Tensor(x_train) # transform to torch tensor
tensor_y = torch.Tensor(y_train)

#tensor_x = tensor_x.unsqueeze(0).unsqueeze(0)
print(tensor_x.shape)
#tensor_y = tensor_y.unsqueeze(0).unsqueeze(0)
print(tensor_y.shape)

dataset = torch.utils.data.TensorDataset(tensor_x,tensor_y) # create your datset
dataloader = torch.utils.data.DataLoader(dataset) # create your dataloader








class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.up1 = nn.Linear(1000, 10000)
        self.up2 = nn.Linear(10000, 20000)

        self.down1 = nn.Linear(20000, 9050)
        self.down2 = nn.Linear(9050, 43)

        self.out = nn.Linear(43, 2)

    def forward(self, t):
        t = self.up1(t)
        t = F.relu(t)

        t = self.up2(t)
        t = F.relu(t)


        # (3) hidden linear layer
        t = self.down1(t)
        t = F.relu(t)

        # (4) hidden linear layer
        t = self.down2(t)
        t = F.relu(t)

        # (6) output layer
        t = self.out(t)

        return t

        
net = CNN()


criterion = nn.SmoothL1Loss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


print("start training")
for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(dataloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        print(inputs.shape)
        outputs = net(inputs)
        print(outputs)
        
        
        loss = criterion(outputs, labels)
        
        
        loss.backward()
        optimizer.step()
        

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')