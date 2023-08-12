from vrp_model import *
from SolutionDrawer import *
#33804.84774780611

class Swap_move:
    def __init__(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9
    
    def initialise_again(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9

class Improver:
    def __init__(self, initial_solution, model):
        self.sol = initial_solution
        self.allNodes = model.allNodes     
        self.cost_matrix = model.matrix
        self.capacity = model.capacity
        self.best_sol = None #den kserw an xreiazetai

    def improve(self):
        self.local_search(1)
        print("IMPROVED")
        self.sol.report_solution()

    def local_search(self, operator):

        # self.best_sol = self.sol.clone_solution(self.allNodes[0], self.capacity)
        # print("CLONED")
        # self.best_sol.report_solution()

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
            #print(local_search_iterations, self.sol.cost) #extra mia epanalipsi gia na vgei

        #     self.TestSolution()

        #     if (self.sol.cost < self.best_sol.cost):
        #         self.best_sol = self.sol.clone_solution(self.allNodes[0], self.capacity)
        # self.sol = self.best_sol

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

                        #Orgin route INFO
                        is_last1 = (len(origin_rt.nodes_sequence)-node1_index_in_route-1) == 0
                        p1 = origin_rt.nodes_sequence[node1_index_in_route - 1] #previous
                        s1 = origin_rt.nodes_sequence[node1_index_in_route] #selected
                        if is_last1 is False:
                            n1 = origin_rt.nodes_sequence[node1_index_in_route + 1] #next
                        cost_multiplier1 = len(origin_rt.nodes_sequence)-node1_index_in_route #fores pou prostithetai to cost[ dist(previous->selected)+selected.uploading_time ] sto cumulative_cost gia to sugkekrimeno route. Ean o selected OXI TELEUTAIOS: +cost[ dist(selcted->next)]*(multiplier-1)

                        #Target route Info
                        is_last2 = (len(target_rt.nodes_sequence)-node2_index_in_route-1) == 0
                        p2 = target_rt.nodes_sequence[node2_index_in_route - 1]
                        s2 = target_rt.nodes_sequence[node2_index_in_route]
                        if is_last2 is False:
                            n2 = target_rt.nodes_sequence[node2_index_in_route + 1]
                        cost_multiplier2 = len(target_rt.nodes_sequence)-node2_index_in_route

                        total_move_cost_differce = None
                        origin_route_cost_difference = None
                        target_route_cost_difference = None

                        if (origin_rt == target_rt) and (node1_index_in_route == node2_index_in_route - 1):
                            
                            cost_removed = cost_multiplier1 * (self.cost_matrix[p1.id][s1.id] + s1.uploading_time) + cost_multiplier2 * (self.cost_matrix[s1.id][s2.id] + s2.uploading_time)
                            if is_last2 is False:
                                cost_removed += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added = cost_multiplier1 * (self.cost_matrix[p1.id][s2.id] + s2.uploading_time) + cost_multiplier2 * (self.cost_matrix[s2.id][s1.id] + s1.uploading_time)
                            if is_last2 is False:
                                cost_added += (cost_multiplier2-1) * self.cost_matrix[s1.id][n2.id]

                            origin_route_cost_difference = cost_added - cost_removed
                            target_route_cost_difference = 0
                            total_move_cost_differce = cost_added - cost_removed                         
                            
                        else:
                            if origin_rt != target_rt:
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

                            if origin_rt == target_rt:
                                origin_route_cost_difference = cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2)
                                target_route_cost_difference = 0
                            else:
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
    
    def apply_swap_move(self, sm_obj):
        route1 = self.sol.routes[sm_obj.origin_rt_pos]
        route2 = self.sol.routes[sm_obj.target_rt_pos]
        selected_node1 = route1.nodes_sequence[sm_obj.selected_node1_pos]
        selected_node2 = route2.nodes_sequence[sm_obj.selected_node2_pos]
        route1.nodes_sequence[sm_obj.selected_node1_pos] = selected_node2
        route2.nodes_sequence[sm_obj.selected_node2_pos] = selected_node1

        if route1 == route2:
            route1.cumulative_cost += sm_obj.cost_change_origin_rt
        else:
            route1.cumulative_cost += sm_obj.cost_change_origin_rt
            route2.cumulative_cost += sm_obj.cost_change_target_rt
            route1.load = route1.load - selected_node1.demand + selected_node2.demand
            route2.load = route2.load - selected_node2.demand + selected_node1.demand

        self.sol.cost += sm_obj.move_cost_difference


################
    def TestSolution(self):
        testing_solution = self.sol
        totalSolCost = 0
        for r in range (len(testing_solution.routes)):
            route = testing_solution.routes[r]
            calc_rt_TimeCost = 0
            calc_rtCost = 0
            calc_rtLoad = 0
            for n in range (len(route.nodes_sequence)-1):
                A = route.nodes_sequence[n]
                B = route.nodes_sequence[n+1]
                calc_rt_TimeCost += self.cost_matrix[A.id][B.id] + B.uploading_time
                calc_rtCost += calc_rt_TimeCost
                calc_rtLoad += B.demand

            if abs(calc_rtCost - route.cumulative_cost) > 0.0001:
                #print(r, calc_rtCost, route.cumulative_cost)
                print ('Route Cost problem')
            if calc_rtLoad != route.load:
                #print(r, calc_rtLoad, route.load)
                print ('Route Load problem')
            
            totalSolCost += route.cumulative_cost
        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')
        print("TEST HAS ENDED")