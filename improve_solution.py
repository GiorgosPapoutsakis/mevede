from vrp_model import *
from SolutionDrawer import *
#31924.448077515277

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

class Relocation_move:
    def __init__(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9    
    def initialise_again(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9

class TwoOpt_move:
    def __init__(self) -> None:
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.origin_rt_new_load = None
        self.target_rt_new_load = None
        self.move_cost_difference = 10**9
    def initialise_again(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.origin_rt_new_load = None
        self.target_rt_new_load = None
        self.move_cost_difference = 10**9

class Improver:
    def __init__(self, initial_solution, model):
        self.sol = initial_solution
        self.allNodes = model.allNodes     
        self.cost_matrix = model.matrix
        self.capacity = model.capacity
        self.best_sol = None #den kserw an xreiazetai

    def improve(self):
        #self.TestSolution()
        self.local_search(2)
        print("IMPROVED")
        self.sol.report_solution()

    def local_search(self, operator):

        # self.best_sol = self.sol.clone_solution(self.allNodes[0], self.capacity)
        # print("CLONED")
        # self.best_sol.report_solution()

        termination_condition = False
        local_search_iterations = 0
        
        sm_obj = Swap_move()
        rm_obj = Relocation_move()
        tOpt_obj = TwoOpt_move()

        while termination_condition is False:
            rm_obj.initialise_again()
            sm_obj.initialise_again()
            tOpt_obj.initialise_again()
            #SolDrawer.draw(local_search_iterations, self.sol, self.allNodes)
            
            #Relocations
            if operator == 0:
                self.find_best_relocation_move(rm_obj)
                if rm_obj.origin_rt_pos is not None:
                    if rm_obj.move_cost_difference <0:
                        self.apply_relocation_move(rm_obj)
                    else:
                        termination_condition = True
            #Swaps
            elif operator == 1:
                self.find_best_swap_move(sm_obj)
                if sm_obj.origin_rt_pos is not None:
                    if sm_obj.move_cost_difference < 0:
                        self.apply_swap_move(sm_obj)
                    else:
                        termination_condition = True
            #Two_Opt
            elif operator == 2:
                self.find_best_two_opt(tOpt_obj)
                if tOpt_obj.origin_rt_pos is not None:
                    if tOpt_obj.move_cost_difference < 0:
                        self.apply_two_opt_move(tOpt_obj)
                    else:
                        termination_condition = True

            local_search_iterations += 1
            print("iterations:",local_search_iterations, self.sol.cost) #extra mia epanalipsi gia na vgei
        #print(local_search_iterations, self.sol.cost)

            # if self.TestSolution() > 0:
            #     print("PROBLEM")

            #     termination_condition = True
            # else:
            #     print("Test passed")

        #     if (self.sol.cost < self.best_sol.cost):
        #         self.best_sol = self.sol.clone_solution(self.allNodes[0], self.capacity)
        # self.sol = self.best_sol

    def find_best_two_opt(self, tOpt_obj):
        for rt1_index in range(len(self.sol.routes)):
            origin_rt = self.sol.routes[rt1_index]
            for rt2_index in range(len(self.sol.routes)):
                target_rt = self.sol.routes[rt2_index]
                rt1_time_cost_so_far = 0
                rt1_calc_cost_so_far = 0
                rt1_load_so_far = 0              
                
                for node1_index_in_origin_rt in range(len(origin_rt.nodes_sequence)-1):
                    if node1_index_in_origin_rt != 0:
                        node1 = origin_rt.nodes_sequence[node1_index_in_origin_rt - 1]
                        node2 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                        cost_from_1_to_2 = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
                        rt1_time_cost_so_far += cost_from_1_to_2
                        rt1_calc_cost_so_far += rt1_time_cost_so_far
                        rt1_load_so_far += node2.demand

                    rt2_time_cost_so_far = 0
                    rt2_calc_cost_so_far = 0
                    rt2_load_so_far = 0                                       
                    start_node2_index = 0
                    if rt1_index == rt2_index:
                        start_node2_index = node1_index_in_origin_rt + 2
                    for node2_index_in_target_rt in range(start_node2_index, len(target_rt.nodes_sequence)-1):
                        if node2_index_in_target_rt != 0:
                            node11 = target_rt.nodes_sequence[node2_index_in_target_rt - 1]
                            node22 = target_rt.nodes_sequence[node2_index_in_target_rt]
                            cost_from_11_to_22 = self.cost_matrix[node11.id][node22.id] + node22.uploading_time
                            rt2_time_cost_so_far += cost_from_11_to_22
                            rt2_calc_cost_so_far += rt2_time_cost_so_far
                            rt2_load_so_far += node22.demand


                        s1 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                        n1 = origin_rt.nodes_sequence[node1_index_in_origin_rt + 1]
                        cost_multiplier1 = len(origin_rt.nodes_sequence) - node1_index_in_origin_rt
                                                
                        s2 = target_rt.nodes_sequence[node2_index_in_target_rt ]
                        n2 = target_rt.nodes_sequence[node2_index_in_target_rt + 1]
                        cost_multiplier2 = len(target_rt.nodes_sequence) - node2_index_in_target_rt

                        if origin_rt == target_rt:
                            rt1_new_load, changed_rt1 = 0, 0
                            rt2_new_load, changed_rt2 = 0, 0
                            if node1_index_in_origin_rt and node2_index_in_target_rt == len(origin_rt.nodes_sequence) - 1:
                                continue
                            
                            cost_removed_rt2, cost_added_rt2 = 0, 0
                            cost_removed_rt1 = (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id] + (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added_rt1 = (cost_multiplier1-1) * self.cost_matrix[s1.id][s2.id] + (cost_multiplier2-1) * self.cost_matrix[n1.id][n2.id]

                            minus_multiplier = 1
                            for i in range(node1_index_in_origin_rt + 1, node2_index_in_target_rt):
                                node1 = origin_rt.nodes_sequence[i]
                                node2 = origin_rt.nodes_sequence[i+1]
                                cost_removed_rt1 += (cost_multiplier1-minus_multiplier) * self.cost_matrix[node1.id][node2.id]
                                minus_multiplier += 1

                            adder_multiplier = cost_multiplier1 - 1
                            for i in range(node2_index_in_target_rt, node1_index_in_origin_rt + 1, -1):
                                node1 = origin_rt.nodes_sequence[i]
                                node2 = origin_rt.nodes_sequence[i-1]
                                cost_added_rt1 += (adder_multiplier) * self.cost_matrix[node1.id][node2.id]
                                adder_multiplier -= 1
                        else:
                            # print("CHECK0",origin_rt.cumulative_cost, rt1_calc_cost_so_far, origin_rt.cumulative_cost-rt1_calc_cost_so_far)
                            # print("CHECK0.1",target_rt.cumulative_cost, rt2_calc_cost_so_far, target_rt.cumulative_cost-rt2_calc_cost_so_far)
                            
                            origin_rt_load_second_segment = origin_rt.load - rt1_load_so_far
                            target_rt_load_second_segment = target_rt.load - rt2_load_so_far
                            rt1_new_load = rt1_load_so_far + target_rt_load_second_segment
                            rt2_new_load = rt2_load_so_far + origin_rt_load_second_segment
                            #print("loads1", origin_rt.load, rt1_load_so_far, origin_rt_load_second_segment)
                            #print("loads2", target_rt.load, rt2_load_so_far, target_rt_load_second_segment)
                            if rt1_new_load > self.capacity:
                                continue
                            if rt2_new_load > self.capacity:
                                continue
                            

                            #print("TEST IF CORRECT LOAD, myLoad, functionLoad", rt2_load_so_far, self.calculate_loadSoFar_until_nodeIndex_for_route(target_rt,node2_index_in_target_rt) )
                            #rt1_load_so_far CORRECT
                            #rt2_load_so_far CORRECT

                            #print("TEST IF CORRECT TIME COST, myCost, functionCost", rt2_time_cost_so_far, self.calculate_timeCostSoFar_until_nodeIndex_for_route(target_rt,node2_index_in_target_rt) )
                            #rt1_time_cost_so_far CORRECT
                            #rt2_time_cost_so_far CORRECT

                            origin_rt_length_second_segment = 1
                            time_cost1 = 0
                            origin_rt_calc_cost_second_segment = 0
                            for i in range(node1_index_in_origin_rt + 1, len(origin_rt.nodes_sequence)-1):
                                temp_node1 = origin_rt.nodes_sequence[i]
                                temp_node2 = origin_rt.nodes_sequence[i+1]                                
                                time_cost1 += self.cost_matrix[temp_node1.id][temp_node2.id] + temp_node2.uploading_time
                                origin_rt_calc_cost_second_segment += time_cost1
                                origin_rt_length_second_segment += 1

                            target_rt_length_second_segment = 1                            
                            time_cost2 = 0
                            target_rt_calc_cost_second_segment = 0 
                            for i in range(node2_index_in_target_rt + 1, len(target_rt.nodes_sequence)-1):
                                temp_node11 = target_rt.nodes_sequence[i]
                                temp_node22 = target_rt.nodes_sequence[i+1]                                
                                time_cost2 += self.cost_matrix[temp_node11.id][temp_node22.id] + temp_node22.uploading_time
                                target_rt_calc_cost_second_segment += time_cost2
                                target_rt_length_second_segment += 1

                            #print("TEST IF CORRECT 2nd_segment_cCost, myCost, functionCost", target_rt_calc_cost_second_segment, self.calculate_cumulativeCost_from_nodeIndex_until_end_of_route(target_rt, node2_index_in_target_rt + 1))
                            #rt1_2nd_segment_cCost CORRECT
                            #rt2_2nd_segment_cCost CORRECT

                            #route1 + route2_secondSegment                                                                                    
                            cost_removed_rt1 = origin_rt_calc_cost_second_segment
                            cost_removed_rt1 += (cost_multiplier1 - 1) * (self.cost_matrix[s1.id][n1.id] + n1.uploading_time)

                            cost_added_rt1 = (cost_multiplier2 - 1) * (self.cost_matrix[s1.id][n2.id] + n2.uploading_time)
                            cost_added_rt1 += target_rt_calc_cost_second_segment

                                                        
                            changed_rt1 = (cost_multiplier2-cost_multiplier1) * rt1_time_cost_so_far
                            changed_rt2 = (cost_multiplier1 - cost_multiplier2) * rt2_time_cost_so_far

                            #route2 + route1_secondSegment
                            cost_removed_rt2 = target_rt_calc_cost_second_segment
                            cost_removed_rt2 += (cost_multiplier2 - 1) * (self.cost_matrix[s2.id][n2.id] + n2.uploading_time)

                            cost_added_rt2 = (cost_multiplier1 - 1) * (self.cost_matrix[s2.id][n1.id] + n1.uploading_time)
                            cost_added_rt2 += origin_rt_calc_cost_second_segment

                                                       
                            #print("CHECK1",cost_added_rt1, cost_added_rt2, cost_removed_rt1, cost_removed_rt2, cost_added_rt1+cost_added_rt2-(cost_removed_rt1+cost_removed_rt2))
                            #print("CHECK2", cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2) )

                        cost_change_origin_rt = cost_added_rt1 - cost_removed_rt1 + changed_rt1
                        cost_change_target_rt = cost_added_rt2 - cost_removed_rt2 + changed_rt2
                        total_move_cost_differce = cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2) + changed_rt1 + changed_rt2

                        if total_move_cost_differce < tOpt_obj.move_cost_difference:
                            tOpt_obj.origin_rt_pos = rt1_index
                            tOpt_obj.target_rt_pos = rt2_index
                            tOpt_obj.origin_node_pos = node1_index_in_origin_rt
                            tOpt_obj.target_node_pos = node2_index_in_target_rt
                            tOpt_obj.cost_change_origin_rt = cost_change_origin_rt
                            tOpt_obj.cost_change_target_rt = cost_change_target_rt
                            tOpt_obj.origin_rt_new_load = rt1_new_load
                            tOpt_obj.target_rt_new_load = rt2_new_load
                            tOpt_obj.move_cost_difference = total_move_cost_differce

    def apply_two_opt_move(self, tOpt_obj):
        origin_route = self.sol.routes[tOpt_obj.origin_rt_pos]
        target_route = self.sol.routes[tOpt_obj.target_rt_pos]
        
        if origin_route == target_route:
            reversed_segment = reversed(origin_route.nodes_sequence[tOpt_obj.origin_node_pos + 1: tOpt_obj.target_node_pos + 1])
            origin_route.nodes_sequence[tOpt_obj.origin_node_pos + 1 : tOpt_obj.target_node_pos + 1] = reversed_segment
            origin_route.cumulative_cost += tOpt_obj.cost_change_origin_rt
        else:
            #self.calculate_route_details("origin_route_before",origin_route, tOpt_obj.origin_rt_pos + 1 )
            #self.calculate_route_details("target_route_before",target_route, tOpt_obj.target_rt_pos + 1)
            relocatedSegmentOfRt1 = origin_route.nodes_sequence[tOpt_obj.origin_node_pos + 1 :]
            relocatedSegmentOfRt2 = target_route.nodes_sequence[tOpt_obj.target_node_pos + 1 :]
            del origin_route.nodes_sequence[tOpt_obj.origin_node_pos + 1 :]
            del target_route.nodes_sequence[tOpt_obj.target_node_pos + 1 :]
            origin_route.nodes_sequence.extend(relocatedSegmentOfRt2)
            target_route.nodes_sequence.extend(relocatedSegmentOfRt1)
            origin_route.load = tOpt_obj.origin_rt_new_load
            target_route.load = tOpt_obj.target_rt_new_load
            origin_route.cumulative_cost += tOpt_obj.cost_change_origin_rt
            target_route.cumulative_cost += tOpt_obj.cost_change_target_rt
            #self.calculate_route_details("origin_route_after",origin_route, tOpt_obj.origin_rt_pos + 1)
            #self.calculate_route_details("target_route_after",target_route, tOpt_obj.target_rt_pos + 1)
 

        self.sol.cost += tOpt_obj.move_cost_difference

    def calculate_route_details(self,message,route, route_pos):
        load = 0
        timecost = 0
        calccost = 0
        numberOfNodes = 0
        nodes_in_route = [0]
        for i in range(0, len(route.nodes_sequence)-1):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            dist_cost = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
            timecost += dist_cost
            calccost += timecost
            load += node2.demand
            numberOfNodes += 1
            nodes_in_route.append(node2.id)
        print()
        print("ROUTEDETAILS:",route_pos, message,"calcCost, nodes_in_route, numberOfNodes", calccost, nodes_in_route, numberOfNodes)
        print()

    def calculate_timeCostSoFar_until_nodeIndex_for_route(self, route, node_index_in_route):
        timecost = 0
        for i in range(0, node_index_in_route):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            dist_cost = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
            timecost += dist_cost
        return timecost
    
    def calculate_loadSoFar_until_nodeIndex_for_route(self, route, node_index_in_route):
        load = 0
        for i in range(0, node_index_in_route):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            load += node2.demand
        return load
    
    def calculate_cumulativeCost_from_nodeIndex_until_end_of_route(self, route, node_index_in_route):
        tCost = 0
        cCost = 0
        for i in range(node_index_in_route, len(route.nodes_sequence)-1):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            dist_cost = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
            tCost += dist_cost
            cCost += tCost
        return cCost

    

    def find_best_swap_move(self, sm_obj):
        for rt1_index in range(len(self.sol.routes)):
            origin_rt = self.sol.routes[rt1_index]
            for rt2_index in range(len(self.sol.routes)): #mallon ksekinaw apo rt1_index
                target_rt = self.sol.routes[rt2_index]
                for node1_index_in_route in range(1, len(origin_rt.nodes_sequence)):
                    #node2_index_in_route = 1
                    start_node2_index = 1
                    if origin_rt == target_rt:
                        start_node2_index = node1_index_in_route + 1
                    for node2_index_in_route in range(start_node2_index, len(target_rt.nodes_sequence)):

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

    def find_best_relocation_move(self, rm_obj):
        for rt1_index in range(len(self.sol.routes)):
            origin_rt = self.sol.routes[rt1_index]
            time_so_far_in_origin_rt = 0
            for node1_index_in_origin_rt in range(1, len(origin_rt.nodes_sequence)):
                #xreiazontai gia ton upologismo tou time_so_far
                prev_node_rt1 = origin_rt.nodes_sequence[node1_index_in_origin_rt-1]
                node_rt1 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                time_so_far_in_origin_rt += self.cost_matrix[prev_node_rt1.id][node_rt1.id] + node_rt1.uploading_time
                
                for rt2_index in range(len(self.sol.routes)):
                    target_rt = self.sol.routes[rt2_index]
                    time_so_far_in_target_rt = 0
                    for node2_index_in_target_rt in range(1,len(target_rt.nodes_sequence)):
                        #xreiazontai gia ton upologismo tou time_so_far
                        prev_node_rt2 = target_rt.nodes_sequence[node2_index_in_target_rt-1]
                        node_rt2 = target_rt.nodes_sequence[node2_index_in_target_rt]
                        time_so_far_in_target_rt += self.cost_matrix[prev_node_rt2.id][node_rt2.id] + node_rt2.uploading_time
                    

                        if origin_rt == target_rt and (node1_index_in_origin_rt==node2_index_in_target_rt or node1_index_in_origin_rt-1==node2_index_in_target_rt):
                            continue

                        #Origin route Info
                        is_last1 = (len(origin_rt.nodes_sequence)-node1_index_in_origin_rt-1) == 0
                        p1 = origin_rt.nodes_sequence[node1_index_in_origin_rt - 1] #previous
                        s1 = origin_rt.nodes_sequence[node1_index_in_origin_rt] #selected
                        if is_last1 is False:
                            n1 = origin_rt.nodes_sequence[node1_index_in_origin_rt + 1] #next
                        cost_multiplier1 = len(origin_rt.nodes_sequence) - node1_index_in_origin_rt

                        #Target route info
                        is_last2 = (len(target_rt.nodes_sequence)-node2_index_in_target_rt-1) == 0
                        s2 = target_rt.nodes_sequence[node2_index_in_target_rt]
                        if is_last2 is False:
                            n2 = target_rt.nodes_sequence[node2_index_in_target_rt + 1]
                        cost_multiplier2 = len(target_rt.nodes_sequence) - node2_index_in_target_rt

                        total_move_cost_differce = None
                        origin_route_cost_difference = None
                        target_route_cost_difference = None

                        if origin_rt == target_rt:                          
                            cost_added_rt2, cost_removed_rt2 = 0, 0
                            if node2_index_in_target_rt > node1_index_in_origin_rt:
                                inclusive_time_from_s1_to_s2 = 0
                                for i in range(node1_index_in_origin_rt +1, node2_index_in_target_rt):
                                    node1 = origin_rt.nodes_sequence[i]
                                    node2 = origin_rt.nodes_sequence[i+1]
                                    inclusive_time_from_s1_to_s2 += self.cost_matrix[node1.id][node2.id] + node1.uploading_time

                                cost_removed_rt1 = cost_multiplier1 * self.cost_matrix[p1.id][s1.id]
                                cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]
                                cost_removed_rt1 += (cost_multiplier1 - cost_multiplier2) * s1.uploading_time
                                cost_added_rt1 = cost_multiplier1 * self.cost_matrix[p1.id][n1.id]
                                cost_added_rt1 += cost_multiplier2 * self.cost_matrix[s2.id][s1.id]
                                cost_added_rt1 += inclusive_time_from_s1_to_s2
                                cost_added_rt1 += s2.uploading_time
                                if is_last2 is False:
                                    cost_added_rt1 += (cost_multiplier2-1) * self.cost_matrix[s1.id][n2.id]
                                    cost_removed_rt1 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            else:
                                inclusive_time_from_s2_to_s1 = 0
                                for i in range(node2_index_in_target_rt +1, node1_index_in_origin_rt - 1):
                                    node1 = origin_rt.nodes_sequence[i]
                                    node2 = origin_rt.nodes_sequence[i+1]
                                    inclusive_time_from_s2_to_s1 += self.cost_matrix[node1.id][node2.id] + node1.uploading_time
                                inclusive_time_from_s2_to_s1 += p1.uploading_time
                                                                
                                cost_removed_rt1 = cost_multiplier1 * self.cost_matrix[p1.id][s1.id]
                                cost_removed_rt1 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                                cost_removed_rt1 += inclusive_time_from_s2_to_s1
                                cost_added_rt1 = (cost_multiplier2-1) * self.cost_matrix[s2.id][s1.id]
                                cost_added_rt1 += (cost_multiplier2-2) * self.cost_matrix[s1.id][n2.id]
                                cost_added_rt1 += (cost_multiplier2 - 1 - cost_multiplier1) * s1.uploading_time
                                if is_last1 is False:
                                    cost_added_rt1 += (cost_multiplier1-1) * self.cost_matrix[p1.id][n1.id]
                                    cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]                                
                        else:
                            if target_rt.load + s1.demand > origin_rt.capacity:
                                continue

                            if is_last1 is True:
                                cost_removed_rt1 = time_so_far_in_origin_rt
                                cost_added_rt1 = 0
                            elif is_last2 is False:
                                cost_removed_rt1 = time_so_far_in_origin_rt
                                cost_removed_rt1 += (cost_multiplier1-1) * (self.cost_matrix[p1.id][s1.id] + s1.uploading_time)
                                cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]
                                cost_added_rt1 = (cost_multiplier1-1) * self.cost_matrix[p1.id][n1.id]

                            if is_last2 is True:
                                cost_removed_rt2 = 0
                                cost_added_rt2 = cost_multiplier2 * (self.cost_matrix[s2.id][s1.id] + s1.uploading_time)
                                cost_added_rt2 += time_so_far_in_target_rt
                            elif is_last2 is False:
                                cost_removed_rt2 = (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                                cost_added_rt2 = time_so_far_in_target_rt
                                cost_added_rt2 += cost_multiplier2 * (self.cost_matrix[s2.id][s1.id] + s1.uploading_time)
                                cost_added_rt2 += (cost_multiplier2-1) * self.cost_matrix[s1.id][n2.id]

                        origin_route_cost_difference = cost_added_rt1 - cost_removed_rt1
                        target_route_cost_difference = cost_added_rt2 - cost_removed_rt2
                        total_move_cost_differce = cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2)

                        if total_move_cost_differce < rm_obj.move_cost_difference:
                            rm_obj.origin_rt_pos = rt1_index
                            rm_obj.target_rt_pos = rt2_index
                            rm_obj.origin_node_pos = node1_index_in_origin_rt
                            rm_obj.target_node_pos = node2_index_in_target_rt
                            rm_obj.cost_change_origin_rt = origin_route_cost_difference
                            rm_obj.cost_change_target_rt = target_route_cost_difference
                            rm_obj.move_cost_difference = total_move_cost_differce

    def apply_relocation_move(self, rm_obj):

        origin_route = self.sol.routes[rm_obj.origin_rt_pos]
        target_route = self.sol.routes[rm_obj.target_rt_pos]
        selected_node1 = origin_route.nodes_sequence[rm_obj.origin_node_pos]

        if origin_route == target_route:
            del origin_route.nodes_sequence[rm_obj.origin_node_pos]
            if (rm_obj.origin_node_pos < rm_obj.target_node_pos):
                target_route.nodes_sequence.insert(rm_obj.target_node_pos, selected_node1)
            else:
                target_route.nodes_sequence.insert(rm_obj.target_node_pos + 1, selected_node1) #den vrike gia seed=39, vrike gia seed=3, swsto me +1 gia origin_node_pos > target_node_pos

            origin_route.cumulative_cost += rm_obj.move_cost_difference        
        else:
            del origin_route.nodes_sequence[rm_obj.origin_node_pos]
            target_route.nodes_sequence.insert(rm_obj.target_node_pos + 1, selected_node1)
            origin_route.cumulative_cost += rm_obj.cost_change_origin_rt
            target_route.cumulative_cost += rm_obj.cost_change_target_rt
            origin_route.load -= selected_node1.demand
            target_route.load += selected_node1.demand

        self.sol.cost += rm_obj.move_cost_difference
        #print(f"moved from route:{rm_obj.origin_rt_pos} to {rm_obj.target_rt_pos}: node{selected_node1.id} to pos: {rm_obj.target_node_pos + 1}")

################
    def TestSolution(self):
        failed_test = 0
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
                print(r+1, calc_rtCost, route.cumulative_cost)
                print ('Route Cost problem')
                failed_test += 1
            if calc_rtLoad != route.load:
                #print(r, calc_rtLoad, route.load)
                print ('Route Load problem')
                failed_test += 1
            
            totalSolCost += route.cumulative_cost
        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')
        return failed_test