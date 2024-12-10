import random 
import time
import math 
# l = 100000000
# suma = 0
# for i in range(l):
#     suma += min(random.randint(1,l), random.randint(1,l))
    
# t1 = time.time()
# for i in range(l):
#     suma += min(random.randint(1,l), random.randint(1,l))

# t2 = time.time()  
# print(f"Ex1: {(t2-t1)}")
# print(f"Ex1: {(t2-t1)/l}")

# for i in range(l):
#     x1 = random.randint(1,l)
#     x2 = random.randint(1,l)
#     if x1 > x2: suma += x1
#     else: suma += x2

# t3 = time.time()

# print(f"Ex2: {(t3-t2)}")
# print(f"Ex2: {(t3-t2)/l}")


def sample_q(z, r, mu, d):
    rhs = r - mu
    x = list(z)
    
    for i in random.sample(range(d), rhs):
        x[i] = 1 - x[i]
    
    return x

def query(q):
    print(f'q {" ".join(map(str, q))}')
    line = input().split(" ")
    m = int(line[0])
    p = [int(i) for i in line[1:]]
    return m, p
    
def dist(q, z):
    dist = 0
    for qi, zi in zip(q, z):
        if qi != zi: 
            dist += 1
            
    return dist 
    
def get_uj(q, I, j):
    uj = list(q)
    for i in I[:j]:
        uj[i] = 1-q[i]
        
    return uj

def get_m(z, q, d):
    return [i for i in range(d) if z[i] == q[i]]
def update_q(q, j):
    q[j] = 1 - q[j]
    
r = 3
c = 1.5
z = [0,1,0,1,0,1,0,1,0,1,0]
for i in range(10):
    q = sample_q(z,r*2,r,len(z))
    
    print(f"{q = }")
    # print(f"{z = }")
    update_q(q, i)
    print(f"{q = }")
    # # print(f"uj= {get_uj(q, get_m(z, q, len(q)), len(z))}")
    dist_q_z = dist(q,z)
    print(f"{dist_q_z = }")
    # # print(f"{query(q) = }")
    
    M = get_m(z,q,len(z))
    w = math.ceil(c*r) + 1 - dist_q_z
    I = sorted(random.sample(M, w))
    print(I)
    
    
