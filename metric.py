# -*- coding: utf-8 -*-

from agents import CP
from typing import List, Dict, Tuple
import time

def time_function_call(func, *args, **kwargs):
    start_time = time.time()
    matched_s, matched_c = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    return elapsed_time, matched_s, matched_c

def charging_analysis(cp_list: List[CP], matched_c: Dict[int, List[Tuple[int, int, float, int]]]):
    """

    Parameters
    ----------
    cp_list : List[CP]
    matched_c : Dict[int, List[Tuple[int, int, float, int]]]
        key is CP ID. Each value is list of tuples (s_i, t1_ij, psi_ij, delta_ij) 
    Returns
    -------

    """
    innet_cp = [] # in-network CP
    outnet_cp = [] # par-network CP
    total_ct_in = 0 # total in-net charge transferred
    wait_time_list = [] # wait time list for all in-net EV 
    total_s = 0 # total EV charged in-net
    total_SLA_breach = 0
    for c in cp_list:
        if c.eta == 0:
            innet_cp.append(c.ID)
        else:
            outnet_cp.append(c.ID)
    for c_id in innet_cp:
        t_w_c_id = 0 # total wait time at c_id
        A_c = matched_c[c_id]
        total_s = total_s + len(A_c)
        for s in A_c:
            t1_ij = s[1] # charging time
            wait_time_list.append(t_w_c_id)
            if t_w_c_id + t1_ij > s[3]:
                total_SLA_breach = total_SLA_breach + 1
            total_ct_in = total_ct_in + s[2] # s[2] = psi_ij
            t_w_c_id = t_w_c_id + t1_ij # wait time for the next EV in the queue
    
    total_s_out = 0
    wait_time_list_out = [] # wait time list for all in-net EV        
    total_ct_out = 0
    for c_id in outnet_cp:
        t_w_c_id = 0 # total wait time at c_id
        A_c = matched_c[c_id]
        total_s_out = total_s_out + len(A_c)
        for s in A_c:
            t1_ij = s[1] # charging time
            wait_time_list_out.append(t_w_c_id)
            if t_w_c_id + t1_ij > s[3]:
                total_SLA_breach = total_SLA_breach + 1
            total_ct_out = total_ct_out + s[2] # s[2] = psi_ij
            t_w_c_id = t_w_c_id + t1_ij # wait time for the next EV in the queue
            
    
    print("*** METRICS ****")
    print(":: Total in-net CP = ", len(innet_cp))
    print("Total EV charged in-net = ", total_s)
    print("Total charge transferred in-net = ", total_ct_in)
    #print("In-net wait-time list = ", wait_time_list)
    
    print(":: Total par-net CP = ", len(outnet_cp))
    print("Total EV charged par-net = ", total_s_out)
    print("Total charge transferred par-net = ", total_ct_out)
    #print("par-net wait-time list = ", wait_time_list_out)
    print("Total SLA breach = ", total_SLA_breach)
    return (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach)
    
def find_unmatched(matched_s):
    unmatched = 0
    for s_id in matched_s.keys():
        if matched_s[s_id] == []:
            unmatched = unmatched + 1
    return unmatched

def find_distribution_CP(matched_c: Dict[int, List[Tuple[int, int, float, int]]]):
    """

    Parameters
    ----------
    matched_c : Dict[int, List[Tuple[int, int, float, int]]]
        key is CP ID. Each value is list of tuples (s_i, t1_ij, psi_ij, delta_ij) 
    Returns
    -------

    """
    ev_assigned_per_cp = [] # list of number of EV assigned to each CP (distribution)
    charge_transferred_per_cp = [] # list of number of EV assigned to each CP (distribution)
    for c_i in matched_c.keys():
        assigned_evs_at_j = matched_c[c_i]
        ev_assigned_per_cp.append(len(assigned_evs_at_j))
        if len(assigned_evs_at_j) == 0:
            charge_transferred_per_cp.append(0)
        else:
            psi_ij = 0
            for s in assigned_evs_at_j: # s = (s_i, t1_ij, psi_ij, delta_ij) 
                psi_ij = psi_ij + s[2]
            charge_transferred_per_cp.append(psi_ij)
    return ev_assigned_per_cp, charge_transferred_per_cp
            