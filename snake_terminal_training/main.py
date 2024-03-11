from game import *
from tqdm import tqdm
import copy

def main():
    nmbre_generation = 10
    population_generation = 100

    pourcentage_selection = 0.1
    mutation_rate = 0.01

    taille_plateau = 6
    temps_training = 200

    next_generation = [Game(taille_plateau, temps_training) for _ in range(population_generation)]
    for _ in tqdm(range(nmbre_generation)):
        for i in range(population_generation):
            next_generation[i].main_loop()

        new_generation = []

        # Selection des meilleurs agents
        score_generation = [len(agent.snake.list_body) - 1 for agent in next_generation]
        sorted_agents = [agent for _, agent in sorted(zip(score_generation, [i for i in range(100)]), reverse=True)]
        for top_agent in sorted_agents[:int(population_generation*pourcentage_selection)]:
            new_generation.append(next_generation[top_agent])
        
        # Mutation des meilleurs agents
        for i in range(int(population_generation*pourcentage_selection)):
            new_game = copy.deepcopy(new_generation[i])
            new_network = mutate(new_game.network, mutation_rate)
            new_game.network = new_network
            new_generation.append(new_game)
        
        # On complète avec des nouveaux agents
        for _ in range(2*int(population_generation*pourcentage_selection), population_generation):
            new_generation.append(Game(taille_plateau, temps_training))
        
        next_generation = new_generation
    
    top_agents = next_generation[0]
    print("Score top agents : ", len(top_agents.snake.list_body)-1)
    top_agents.sauvegarde()
    return

def mutate(network, mutation_rate):
    for param in network.parameters():
        if len(param.shape) == 2:  # Vérifier si le paramètre est une matrice de poids
            mutation_mask = torch.rand_like(param) < mutation_rate
            param.data += torch.randn_like(param) * mutation_mask.float()
    return network


if __name__ == "__main__":
    main()