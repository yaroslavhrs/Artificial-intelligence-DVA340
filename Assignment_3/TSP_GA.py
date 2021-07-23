import random
import math
import time
import matplotlib.pyplot as plt


class City:
    location_id = 0
    x = 0
    y = 0
    def __init__(self, location_id, x, y):
        self.location_id = location_id
        self.x = x
        self.y = y 


class Individual:
    path = []
    distance = 0
    def __init__(self, path, distance):
        self.path = path
        self.distance = distance
        
        
def read_file():
    global location_obj
    with open('Assignment 3 berlin52.tsp') as file:
        lines = file.readlines()
    locations = lines[6:58]
    location_obj = {}
    for k in range(1, 53):
        location_obj[k] = None
    for i in range(0, len(locations)):
        locations[i] = locations[i].replace('\n','')
        locations[i] = locations[i].replace('.0','')
        locations[i] = locations[i].split()
        locations[i][0], locations[i][1], locations[i][2] = int(locations[i][0]), int(locations[i][1]), int(locations[i][2])
        city = City(locations[i][0], locations[i][1], locations[i][2])
        location_obj[i+1] = city
    return location_obj


def create_random_chromosome(number_of_locations, location_obj):
    global population
    chromosome = []
    for i in range(2,number_of_locations+1):
        chromosome.append(i)
    random.shuffle(chromosome)
    chromosome.insert(0, 1)
    chromosome.insert(52, 1)
    distance = find_distance(chromosome, location_obj)
    individual = Individual(chromosome, distance)
    population.append(individual)
    return


def find_distance(path, location_obj):
    distance = 0
    i = 0
    j = 0
    for k in range(len(path)-1):
        i = path[k]
        j = path[k+1]
        cityA = location_obj[i]
        cityB = location_obj[j]
        dist = math.sqrt(  pow((cityB.x - cityA.x),2) + pow((cityB.y - cityA.y),2) )
        distance += dist
    return distance


def calculate_fitness(population):
    fitness = []
    for i in population:
        fitness.append(1/(i.distance+1))
    return fitness


def normalize_fitness(fitness):
    total_fitness = 0
    for i in fitness:
        total_fitness += i
    for i in range(len(fitness)):
        fitness[i] = fitness[i]/total_fitness
    return fitness


def find_best_parent(norm_fitness):
    index = 0
    best_fitness = 0
    parent = None
    for i in range(len(norm_fitness)):
        if norm_fitness[i] > best_fitness:
            best_fitness = norm_fitness[i]
            index = i
    parent = population[index]
    return parent


def find_second_parent(fitness, parent_1):
    max_fitness = max(fitness)
    index = random.randint(0, len(population)-1)
    while population[index] == parent_1:
            index = random.randint(0, len(population)-1)
    while fitness[index] < random.uniform(0, max_fitness):
        index = random.randint(0, len(population)-1)
        while population[index] == parent_1:
            index = random.randint(0, len(population)-1)
    return population[index]


def crossover(parent_1, fitness):
    parent_2 = find_second_parent(fitness, parent_1)
    global flip_parents_rate
    if random.random() < flip_parents_rate:
        parent_1, parent_2 = parent_2, parent_1
    a = random.randint(1, 50)
    b = random.randint(a, 51)
    child = [None] * len(parent_1.path)
    child[len(child)-1] = 1
    child[0] = 1
    genA = []
    genB = []
    for i in range(a, b+1):
        genA.append(parent_1.path[i])
    k = a
    for i in genA:
        child[k] = i
        k += 1
    for i in range(1, 52):
        if parent_2.path[i] not in genA: 
            genB.append(parent_2.path[i])
    for i in range(1, len(child)-1):
        if child[i] == None:
            child[i] = genB.pop(0)     
    distance = find_distance(child, location_obj)
    individual = Individual(child, distance)
    return individual
            

def mutation(child):
    global mutation_rate
    while True:
        if random.random() < mutation_rate:
            indexA = random.randint(1, len(child.path)-2)
            indexB = random.randint(1, len(child.path)-2)
            if indexA == indexB:
                continue
            taken_list = child.path[indexA:indexB+1]
            mutation_list = taken_list[::-1]
            for i in range(len(mutation_list)):
                child.path[indexA+i] = mutation_list[i]
            return child
        else:
            return child
    

def new_population():
    global population
    global best_distance
    global best_path
    global end_time
    global generations
    global distances
    global final_distance
    generation = 1
    previous_best = 100000
    k = 0
    counter = 0
    while True:
        new_population = []
        fitness = calculate_fitness(population)
        norm_fitness = normalize_fitness(fitness)        
        parent_1 = find_best_parent(norm_fitness)   
        for i in range(len(population)):
            child = crossover(parent_1, fitness)
            mutated_child = mutation(child)
            new_population.append(mutated_child)
        population = new_population
        generation += 1
        for i in population:
            if i.distance < best_distance:
                best_distance = i.distance
                best_path = i.path
        if best_distance < previous_best:
            print("Best distance found: ", round(best_distance, 2), "Generation: ", generation)
            previous_best = best_distance
            generations.append(generation)
            distances.append(best_distance)            
        if best_distance < final_distance:
            if k > 100:
                end_time = time.time()
                print("Best path: ", best_path)
                break
            k += 1
        counter += 1

# Main
number_of_locations = 52
number_of_chromosomes = 50
best_distance = 100000
final_distance = 9000
mutation_rate = 0.01
flip_parents_rate = 0.5
best_path = []
population = []
generations = []
distances = []

location_obj = read_file()      # list of instances of the class 'City'

for i in range(number_of_chromosomes):
    create_random_chromosome(number_of_locations, location_obj)
start_time = time.time()
end_time = None
new_population()

print("Time of execution: ", round((end_time-start_time), 2))

plt.plot(generations, distances)
plt.xlabel('Generations')
plt.ylabel('Distances')
plt.show()