from GA import GeneticAlgorithm

target_text = input('Input text (strings):')
population_size = int(input('Population Size (integer>=4): '))
mutation_rate = float(input('Mutation Rate (float, 0-1): '))

GA = GeneticAlgorithm(target_text)
best_gen, generation = GA.run(population_size, mutation_rate)

print("GA results:")
print(f'Target\t\t: {target_text}')
print(f'Solution\t: {best_gen}')

print(f'Generation\t: {generation}')
