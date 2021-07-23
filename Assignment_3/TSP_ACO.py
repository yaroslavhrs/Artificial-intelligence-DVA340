import random
import math
import time
from copy import copy
import matplotlib.pyplot as plt

number_of_locations = 52
number_of_ants = 75
init_pheromone = 10
location_obj = []
tau = []            # pheromone tau table
D = []              # distance matrix
eta = []            # heuristic information (1/distance)
L = []              # list of lists of visited cities of each ant
alpha = 0.95
beta = 1.5
p = 0.9
distance_list = []
final_best_dist = 100000
global_best_path = []
best_distance = 100000
iteration = 1
plot_generations = []
plot_distances = []

class City:
    location_id = 0
    x = 0
    y = 0
    def __init__(self, location_id, x, y):
        self.location_id = location_id
        self.x = x
        self.y = y
        

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


def init_pheromones():
    global tau
    line = []
    for i in range(number_of_locations):
        for j in range(number_of_locations):
            if i == j:
                line.append(0)
            else:
                line.append(init_pheromone)
        tau.append(copy(line))
        line.clear()
        

def init_distances():
    global D
    line = []
    for i in range(number_of_locations):
        for j in range(number_of_locations):
            if i == j:
                line.append(math.inf)
            else:
                line.append(find_distance(i, j))
        D.append(copy(line))
        line.clear()


def find_distance(i,j):
    global location_obj
    cityA = location_obj[i+1]
    cityB = location_obj[j+1]
    distance = math.sqrt(  pow((cityB.x - cityA.x),2) + pow((cityB.y - cityA.y),2) )
    return distance


def init_heuristic():
    global eta, D
    line = []
    for i in range(number_of_locations):
        for j in range(number_of_locations):
            if D[i][j] != 0 and D[i][j] != math.inf:
                heuristic = 1/(D[i][j])
                line.append(heuristic)
            else:
                line.append(0.0)
        eta.append(copy(line))
        line.clear()


def init_ants():
    global L
    L = []
    for k in range(number_of_ants):
        init_route = [0, 0]                         # start and end city index is index 0
        L.append(init_route)               


def build_solution():
    global L
    for i in range(1,number_of_locations):
        for k in range(number_of_ants):
            L[k].insert(-1, transition_rule(k))     # add the next city on second last position to the ant route


def transition_rule(k):
    global L
    result = 0
    possible_cities = []
    city_r = L[k][-2]
    probabilities = []
    summa = 0
    
    # denominator of probabilistic rule
    for city in range(number_of_locations):
        if city not in L[k]:
            possible_cities.append(city)
            summa += math.pow(tau[city_r][city], alpha) * math.pow(eta[city_r][city], beta)
            
    for city_s in possible_cities:
        # probability in which the ant k will move from city r to the city s
        probability = math.pow(tau[city_r][city_s], alpha) * math.pow(eta[city_r][city_s], beta) / summa
        probabilities.append([city_s, probability])
        
    # find the result of transition rule
    sum_p = 0
    norm_prob = []
    for i in range(len(probabilities)):
        sum_p += probabilities[i][1]
    for i in range(len(probabilities)):
        norm_prob.append(probabilities[i][1]/sum_p)     # normalized probability
    rand = random.random()
    rand_s= 0
    for i in range(len(norm_prob)):
        rand_s += norm_prob[i]
        if rand_s > rand:
            result = probabilities[i][0]                # index of next city
            break
    return result


def distance_L():
    global L , distance_list
    best_distance = 100000
    best_ant = 0
    for k in range(number_of_ants):
        distance = 0
        for i in range(len(L[k])-1):
            distance += find_distance(L[k][i], L[k][i+1])
            distance_list.append(distance)
        if distance < best_distance:
            best_distance = distance
            best_path = L[k]
            best_ant = k
    return best_distance, best_path, best_ant


def update_pheromones():
    global p, L, distance_list
    for i in range(number_of_locations):
        for j in range(number_of_locations):
            summa = 0
            for k in range(number_of_ants):
                if i in L[k] and j == L[k][L[k].index(i)+1]:
                    summa += 1/distance_list[k]
            tau[i][j] = (1-p)*tau[i][j] + summa                 # (1-p) is evaporation
            
            
def update_pheromones_best_ant(best_ant):
    global p, L, distance_list
    for i in range(number_of_locations):
        for j in range(number_of_locations):
            summa = 0
            if i in L[best_ant] and j == L[best_ant][L[best_ant].index(i)+1]:
                summa += 1/distance_list[best_ant]
            tau[i][j] = (1-p)*tau[i][j] + summa                 # (1-p) is evaporation
            
            

# Main
location_obj = read_file()      # list of instances of the class 'City'
init_pheromones()               # get the pheromone tau table
init_distances()                # get the distance D matrix
init_heuristic()                # get the heuristic 'eta' matrix


start_time = time.time()
while final_best_dist > 9000:
    init_ants()
    build_solution()
    best_distance, best_path, best_ant = distance_L()
    update_pheromones()
    if best_distance < final_best_dist:
        final_best_dist = best_distance
        global_best_path = best_path
        print("Best distance found: ", round(final_best_dist,2))
        plot_generations.append(iteration)
        plot_distances.append(final_best_dist)         
    update_pheromones_best_ant(best_ant)
    iteration += 1
end_time = time.time()

for i in range(len(global_best_path)):
    global_best_path[i] += 1

print()
print("Shortest route: ", global_best_path)
print("Number of iterations ", iteration)
print("Execution time: ", round((end_time-start_time), 2), "s")

plt.plot(plot_generations, plot_distances)
plt.xlabel('Generations')
plt.ylabel('Distances')
plt.show()