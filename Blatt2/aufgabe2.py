import numpy as np
import random



class Individum():
    def __init__(self):
        self.problems = 0
        self.fitness = 0
        self.bit_string = ""
        self.arr = []


#1D Array von der Länge 8 und Werten von 1-8
def create_population(size=100): #Standart Wer ist 100
    creation = []
    for i in range(size):
        arr = np.array([random.randint(0,7),
                        random.randint(0,7),
                        random.randint(0,7),
                        random.randint(0,7),
                        random.randint(0,7),
                        random.randint(0,7),
                        random.randint(0,7)])
        indiv = Individum()
        indiv.arr = arr
        creation.append(indiv)

    return creation

def bitstring_to_array(indiv):
    problem_array = []
    for i in range(0, len(indiv.bit_string), 3):
        bits = indiv.bit_string[i:i + 3]
        zahl = int(bits, 2)
        problem_array.append(zahl)
    indiv.arr = problem_array
    return problem_array

def array_to_bitstring(indiv):
    indiv.bit_string = ''.join(format(x, '03b') for x in indiv.arr)
    return indiv.bit_string

def fitness_funktion(indiv):
    problems= 0
    n = len(indiv.arr)

    for i in range(n):
        for j in range(i + 1, n):
            same_row = indiv.arr[i] == indiv.arr[j]
            same_diag = abs(indiv.arr[i] - indiv.arr[j]) == abs(i - j)
            if same_row or same_diag:
                problems += 1
    indiv.problems = problems
    indiv.fitness = 64 - problems
    return indiv.fitness


#Tournement Selection
#Eine Menge von Induividuen Auswählen
#Die Fittesten nehmen
def selection(population):

    population.sort(key=lambda x: x.fitness)
    half = int(len(population)/2)
    population.sort(key=lambda x: x.fitness)
    best = population[:half]
    worst = population[half:]

    num = len(population)//4
    selected_worst = random.sample(worst, num)

    new_population = best + selected_worst
    missing = create_population(len(population) - len(new_population))
    for indiv in missing:
        array_to_bitstring(indiv)
        fitness_funktion(indiv)
    new_population += missing

    return new_population

def crossover(parent1, parent2):

    if not parent1.bit_string:
        array_to_bitstring(parent1)
    if not parent2.bit_string:
        array_to_bitstring(parent2)


    point = random.randint(1, len(parent1.bit_string) - 2)


    child1_bits = parent1.bit_string[:point] + parent2.bit_string[point:]
    child2_bits = parent2.bit_string[:point] + parent1.bit_string[point:]

    child1 = Individum()
    child1.bit_string = child1_bits
    bitstring_to_array(child1)
    fitness_funktion(child1)

    child2 = Individum()
    child2.bit_string = child2_bits
    bitstring_to_array(child2)
    fitness_funktion(child2)

    return child1, child2

def reproduction(population):
    new_generation = []

    random.shuffle(population)

    for i in range(0, len(population) - 1, 2):
        parent1 = population[i]
        parent2 = population[i + 1]

        #70% Wkeit Crossover
        if random.random() < 0.7:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2

        new_generation.extend([child1, child2])

    return new_generation


def mutation(indiv):

    if not indiv.bit_string:
        array_to_bitstring(indiv)

    pos = random.randint(0, len(indiv.bit_string) - 1)

    flipped_bit = '1' if indiv.bit_string[pos] == '0' else '0'

    #Im String ersetzten
    indiv.bit_string = indiv.bit_string[:pos] + flipped_bit + indiv.bit_string[pos + 1:]

    bitstring_to_array(indiv)


def main_funktion(populationsize = 100):
    population = create_population(populationsize)
    best, worst, avg = 0,0,0
    generation = 0
    while best < 64:
        generation +=1

        for indiv in population:
            fitness_funktion(indiv)

        best_indiv = population[0]
        best = best_indiv.fitness

        for indiv in population:
            avg += indiv.fitness
        avg /= len(population)

        if best == 64:
            print(best_indiv.arr)
            break
        print(f"best: {best}, worst: {worst}, avg: {avg}")

        #crossover und mutation
        population = selection(population)
        population = reproduction(population)
        for indiv in population:
            mutation(indiv)

main_funktion(100)