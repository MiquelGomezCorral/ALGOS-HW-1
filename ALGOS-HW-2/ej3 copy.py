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
    global rem_q
    rem_q -= 1
    
    print(f'q {" ".join(map(str, q))}')
    line = input().split(" ")
    m = int(line[0])
    p = [int(i) for i in line[1:]]
    return m, p
    
def print_q_star(q):
    print(f'* {" ".join(map(str, q))}')
    
    
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
    return [i for i in range(d) if z[i] == q[i]]
    
def find_j_div(q, I, w):
    ini, end = 0, w
    mid = w // 2
    
    while ini <= end and rem_q > 1:
        uj = get_uj(q, I, mid)
        m, p = query(uj)
        if m == 1: # return _|_
            end = mid - 1
        else: ini = mid + 1 # return z
        mid = (ini + end) // 2
        
    return mid

def find_j(q, I, w):
    for j in range(1, w):
        uj = get_uj(q, I, j)
        m, p = query(uj)
        if m == 1 or rem_q <= 1:
            return j-1
        
    return w
         
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
d, r, c, n, N = read_first_line()
z = read_second_line()
mu = min(
    r,
    math.ceil(2*math.e*math.e * (math.log(n)+1))
)

rem_q = N
while rem_q > 1:
    q = sample_q(z, r, mu, d)
    dist_q_z = dist_1(q,z) 
    
    while rem_q > 1 and dist_q_z < r:
        m, p = query(q)
        if m == 1: # m = d or 1 bc d >= 10
            print_q_star(q)
            
        M = get_m(z,q)
        w = math.ceil(c*r) + 1 - dist_q_z
        # I = random.sample(M, w)
        I = sorted(random.sample(M, w))
        
        j = find_j(q, I, w)
        update_q(q,j)
        dist_q_z = dist_1(q,z) 
    
print_q_star(q)