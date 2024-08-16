# -*- coding: utf-8 -*-
"""
# 8 block = 1 mile (Chicago)
# RSU radius is 1.5 mile = 12 blocks
# The largest square that can fit in RSU area will have 12*sqrt(2) = 16.97 blocks
# Let us consider the grid size 16 X 16
"""

# from agents import EV, CP
from matching_at_RSU import match, randomChoice, PCG, PCD
from metric import charging_analysis, find_unmatched, find_distribution_CP
from helper import create_EVobjects, create_CPobjects, debug_print
import time
import random
import csv
from plot import plot_varyingQ
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.chdir(r"C:\Phd\CUDA test\Test\test 1\V2V_charging_service\code\EV_assignment")


time_seed = time.time()
random.seed(time_seed)
Debug = True


if __name__ == "__main__":

    # # user input
    n_ev = 45
    q_range_min = 1
    q_range_max = 5
    n_cp_in_fast = 5
    n_cp_in_regular = 10
    n_cp_par_fast = 5
    n_cp_par_regular = 10
    max_itr = 20 # maximum iteration
    csv_file = 'results_varying_Q_1.csv'
    
    
    # Initialize EVs
    ev_list = create_EVobjects(n_ev, start_id=0) # create list of EVs
    
    
    q = 4     
    # Initialize Charging points (Static for the whole experiment)
    start_id = 0
    cp_in_fast = create_CPobjects(n_cp_in_fast, start_id=start_id, theta=1, eta=0, q=q) # in-net fast charging points
    start_id = start_id + n_cp_in_fast
    cp_in_regular = create_CPobjects(n_cp_in_regular, start_id=start_id, theta=0, eta=0, q=q) # in-net regular charging points
    start_id = start_id + n_cp_in_regular
    cp_par_fast = create_CPobjects(n_cp_par_fast, start_id=start_id, theta=1, eta=1, q=q) # in-net fast charging points
    start_id = start_id + n_cp_par_fast
    cp_par_regular = create_CPobjects(n_cp_par_regular, start_id=start_id, theta=0, eta=1, q=q) # in-net fast charging points
    cp_list = cp_in_fast + cp_in_regular + cp_par_fast + cp_par_regular
    
    # CP ID list (required for plotting)
    cp_id_list = [i for i in range(n_cp_in_fast + n_cp_in_regular + n_cp_par_fast + n_cp_par_regular)]
    # q_in_fast = str(q) +" in-net fast"
    # q_in_reg = str(q) +" in-net regular"
    # q_par_fast = str(q) +" par-net fast"
    # q_par_reg = str(q) +" par-net regular"
    # CP_category = [q_in_fast] * n_cp_in_fast + [q_in_reg] * n_cp_in_regular + \
                # [q_par_fast] * n_cp_par_fast + [q_par_reg] * n_cp_par_regular
    CP_category = ["in-net fast"] * n_cp_in_fast + ["in-net regular"] * n_cp_in_regular + \
                 ["par-net fast"] * n_cp_par_fast + ["par-net regular"] * n_cp_par_regular

    # compute preference list for EV
    Pref = {}
    #print("Preference list of EV (CP ID, Distance d_ij, time to reach t0_ij, psi, r_i, gamma):")
    for ev in ev_list:
        ev.compute_preference(cp_list)
        Pref[ev.ID] = ev.pref
        #print(ev.ID, " => ", ev.pref)
            
            
    print("\n***Method: Random***")
    print("-----------------------------------------")
    # start_time = time.time()
    matched_s, matched_c = match(ev_list, cp_list, Pref, randomChoice)
    ev_assigned_per_cp_rand, charge_transferred_per_cp_rand = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp_rand)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp_rand)
            
    print("\n***Method: PCG***")
    print("-----------------------------------------")
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCG)
    ev_assigned_per_cp_PCG, charge_transferred_per_cp_PCG = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp_PCG)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp_PCG)
    
    print("\n***Method: PCD***")
    print("-----------------------------------------")
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCD)
    ev_assigned_per_cp_PCD, charge_transferred_per_cp_PCD = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp_PCD)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp_PCD)
    
    
    
    # palette = sns.color_palette("rocket")
    data1 = pd.DataFrame({
        'ID': cp_id_list * 2,
        'Value': charge_transferred_per_cp_PCG + charge_transferred_per_cp_PCD,
        'Category': [category + " (PCG)" for category in CP_category] +
            [category + " (PCD)" for category in CP_category]
    })
    

    # Create the bar plot using seaborn with reduced gap between the bars
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='ID', y='Value', hue='Category', data=data1, palette="tab20")
    for patch in plt.gca().patches:
        patch.set_width(0.4)  # Adjusting bar width for data1
    plt.xlabel('Charging Point ID', fontsize=22)
    plt.ylabel('Charge Transfer (kWh)', fontsize=22)
    #plt.title('Charge Transfer per Charging Point', fontsize=18)
    plt.legend(title='Category', fontsize=14, title_fontsize=18, loc='upper right', ncol=2)
    plt.tick_params(axis='both', which='major', labelsize=16)
    #plt.xticks(xtick_values)
    plt.grid(True)
    plt.savefig(f'Charge_Distribution_n_ev{n_ev}_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    
    
    
    # palette = sns.color_palette("rocket")
    data2 = pd.DataFrame({
        'ID': cp_id_list * 2,
        'Value': ev_assigned_per_cp_PCG + ev_assigned_per_cp_PCD,
        'Category': [category + " (PCG)" for category in CP_category] +
            [category + " (PCD)" for category in CP_category]
    })
    ytick_values = data2['Value'].unique()
    
    # Create the bar plot using seaborn with reduced gap between the bars
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='ID', y='Value', hue='Category', data=data2, palette="tab20")
    for patch in plt.gca().patches:
        patch.set_width(0.4)  # Adjusting bar width for data1
    plt.xlabel('Charging Point ID', fontsize=22)
    plt.ylabel('Number of EVs', fontsize=22)
    #plt.title('EVs per Charging Point', fontsize=18)
    plt.legend(title='Category', fontsize=14, title_fontsize=18, loc='upper right', ncol=2)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.yticks(ytick_values)
    plt.grid(True)
    plt.savefig(f'EV_Distribution_n_ev{n_ev}_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    