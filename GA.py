import random
import os

class GeneticAlgorithm:
    def __init__(self, target_text):
        self.target_text = target_text
        self.text_length = len(target_text)

    # Create gen representation
    def create_gen(self):
        return "".join([chr(random.randint(32, 126)) for i in range(self.text_length)])

    # Calculate fitness value of each gen
    def calculate_fitness(self, gen):
        fitness_value = sum([1 if g==t else 0 for g,t in zip([*gen], [*self.target_text])])
        return (fitness_value/self.text_length)*100

    # Create population
    def create_population(self, population_size):
        population = dict()
        for i in range(0, population_size):
            gen = self.create_gen()
            population[i] = {'gen': gen, 'FV': self.calculate_fitness(gen)}
        return population

    # Parent selection
    def create_parents(self, population):
        pops = list(population.values())
        parents = list()
        for i in range(2):
            max_key = max(range(len(pops)), key= lambda i: pops[i]['FV'])
            parents.append(pops[max_key]['gen'])
            pops.pop(max_key)
        return parents

    # Random point crossover to create children
    def create_children(self, parents):
        COindex = random.sample(range(len(self.target_text)), len(self.target_text)//2)
        child1 = parents[0]
        child2 = parents[1]
        # cross-over-ing
        for coi in sorted(COindex):
            child1 = child1[:coi] + parents[1][coi] + child1[coi+1:]
            child2 = child2[:coi] + parents[0][coi] + child2[coi+1:]
        return list([child1, child2])
    
    def create_mutants(self, children, mutation_rate):
        mutants = list()
        for child in children:
            mutant = child
            for i in range(len(child)):
                if random.uniform(0,1) < mutation_rate:
                    mutant = mutant[:i] + chr(random.randint(32,126)) + mutant[i+1:]
            mutants.append(mutant)
        return mutants

    def regeneration(self, mutants, population):
        sorted_population = sorted(list(population.values()), key=lambda x:x['FV'])[2:]
        for mutant in mutants:
            sorted_population.append({
                'gen': mutant,
                'FV': self.calculate_fitness(mutant)
            })
        population = dict()
        for i, individual in enumerate(sorted_population):
            population[i] = individual
        return population

    def runGA(self, population_size, mutation_rate):
        population = self.create_population(population_size)
        generation = 0
        isLooping = True
        while isLooping:
            parents = self.create_parents(population)
            children = self.create_children(parents)
            mutants = self.create_mutants(children, mutation_rate)
            population = self.regeneration(mutants, population)
            best_gen = self.create_parents(population)[0]
            generation += 1
            print('[INFO]: Searching...')
            print(f'Target\t\t: {self.target_text}')
            print(f'Solution\t: {best_gen}')
            print(f'Generation\t: {generation}')
            self.clearConsole()
            if best_gen == self.target_text:
                isLooping = False
        return best_gen, generation

    def clearConsole(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)