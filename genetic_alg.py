import random

MAX_GENERATIONS = 1000
POPULATION_NO = 50
N_QUEENS = 8
MUTATION_RATE = 0.1


def main():
    generations = 1
    populations = []
    populations = generate_population(populations)
    while generations <= MAX_GENERATIONS:
        fitness_vals = fitness_function(populations)
        best_fitness = max(fitness_vals)
        pop_index = fitness_vals.index(max(fitness_vals))
        print(f"Fitness values are {fitness_vals}, "
              f"Population is {populations}, "
              f"Maximum fitness is {best_fitness}"
              f"Population Index is {pop_index}")
        print("-------------------------------------------------------------------------")
        print(f"Generation {generations}'s maximum fitness score is {max(fitness_vals)} for the population, {populations[pop_index]}")
        if best_fitness == N_QUEENS * (N_QUEENS - 1) // 2:
            print(f"Solution found in generation {generations}!")
            break
        probability_values, cumulative_prob_values = fitness_calculation(fitness_vals)
        offsprings = selection(populations, cumulative_prob_values)
        new_gen = crossover(offsprings)
        populations = mutation(new_gen)
        generations += 1
        print("-------------------------------------------------------------------------")
    if generations >= MAX_GENERATIONS:
        print("Solution not found")


def generate_population(populations):
    single_pop = []
    for i in range(POPULATION_NO):  # 4
        for j in range(0, N_QUEENS):  # 8
            element = random.randint(0, N_QUEENS - 1)
            single_pop.append(element)
        populations.append(single_pop)
        single_pop = []
    return populations


def fitness_function(populations):
    fitness_values = []
    for pop in populations:
        non_attacking_queens = 0
        for col1 in range(0, N_QUEENS):
            for col2 in range(col1 + 1, N_QUEENS):
                col_distance = abs(col2 - col1)
                if pop[col1] != pop[col2] and col_distance != abs(pop[col1] - pop[col2]):
                    # First condition is for checking rows and columns. Second is for diagonals
                    non_attacking_queens += 1
        fitness_values.append(non_attacking_queens)  # For each values
    print(fitness_values)
    return fitness_values


def fitness_calculation(fitness_values):
    sum_of_fitness_values = sum(fitness_values)
    probability_values = list(map(lambda n: (n / sum_of_fitness_values), fitness_values))
    cumulative_prob_values = probability_values.copy()
    if sum(probability_values) > 1:
        print("Normalizing probability values")
        cumulative_prob_values = [p / sum(probability_values) for p in
                                  probability_values]  # Normalizing probability values
    for i in range(1, len(probability_values)):
        cumulative_prob_values[i] = cumulative_prob_values[i] + cumulative_prob_values[i - 1]
    return probability_values, cumulative_prob_values


def generate_indices(cumulative_prob_values, no_of_parents):
    # Using roulette wheel.
    indices = random.choices(
        population=range(len(cumulative_prob_values)),
        weights=cumulative_prob_values,
        k=no_of_parents
    )
    print(f"Indices are {indices}")
    return indices


def selection(populations, cumulative_prob_values):
    no_of_parents = len(populations)
    indices = generate_indices(cumulative_prob_values, no_of_parents)
    offsprings = [populations[i] for i in indices]
    return offsprings


def crossover(offsprings):
    # We calculate single crossover point
    crossover_point = random.randint(1, N_QUEENS-1)
    print(f"Before Crossover, Crossover Point {crossover_point}, Offsprings {offsprings}")
    for i in range(0, len(offsprings) - 1, 2):
        # Perform crossover between pairs
        parent1, parent2 = offsprings[i], offsprings[i + 1]
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        offsprings[i], offsprings[i + 1] = child1, child2
    print(f"After Crossover, Crossover Point {crossover_point}, Offsprings {offsprings}")
    return offsprings


def mutation(populations):
    for row in range(len(populations)):
        for col in range(N_QUEENS):
            if random.random() < MUTATION_RATE:
                populations[row][col] = random.randrange(N_QUEENS)
    return populations


main()
