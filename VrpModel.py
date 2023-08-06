import random
import math

class Model:
    def __init__(self):
        self.allNodes = []
        self.matrix = []
        self.capacity = -1

    def build_model(self,capacity):
        self.capacity = capacity

        warehouse = Node(0,250,250,0,0)
        self.allNodes.append(warehouse)
        birthday = 39
        random.seed(birthday)
        for i in range(100):
            idd = i+1
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            demand = random.randint(100, 300)
            unloading_time = 10
            customer = Node(idd, x, y, demand, unloading_time)
            self.allNodes.append(customer)

        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(len(self.allNodes)):
            for j in range(len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

class Node:
    def __init__(self,id,x,y,demand,unloading_time):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.time = unloading_time

class Route:
    def __init__(self,departure,capacity):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(departure)
        self.time_cost = 0
        self.capacity = capacity
        self.load = 0