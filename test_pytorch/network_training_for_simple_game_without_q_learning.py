import torch
import torch.nn as nn
import numpy as np
from random import randint
import matplotlib.pyplot as plt

class QNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(QNetwork, self).__init__()
        self.fc = nn.Linear(input_size, 10)
        self.fc2 = nn.Linear(10, output_size)

    def forward(self, x):
        x = torch.relu(self.fc(x))
        x = self.fc2(x)
        return x


def creation_list(long_list):
    liste = [-1 for _ in range(long_list)]
    liste[randint(0, long_list-1)] = 1
    return liste

def find_max(liste):
    max = liste[0]
    indice = 0

    for i in range(1,len(liste)):
        if liste[i] > max:
            max = liste[i]
            indice = i
    
    return indice


def training_network():
    # Hyperparamètres
    learning_rate = 0.001
    gamma = 0.99
    num_episodes = 500


    q_network = QNetwork(4, 4)
    optimizer = torch.optim.Adam(q_network.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    # Suivi de l'évolution
    total_score = 0
    reward_list = []

    for episode in range(num_episodes):
        etat = creation_list(4)
        
        # Convertir l'état en tenseur PyTorch
        input_tensor = torch.FloatTensor(etat)
        
        # Obtenir les probabilités d'action à partir du réseau de neurones
        output_tensor = q_network(input_tensor)
        
        output_data = output_tensor.detach().numpy()

        # Choix de l'action en utilisant les probabilités
        action = find_max(output_data)

        reward = etat[action]

        for i in range(len(etat)):
            if etat[i] == -1:
                etat[i] = 0
        loss = criterion(output_tensor, torch.tensor(etat, dtype=torch.float32))

        total_score += reward
        reward_list.append(total_score)

        # Affichage de la récompense
        print(f"Episode {episode}, Action: {action}, Reward: {reward}")

        # Mise à jour du réseau de neurones par la récompense
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    plt.plot(reward_list)
    plt.show()

training_network()