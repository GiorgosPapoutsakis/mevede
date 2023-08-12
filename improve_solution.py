from vrp_model import *
from SolutionDrawer import *
from initial_solution import Solution
#33456.130850391106

class Swap_move:
    def __init__(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = None
    
    def initialise_again(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9

class Improver:
    def __init__(self,initial_solution,model):
        self.sol = initial_solution
        self.best_sol = None
        self.allNodes = model.allNodes
        self.warehouse = model.allNodes[0]      
        self.cost_matrix = model.matrix
        self.capacity = model.capacity

    def improve(self):
        self.local_search(1)
        self.report_solution(self.sol)

    def local_search(self, operator):
        self.best_sol = self.clone_solution(self.sol)
        termination_condition = False
        local_search_iterations = 0

        sm_obj = Swap_move()

        while termination_condition is False:
            
            sm_obj.initialise_again() #olous tous telestes
            #SolDrawer.draw(local_search_iterations, self.sol, self.allNodes)
            
            if operator == 1:
                self.find_best_swap_move(sm_obj)
                if sm_obj.origin_rt_pos is not None:
                    if sm_obj.move_cost_difference < 0:
                        self.apply_swap_move(sm_obj)
                    else:
                        termination_condition = True

            local_search_iterations += 1



    def clone_solution(self,solution):
        cloned_solution = Solution() #na valw klassi Solution sto vrp_model
        for i in range(len(solution.routes)):
            route = solution.routes[i]
            cloned_route = self.clone_route(route)
            cloned_solution.routes.append(cloned_route)
        cloned_route.cost = solution.cost
        return cloned_solution

    def clone_route(self,route):
        cloned_route = Route(self.warehouse, self.capacity)
        cloned_route.cumulative_cost = route.cumulative_cost
        cloned_route.load = route.load
        cloned_route.nodes_sequence = route.nodes_sequence.copy()
        return cloned_route

    def find_best_swap_move(self, sm_obj):
        for rt1_index in range(len(self.sol.routes)):
            origin_rt = self.sol.routes[rt1_index]
            for rt2_index in range(1, len(self.sol.routes)):
                target_rt = self.sol.routes[rt2_index]
                for node1_index_in_route in range(1, len(origin_rt.nodes_sequence)):
                    node2_index_in_route = 1
                    if origin_rt == target_rt:
                        node2_index_in_route = node1_index_in_route + 1
                    for node2_index_in_route in range(node1_index_in_route, len(target_rt.nodes_sequence)):

                        is_last1 = (len(origin_rt.nodes_sequence)-node1_index_in_route-1) == 0
                        #previous, selected, next
                        p1 = origin_rt.nodes_sequence[node1_index_in_route - 1]
                        s1 = origin_rt.nodes_sequence[node1_index_in_route]
                        if is_last1 is False:
                            n1 = origin_rt.nodes_sequence[node1_index_in_route + 1]
                        #poses fores prostithetai to kostos dist(A->B) sto cumulative_cost sto sugkekrimenou route
                        cost_multiplier1 = len(origin_rt.nodes_sequence)-node1_index_in_route

                        is_last2 = (len(target_rt.nodes_sequence)-node2_index_in_route-1) == 0
                        p2 = target_rt.nodes_sequence[node2_index_in_route - 1]
                        s2 = target_rt.nodes_sequence[node2_index_in_route]
                        if is_last2 is False:
                            n2 = target_rt.nodes_sequence[node2_index_in_route + 1]
                        cost_multiplier2 = len(target_rt.nodes_sequence)-node2_index_in_route

                        total_move_cost_differce = None
                        origin_route_cost_difference = None
                        target_route_cost_difference = None

                        if origin_rt == target_rt:
                            target_route_cost_difference = 0
                            if node1_index_in_route == node2_index_in_route - 1:
                                continue
                            else:
                                continue
                        else:
                            if origin_rt.load - s1.demand + s2.demand > self.capacity:
                                continue
                            if target_rt.load - s2.demand + s1.demand > self.capacity:
                                continue

                            cost_removed_rt1 = cost_multiplier1 * (self.cost_matrix[p1.id][s1.id] + s1.uploading_time)
                            if is_last1 is False:
                                cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]
                            cost_added_rt1 = cost_multiplier1 * (self.cost_matrix[p1.id][s2.id] + s2.uploading_time)
                            if is_last1 is False:
                                cost_added_rt1 += (cost_multiplier1-1) * self.cost_matrix[s2.id][n1.id]              
                            cost_removed_rt2 = cost_multiplier2 * (self.cost_matrix[p2.id][s2.id] + s2.uploading_time)
                            if is_last2 is False:
                                cost_removed_rt2 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added_rt2 = cost_multiplier2 * (self.cost_matrix[p2.id][s1.id] + s1.uploading_time)
                            if is_last2 is False:
                                cost_added_rt2 += (cost_multiplier2-1)*self.cost_matrix[s1.id][n2.id]

                            origin_route_cost_difference = cost_added_rt1 - cost_removed_rt1
                            target_route_cost_difference = cost_added_rt2 - cost_removed_rt2
                            total_move_cost_differce = cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2)

                        if total_move_cost_differce < sm_obj.move_cost_difference:
                            sm_obj.origin_rt_pos = rt1_index
                            sm_obj.target_rt_pos = rt2_index
                            sm_obj.selected_node1_pos = node1_index_in_route
                            sm_obj.selected_node2_pos = node2_index_in_route
                            sm_obj.cost_change_origin_rt = origin_route_cost_difference
                            sm_obj.cost_change_target_rt = target_route_cost_difference
                            sm_obj.move_cost_difference = total_move_cost_differce
    
    def apply_swap_move(self,sm_obj):
        old_cost = self.sol.cost
        route1 = self.sol.routes[sm_obj.origin_rt_pos]
        route2 = self.sol.routes[sm_obj.target_rt_pos]
        selected_node1 = route1.nodes_sequence[sm_obj.selected_node1_pos]
        selected_node2 = route2.nodes_sequence[sm_obj.selected_node2_pos]
        route1.nodes_sequence[sm_obj.selected_node1_pos] = selected_node2
        route2.nodes_sequence[sm_obj.selected_node2_pos] = selected_node1

        #print("routes load",sm_obj.origin_rt_pos, route1.load, sm_obj.target_rt_pos, route2.load)
        if route1 == route2:
            route1.cumulative_cost += sm_obj.cost_change_origin_rt
        else:
            route1.cumulative_cost += sm_obj.cost_change_origin_rt
            route2.cumulative_cost += sm_obj.cost_change_target_rt
            route1.load = route1.load - selected_node1.demand + selected_node2.demand
            route2.load = route2.load + selected_node2.demand - selected_node1.demand

        #print("routes load AFTER",sm_obj.origin_rt_pos, route1.load, sm_obj.target_rt_pos, route2.load)
        self.check_capacities(route1,route2)
    
        self.sol.cost += sm_obj.move_cost_difference

    def check_capacities(self,rt1,rt2):
        load1, load2 = 0, 0
        for node in rt1.nodes_sequence:            
            load1 += node.demand
        for node2 in rt2.nodes_sequence:            
            load2 += node2.demand
        print("routes_load", load1, load2)

        
    def report_solution(self, solution):
        print("Cost:")
        print(solution.cost)
        print("Routes:")
        print(len(solution.routes))
        for i in range(len(solution.routes)):
            rt = solution.routes[i]
            for j in range(len(rt.nodes_sequence)):
                print(rt.nodes_sequence[j].id, end=',')
            print(" ",rt.cumulative_cost)