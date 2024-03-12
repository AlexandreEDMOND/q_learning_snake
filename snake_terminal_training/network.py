import torch
import torch.nn as nn
import torch.nn.functional as F

class Network(nn.Module):
    def __init__(self, input_size, output_size):
        super(Network, self).__init__()
        self.fc = nn.Linear(input_size, 50)
        self.fc2 = nn.Linear(50, output_size)

    def forward(self, x):
        x = F.relu(self.fc(x))
        x = self.fc2(x)
        x = F.softmax(x, dim=x.dim()-1)  # Cela appliquera softmax sur la dernière dimension, qu'importe le shape de x
        return x
    
