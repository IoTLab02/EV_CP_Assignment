# -*- coding: utf-8 -*-

import math
import random
import time


time_seed = time.time()
random.seed(time_seed)

def compute_euclidean_distance(x_i,y_i,x_j,y_j):
    distance = math.sqrt((x_j - x_i) ** 2 + (y_j - y_i) ** 2)
    return distance

def compute_manhattan_distance(x_i, y_i, x_j, y_j):
    distance = abs(x_j - x_i) + abs(y_j - y_i)
    dist_miles = distance * 0.125 # In Chicago 8 blocks is 1 mile
    return dist_miles

class EV:
    """
    Electric Vehicle (EV) class

    Attributes:
        ID (int): Unique identifier for the EV.
        x_loc (int): X-coordinate location of the EV.
        y_loc (int): Y-coordinate location of the EV.
        r_i (int): Charge acceptance rate of the EV. Default: 2 kWh per min.
        v_i (float): average velocity of the EV. Default: 0.5 mile per min => 30 mph 
        alpha (0 < alpha <= 1): Minimum fraction of total battery charge s_i 
            desires to attain when leaving a CP. Default: 0.8
        B_full (int): Battery capacity of the EV. Default: 60 kWh
        fast (int): Fast charging quota left in kWh
        B_res (int): Residual battery (B_i^0) in kWh. 
            Default: a random value between 10 and 36 (60% of B_full)
        gamma (int): waiting time as per SLA
        m (int): mileage of the EV in miles per kWh. 
            Default: 3 or 4 miles per kWh.
        psi_ij (list of int): Charge requirement associated with the EV s_i 
            if it goes to CP c_j.
        t0_ij (list of int): Time to reach CP c_j from the 
            current location of s_i.
        pref (list of int): List of CP preferences.

    Methods:
        compute_preference(cp_list): 
    """
    def __init__(self, ID, x_loc, y_loc, r_i=2, v_i=0.5, alpha=0.8, B_full=60, fast=None, gamma=None, B_res=None, m=None, psi_ij=None, t0_ij=None, pref=None):
        self.ID = ID
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.r_i = r_i
        self.v_i = v_i
        self.alpha = alpha
        self.B_full = B_full
        self.fast = fast if fast is not None else random.randint(0,60) 
        possible_gammas = [i for i in range(5, 25 + 1) if i % 5 == 0] # gamma value depends on the subscription. We are taking it random
        self.gamma = gamma if gamma is not None else random.choice(possible_gammas)
        #self.B_res = B_res if B_res is not None else random.randint(20,B_full * self.alpha)
        self.B_res = B_res if B_res is not None else random.randint(10,37) # considering the residual charge to be below 60% of the full battery
        self.m = m if m is not None else random.randint(3,5)
        self.psi_ij = psi_ij if psi_ij is not None else []
        self.t0_ij = t0_ij if t0_ij is not None else []
        self.pref = pref if pref is not None else []

    def __repr__(self):
        return f'EV(ID={self.ID}, x_loc={self.x_loc}, y_loc={self.y_loc}, r_i={self.r_i}, alpha={self.alpha}, B_full={self.B_full}, fast={self.fast}, gamma={self.gamma}, B_res={self.B_res}, m={self.m}, psi_ij={self.psi_ij}, t0_ij={self.t0_ij}, pref={self.pref}\n)'


    # def request_CP_loc(self, o_rsu):
    #     o_rsu.receive(self.x_loc, self.y_loc) # EV sends its location to RSU
    
    def compute_preference(self, cp_list):
        fast_charging_in_cp_list = [cp for cp in cp_list if (cp.theta == 1 and cp.eta==0)]
        fast_charging_out_cp_list = [cp for cp in cp_list if (cp.theta == 1 and cp.eta==1)]
        regular_charging_in_cp_list = [cp for cp in cp_list if (cp.theta == 0 and cp.eta==0)]
        regular_charging_out_cp_list = [cp for cp in cp_list if (cp.theta == 0 and cp.eta==1)]
        CP_types = [fast_charging_in_cp_list, regular_charging_in_cp_list, fast_charging_out_cp_list, regular_charging_out_cp_list]
        
        charge_desired = self.alpha * self.B_full
        for CP_type in CP_types:
            temp = []
            for c_j in CP_type:
                dist_ij = compute_manhattan_distance(self.x_loc, self.y_loc, c_j.x_loc, c_j.y_loc)
                B_ij = self.B_res - dist_ij/self.m # remaining charge after reaching c_j
                if B_ij <= 0:
                    continue
                psi_ij = charge_desired - B_ij # effective charge requirement
                if c_j.theta == 0:
                    t0_ij = math.floor(dist_ij/ self.v_i)
                    temp.append((c_j.ID, dist_ij, t0_ij, round(psi_ij, 1), self.r_i, self.gamma)) # (c_j, d_ij, t0_ij, psi_ij, r_i, gamma_i)
                if c_j.theta == 1 and self.fast > psi_ij:
                    t0_ij = math.floor(dist_ij/ self.v_i)
                    temp.append((c_j.ID, dist_ij, t0_ij, round(psi_ij, 1), self.r_i, self.gamma)) # (c_j, d_ij, t0_ij, psi_ij, r_i, gamma_i)
            sorted_temp = sorted(temp, key=lambda x: x[1]) # sort based on distance or deviation 
            if len(sorted_temp) != 0:
                self.pref.extend(sorted_temp)
        return self.pref
        
        
        
class CP:
    """
    Charging Point (CP) class

    Attributes:
        ID (int): Unique identifier for the CP.
        x_loc (int): X-coordinate location of the CP.
        y_loc (int): Y-coordinate location of the CP.
        r_j (int): Charging rate of the EV. Default: 1 kWh per min.
        theta (bool): theta = 1 for fast and 0 for regular.
        eta (bool): eta = 0 for in-net, 1 for par-net.
        q (int): Quota for CP. How many EV can wait depends on it. Default: 2.
        t_free_j (int): Time after which c_j will be free in min. Default: 0 min.

    Methods:
        
    """
    def __init__(self, ID, x_loc, y_loc, theta, eta, q=2, r_j=1, t_free_j=0):
        self.ID = ID
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.r_j = r_j
        self.theta = theta
        self.eta = eta
        self.q = q
        self.t_free_j = t_free_j
        if(self.theta == 1): # fast charging
            self.r_j = 2
            
    def set_q(self, q):
        self.q = q
        