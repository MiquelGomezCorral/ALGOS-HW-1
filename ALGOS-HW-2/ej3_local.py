# Studients:
# Catalina Regolf Cortés. SCIPER: 394019
# Miquel Gómez Corral. SCIPER: 394325

import math
import random
from grinch import OfflineANNS 

""" 
################################
          FUNCTIONS
################################
""" 

def read_first_line():
    line = input()
    d, r, c, n, N = [i for i in line.split(" ")]
    return int(d), int(r), float(c), int(n), int(N)
def read_second_line():
    line = input()
    z = [int(i) for i in line.split(" ")]
    return z

def query(q, ds):
    global N
    N -= 1
    
    a = ds.query(q)
    print(f'q {" ".join(map(str, q))}, {N = }, {a = }')
    return a

    
def print_q_star(q, ds):
    print(f'* {" ".join(map(str, q))}')
    print(ds.query(q))
    exit()
    
    
def dist_1(q, z):
    dist = 0
    for qi, zi in zip(q, z):
        if qi != zi: 
            dist += 1
            
    return dist 

def sample_q(z, r, mu, d):
    """
    Change rhs elements from z so x is at rhs distance from z 
    """
    rhs = r - mu
    x = list(z)
    
    for i in random.sample(range(d), rhs):
        x[i] = 1 - x[i]
    
    return x

def get_m(z, q):
    d = len(z)
    return [i for i in range(d) if q[i] == z[i]]
    
def find_j_div(q, I, w, ds):
    ini, end = 0, w
    mid = w // 2
    
    while ini <= end and N > 1:
        uj = get_uj(q, I, mid)
        a = query(uj, ds)
        if a[0] == -1: # return _|_
            end = mid - 1
        else: ini = mid + 1 # return z
        mid = (ini + end) // 2
        
    return mid

def find_j(q, I, w, ds):
    for j in range(1, w+1):
        uj = get_uj(q, I, j)
        a = query(uj, ds)
        if a[0] == -1 or N <= 1:
            return j-1
        
    return w-1
         
def get_uj(q, I, j):
    uj = list(q)
    for i in I[:j]:
        uj[i] = 1-q[i]
            
    return uj

def update_q(q, j):
    q[j] = 1 - q[j]
    
    
""" 
################################
         EXECUTION
################################
""" 


def algorithm(d, r, c, n, z, ds):
    mu = min(
        r,
        math.ceil(2*math.e*math.e * (math.log(n)+1))
    )
    while N > 0:
        q = sample_q(z, r, mu, d)
        dist_q_z = dist_1(q,z) 
        print(f"\nNEW Q: {q}")
        
        while N > 0 and dist_q_z < r:
            print(f"UPDATED Q: {q}")
            a = query(q, ds)
            if a[0] == -1: # first coordinate is -1 -> not found
                print_q_star(q, ds)
                
            M = get_m(z,q)
            w = math.ceil(c*r) + 1 - dist_q_z
            # I = random.sample(M, w)
            I = sorted(random.sample(M, w))
            
            j = find_j(q, I, w, ds)
            
            update_q(q,I[j])
            dist_q_z = dist_1(q,z) 
            print(f"{dist_q_z = }, {j = }")
        # End while 
        
        if N > 0 and dist_q_z <= r:
            a = query(q, ds)
            if a[0] == -1: # first coordinate is -1 -> not found
                print_q_star(q, ds)
        
    print_q_star(q, ds)
    
d, r, c, n, N = read_first_line()
z = read_second_line()

ds = OfflineANNS(d, r, c, n, z)
algorithm(d, r, c, n, z, ds)
