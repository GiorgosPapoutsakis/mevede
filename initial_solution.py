from vrp_model import *
from SolutionDrawer import *

class Solution():
    def __init__(self):
        self.cost = 0.0
        self.routes = []
    
class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9
    
class Solver:
    def __init__(self,model):
        self.allNodes = model.allNodes
        self.warehouse = model.allNodes[0]
        self.cost_matrix = model.matrix
        self.capacity = model.capacity
        self.max_routes = model.maxRoutes
        self.initial_solution = None

    def solve(self):
        self.apply_nearest_neighbor_method()
        self.report_solution(self.initial_solution)
        return self.initial_solution
    
    def apply_nearest_neighbor_method(self):
        self.initial_solution = Solution()
        insertions = 0

        while insertions < (len(self.allNodes) - 1):
            bestInsertionObject = CustomerInsertion()
            lastOpenRoute = self.get_last_open_route()

            if lastOpenRoute is not None:
                self.identify_best_customer_to_insert(bestInsertionObject, lastOpenRoute)

            if bestInsertionObject.customer is not None:
                self.apply_best_customer_insertion(bestInsertionObject)
                insertions += 1
            else:
                if len(self.initial_solution.routes) + 1 > self.max_routes:
                    print("No more vehicles to use")
                    break
                else:
                    new_route = Route(self.warehouse, self.capacity)
                    self.initial_solution.routes.append(new_route)

    def get_last_open_route(self):
        if len(self.initial_solution.routes) == 0:
            return None
        else:
            return self.initial_solution.routes[-1]
        
    def identify_best_customer_to_insert(self, bestInsertionObject, route):
        for i in range(1,len(self.allNodes)):
            canditate_customer_to_insert = self.allNodes[i]
            if canditate_customer_to_insert.isRouted is False:
                if route.load + canditate_customer_to_insert.demand <= route.capacity:
                    last_node_in_this_route = route.nodes_sequence[-1]
                    canditate_cost = self.cost_matrix[last_node_in_this_route.id][canditate_customer_to_insert.id]
                    if canditate_cost < bestInsertionObject.cost:
                        bestInsertionObject.customer = canditate_customer_to_insert
                        bestInsertionObject.route = route
                        bestInsertionObject.cost = canditate_cost

    def apply_best_customer_insertion(self,bestInsertionObject):
        customer_to_insert = bestInsertionObject.customer
        route_to_insert = bestInsertionObject.route
        route_to_insert.nodes_sequence.append(customer_to_insert)
        node_before_inserted = route_to_insert.nodes_sequence[-2]

        costAdded = self.cost_matrix[node_before_inserted.id][customer_to_insert.id] + customer_to_insert.uploading_time

        route_to_insert.cost += costAdded
        route_to_insert.load += customer_to_insert.demand
        customer_to_insert.isRouted = True
        self.initial_solution.cost += costAdded
        
    def report_solution(self, initial_solution):
        print("Cost:")
        print(self.initial_solution.cost)
        print("Routes:")
        print(len(initial_solution.routes))
        for i in range(len(initial_solution.routes)):
            rt = initial_solution.routes[i]
            for j in range(len(rt.nodes_sequence)):
                print(rt.nodes_sequence[j].id, end=',')
            print(" ",rt.cost)
        
        SolDrawer.draw('Inital_Sol', self.initial_solution, self.allNodes) #meta mono gia na vlepw ti ginetai