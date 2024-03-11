import torch
import torch.nn as nn
import numpy as np
from random import randint
import matplotlib.pyplot as plt

# Votre définition de QNetwork reste inchangée

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

def training_network_with_q_learning():
    learning_rate = 0.001
    epochs = 1000
    gamma = 0.99  # Facteur de remise

    q_network = QNetwork(4, 4)
    optimizer = torch.optim.Adam(q_network.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    total_score = 0
    reward_list = []
    loss_list = []

    for episode in range(epochs):
        etat = creation_list(4)
        input_tensor = torch.FloatTensor(etat)
        output_tensor = q_network(input_tensor)
        
        action = find_max(output_tensor.detach().numpy())
        reward = etat[action]  # Récompense pour l'action choisie
        
        # Mise à jour de l'état pour le Q-learning (étape simplifiée)
        next_etat = creation_list(4)
        next_input_tensor = torch.FloatTensor(next_etat)
        next_output_tensor = q_network(next_input_tensor)
        
        # Calcul de la valeur Q cible
        max_next_q = torch.max(next_output_tensor).item()
        q_target = reward + gamma * max_next_q
        q_value = output_tensor[action]
        
        loss = criterion(q_value, torch.tensor([q_target], dtype=torch.float32))
        loss_list.append(loss.item())

        total_score += reward
        reward_list.append(total_score)

        print(f"Episode {episode}, Action: {action}, Reward: {reward}, Loss: {loss.item()}")

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    plt.plot(reward_list)
    plt.title("Total Score Over Time")
    plt.show()
    plt.plot(loss_list)
    plt.title("Loss Over Time")
    plt.show()

# Remarque: Vous devriez adapter les fonctions creation_list et find_max pour mieux correspondre à votre environnement spécifique.

training_network_with_q_learning()
