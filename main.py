# from agents import EV, CP
from matching_at_RSU import match, randomChoice, PCG, PCD
from metric import charging_analysis, find_unmatched, find_distribution_CP
from helper import create_EVobjects, create_CPobjects, debug_print
import time
import random
import csv
from plot import plot_varyingEV


time_seed = time.time()
random.seed(time_seed)
Debug = False


if __name__ == "__main__":
    # 8 block = 1 mile (Chicago)
    # RSU radius is 1.5 mile = 12 blocks
    # The largest square that can fit in RSU area will have 12*sqrt(2) = 16.97 blocks
    # Let us consider the grid size 16 X 16
   
    # # user input
    n_ev = 30
    n_cp_in_fast = 5
    n_cp_in_regular = 10
    n_cp_out_fast = 5
    n_cp_out_regular = 10
    q = 4 # quota of each CP
    csv_file = 'resultsTest.csv'
    
    # Initialize Charging points (Static for the whole experiment)
    start_id = 0
    cp_in_fast = create_CPobjects(n_cp_in_fast, start_id=start_id, theta=1, eta=0, q=q) # in-net fast charging points
    start_id = start_id + n_cp_in_fast
    cp_in_regular = create_CPobjects(n_cp_in_regular, start_id=start_id, theta=0, eta=0, q=q) # in-net regular charging points
    start_id = start_id + n_cp_in_regular
    cp_out_fast = create_CPobjects(n_cp_out_fast, start_id=start_id, theta=1, eta=1, q=q) # in-net fast charging points
    start_id = start_id + n_cp_out_fast
    cp_out_regular = create_CPobjects(n_cp_out_regular, start_id=start_id, theta=0, eta=1, q=q) # in-net fast charging points
    cp_list = cp_in_fast + cp_in_regular + cp_out_fast + cp_out_regular
    
    

    # Initialize EVs
    ev_list = create_EVobjects(n_ev, start_id=0) # create list of EVs
    # # Print the sorted EV list
    # print(sorted_ev_list)
    # print("List of EV:")
    # print(ev_list)
    
    # compute preference list for EV
    Pref = {}
    #print("Preference list of EV (CP ID, Distance d_ij, time to reach t0_ij, psi, r_i, gamma):")
    for ev in ev_list:
        ev.compute_preference(cp_list)
        Pref[ev.ID] = ev.pref
        #print(ev.ID, " => ", ev.pref)
    
    
    print("\n***Method: Random***")
    print("-----------------------------------------")
    start_time = time.time()
    matched_s, matched_c = match(ev_list, cp_list, Pref, randomChoice)
    end_time = time.time()
    elapsed_time_random = (end_time - start_time) * 1000
    results_random = charging_analysis(cp_list, matched_c) # returns (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach)
    unmatched_random = find_unmatched(matched_s)
    debug_print(Debug, f"Elapsed time: {elapsed_time_random} ms")
    debug_print(Debug, "Matching for EV:")
    debug_print(Debug, f"{matched_s}")
    debug_print(Debug, "Matching for CP:")
    debug_print(Debug, f"{matched_c}")
    debug_print(Debug, f"No. of unmatched EV: {unmatched_random}")
    ev_assigned_per_cp, charge_transferred_per_cp = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp)
    
    print("\n***Method: PCG***")
    print("-----------------------------------------")
    #matched_s, matched_c, elapsed_time = time_function_call(match, ev_list, cp_list, Pref, PCG)
    #print("Elapsed time: ", elapsed_time, " ms")
    start_time = time.time()
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCG)
    end_time = time.time()
    elapsed_time_PCG = (end_time - start_time) * 1000
    results_PCG = charging_analysis(cp_list, matched_c)
    unmatched_PCG = find_unmatched(matched_s)
    debug_print(Debug, f"Elapsed time: {elapsed_time_PCG} ms")
    debug_print(Debug, "Matching for EV:")
    debug_print(Debug, f"{matched_s}")
    debug_print(Debug, "Matching for CP:")
    debug_print(Debug, f"{matched_c}")
    debug_print(Debug, f"No. of unmatched EV: {unmatched_PCG}")
    ev_assigned_per_cp, charge_transferred_per_cp = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp)
    
    print("\n***Method: PCD***")
    print("-----------------------------------------")
    start_time = time.time()
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCD)
    end_time = time.time()
    elapsed_time_PCD = (end_time - start_time) * 1000
    results_PCD = charging_analysis(cp_list, matched_c)
    unmatched_PCD = find_unmatched(matched_s)
    debug_print(Debug, f"Elapsed time: {elapsed_time_PCD} ms")
    debug_print(Debug, "Matching for EV:")
    debug_print(Debug, f"{matched_s}")
    debug_print(Debug, "Matching for CP:")
    debug_print(Debug, f"{matched_c}")
    debug_print(Debug, f"No. of unmatched EV: {unmatched_PCD}")
    ev_assigned_per_cp, charge_transferred_per_cp = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp)
    
    # file_exists = os.path.isfile(csv_file)
    # with open(csv_file, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    
    #     # Write the header only if the file doesn't exist
    #     if not file_exists:
    #         writer.writerow(['Method', 'Total EV', 'CP Queue', 'Total in-net CP', 'Total par-net CP', 'Total EV charged in-net', 'Total EV charged par-net','Total charge transferred in-net',
    #                            'Total charge transferred par-net', 'Total SLA breach', 'unmatched EV', "execution time"])
        
    #     # results_random = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach)
    #     writer.writerow(['random_elemination', n_ev, q, results_random[0], results_random[1], results_random[2], results_random[3], results_random[4], results_random[5], results_random[6], unmatched_random, elapsed_time_random])  
        
    #     # results_PCG = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach)
    #     writer.writerow(['PCG', n_ev, q, results_PCG[0], results_PCG[1], results_PCG[2], results_PCG[3], results_PCG[4], results_PCG[5], results_PCG[6], unmatched_PCG, elapsed_time_PCG]) 
        
    #     # results_PCD = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach)
    #     writer.writerow(['PCD', n_ev, q, results_PCD[0], results_PCD[1], results_PCD[2], results_PCD[3], results_PCD[4], results_PCD[5], results_PCD[6], unmatched_PCD, elapsed_time_PCD]) 



    
    
  