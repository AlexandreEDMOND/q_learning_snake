from game import *
from network import *
from tqdm import tqdm
import copy

def main():
    nmbre_generation = 20
    population_generation = 100

    pourcentage_selection = 0.2
    mutation_rate = 0.01

    taille_plateau = 6
    temps_training = 200

    next_generation = [Network(33, 3) for _ in range(population_generation)]
    for _ in tqdm(range(nmbre_generation)):
        score_generation = []
        for i in range(population_generation):
            jeu = Game(taille_plateau, temps_training, next_generation[i])
            jeu.main_loop()
            score_generation.append(len(jeu.snake.list_body)-1)

        new_generation = []
        print("Max génération : ", max(score_generation))
        # Selection des meilleurs agents
        sorted_agents = [agent for _, agent in sorted(zip(score_generation, [i for i in range(100)]), reverse=True)]
        for top_agent in sorted_agents[:int(population_generation*pourcentage_selection)]:
            new_generation.append(next_generation[top_agent])
        
        # Mutation des meilleurs agents
        for i in range(int(population_generation*pourcentage_selection)):
            new_game = copy.deepcopy(new_generation[i])
            new_network = mutate(new_game, mutation_rate)
            new_game = new_network
            new_generation.append(new_game)
        
        # On complète avec des nouveaux agents
        for _ in range(2*int(population_generation*pourcentage_selection), population_generation):
            new_generation.append(Network(33, 3))
        
        next_generation = new_generation
    
    top_agents = next_generation[0]
    torch.save(top_agents.state_dict(),f'network_trained/model_trained_score_test.pth')
    return

def mutate(network, mutation_rate):
    for param in network.parameters():
        if len(param.shape) == 2:  # Vérifier si le paramètre est une matrice de poids
            mutation_mask = torch.rand_like(param) < mutation_rate
            param.data += torch.randn_like(param) * mutation_mask.float()
    return network


if __name__ == "__main__":
    main()