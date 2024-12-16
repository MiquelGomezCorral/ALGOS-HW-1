# Studients:
# Catalina Regolf Cortés. SCIPER: 394019
# Miquel Gómez Corral. SCIPER: 394325

import math
import random

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

def query(q):
    global N
    N -= 1
    
    print(f'q {" ".join(map(str, q))}')
    line = input().split(" ")
    m = int(line[0])
    p = [int(i) for i in line[1:]]
    return m, p
    
def print_q_star(q):
    print(f'* {" ".join(map(str, q))}')
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
    
def find_j_div(q, I, w):
    ini, end = 0, w-1
    mid = w // 2
    
    while ini <= end and N > 1:
        uj = get_uj(q, I, mid)
        m, p = query(uj)
        if p[0] == -1: # return _|_
            end = mid - 1
        else: ini = mid + 1 # return z
        mid = (ini + end) // 2
        
    return mid + 1 if mid + 1 < len(I) else mid

def find_j(q, I, w):
    for j in range(1, w+1):
        uj = get_uj(q, I, j)
        m, p = query(uj)
        if p[0] == -1 or N <= 1:
            return j - 1
        
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
def algorithm(d, r, c, n, z):
    mu = min(
        r,
        math.ceil(2*math.e*math.e * (math.log(n)+1))
    )
    while N > 0:
        q = sample_q(z, r, mu, d)
        dist_q_z = dist_1(q,z) 
        
        while N > 0 and dist_q_z < r:
            m, p = query(q)
            if p[0] == -1: # first coordinate is -1 -> not found
                print_q_star(q)
                
            M = get_m(z,q)
            w = math.ceil(c*r) + 1 - dist_q_z
            # I = random.sample(M, w)
            I = sorted(random.sample(M, w))

            j = find_j(q, I, w)
            
            update_q(q,I[j])
            dist_q_z = dist_1(q,z) 
        # End while
        
        if N > 0 and dist_q_z <= r:
            m, p = query(q)
            if p[0] == -1: # first coordinate is -1 -> not found
                print_q_star(q)
        
    print_q_star(q)
    
d, r, c, n, N = read_first_line()
z = read_second_line()

algorithm(d, r, c, n, z)
