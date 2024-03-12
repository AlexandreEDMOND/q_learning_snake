from network import *
import matplotlib.pyplot as plt
import copy

SIZE_INPUT_NETWORK = 100

def generate_random_tensor(size):
    return torch.rand(size)

def fonction_evaluation(network, nmbre_eval=100):
    evaluations = []

    for _ in range(nmbre_eval):
        input_tensor = generate_random_tensor(SIZE_INPUT_NETWORK)
        output = network(input_tensor)
        output_sum = torch.sum(output)
        evaluations.append(output_sum.item())

    moyenne = sum(evaluations) / len(evaluations)

    return moyenne

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

def mutate(network, mutation_rate):
    for param in network.parameters():
        if len(param.shape) == 2:  # Vérifier si le paramètre est une matrice de poids
            mutation_mask = torch.rand_like(param) < mutation_rate
            param.data += torch.randn_like(param) * mutation_mask.float()
    return network

def main_loop():
    nmbre_generation = 100
    population_generation = 100

    pourcentage_selection = 0.2
    mutation_rate = 0.01

    next_generation = [Network(SIZE_INPUT_NETWORK, 10) for _ in range(population_generation)]

    nmbre_top_score = 5
    top_scores = []
    for i in range(nmbre_generation):
        score_generation = []
        for j in range(population_generation):
            score_generation.append(fonction_evaluation(next_generation[j]))
        
        new_generation = []
        print(f"\nMax génération {i} : ", max(score_generation))
        top_scores.append(sorted(score_generation, reverse=True)[:nmbre_top_score])
        # Selection des meilleurs agents
        sorted_agents = [agent for _, agent in sorted(zip(score_generation, next_generation), reverse=True)]
        for top_agent in sorted_agents[:int(population_generation*pourcentage_selection)]:
            new_generation.append(top_agent)
        
        # Mutation des meilleurs agents
        for i in range(int(population_generation*pourcentage_selection)):
            new_game = copy.deepcopy(new_generation[i])
            new_network = mutate(new_game, mutation_rate)
            new_game = new_network
            new_generation.append(new_game)
        
        # On complète avec des nouveaux agents
        for _ in range(2*int(population_generation*pourcentage_selection), population_generation):
            new_generation.append(Network(SIZE_INPUT_NETWORK, 10))
        
        next_generation = new_generation
    
    print_top_scores(top_scores)

