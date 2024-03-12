from game import *
from network import *
from tqdm import tqdm
import copy
import matplotlib.pyplot as plt

def print_top_scores(top_score):
    # Transposer la matrice pour avoir les scores par génération
    scores_transposed = list(map(list, zip(*top_score)))

    # Générer le graphique
    plt.figure(figsize=(10, 6))
    for i, gen_scores in enumerate(scores_transposed):
        plt.plot(range(1, len(gen_scores) + 1), gen_scores, label=f"Top {i+1}")

    plt.xlabel('Score')
    plt.ylabel('Génération')
    plt.title('Évolution des scores par génération')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    nmbre_generation = 500
    population_generation = 50
    repetition_game = 10

    pourcentage_selection = 0.2
    mutation_rate = 0.01

    taille_plateau = 6
    temps_training = 100

    nmbre_top_score = 5
    top_scores = []
    next_generation = [Network(33, 3) for _ in range(population_generation)]
    for gen in tqdm(range(nmbre_generation)):
        score_generation = []
        for i in range(population_generation):
            score = 0
            for _ in range(repetition_game):
                jeu = Game(taille_plateau, temps_training, next_generation[i])
                jeu.main_loop()
                score += len(jeu.snake.list_body)-1
            score_generation.append(score/repetition_game)

        new_generation = []
        print("\nMax génération : ", max(score_generation))
        top_scores.append(sorted(score_generation, reverse=True)[:nmbre_top_score])
        # Selection des meilleurs agents
        sorted_agents = [agent for _, agent in sorted(zip(score_generation, [i for i in range(100)]), reverse=True)]
        for top_agent in sorted_agents[:int(population_generation*pourcentage_selection)]:
            new_generation.append(next_generation[top_agent])
        
        # Mutation des meilleurs agents
        for i in range(int(population_generation*pourcentage_selection)):
            for _ in range(2):
                new_game = copy.deepcopy(new_generation[i])
                new_network = mutate(new_game, mutation_rate)
                new_game = new_network
                new_generation.append(new_game)
        
        # On complète avec des nouveaux agents
        for _ in range(3*int(population_generation*pourcentage_selection), population_generation):
            new_generation.append(Network(33, 3))
        
        next_generation = new_generation
    
        top_agents = next_generation[0]
        torch.save(top_agents.state_dict(),f'network_trained/model_trained_gen_{gen}_score_{top_scores[gen][0]}.pth')
    
    print_top_scores(top_scores)
    return

def mutate(network, mutation_rate):
    for param in network.parameters():
        if len(param.shape) == 2:  # Vérifier si le paramètre est une matrice de poids
            mutation_mask = torch.rand_like(param) < mutation_rate
            param.data += torch.randn_like(param) * mutation_mask.float()
    return network


if __name__ == "__main__":
    main()