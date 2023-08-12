import random
import math

class Model:
    def __init__(self):
        self.allNodes = []
        self.matrix = []
        self.capacity = 1700
        self.maxRoutes = 14

    def build_model(self):
        warehouse = Node(0, 250, 250, 0, 0)
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
        self.matrix = [ [0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

        # NODES INFO
        # for node in self.allNodes:
        #     print(f"{node.id},{node.x},{node.y},{node.demand},{node.uploading_time}")

class Node:
    def __init__(self,idd,xx,yy,dem,time):
        self.id = idd
        self.x = xx
        self.y = yy
        self.demand = dem
        self.uploading_time = time
        self.isRouted = False

class Route:
    def __init__(self,warehouse,capacity):
        self.nodes_sequence = []
        self.nodes_sequence.append(warehouse)
        self.time_cost = 0.0
        self.cumulative_cost = 0.0
        self.capacity = capacity
        self.load = 0

class Solution():
    def __init__(self):
        self.cost = 0.0
        self.routes = []

    def report_solution(self):
            print("***")
            print("Cost:")
            print(self.cost)
            print("Routes:")
            print(len(self.routes))
            for i in range(len(self.routes)):
                rt = self.routes[i]
                for j in range(len(rt.nodes_sequence)):
                    print(rt.nodes_sequence[j].id, end=',')
                print(" ",rt.cumulative_cost)

    def clone_solution(self, deposit_node, capacity): #pithanotata den xreiazetai
        cloned_solution = Solution()
        for i in range(len(self.routes)):
            route = self.routes[i]
            cloned_route = self.clone_route(route, deposit_node, capacity)
            cloned_solution.routes.append(cloned_route)
        cloned_solution.cost = self.cost
        return cloned_solution

    def clone_route(self, route, warehouse, capacity):
        cloned_route = Route(warehouse, capacity)
        cloned_route.cumulative_cost = route.cumulative_cost
        cloned_route.load = route.load
        cloned_route.nodes_sequence = route.nodes_sequence.copy()
        return cloned_route