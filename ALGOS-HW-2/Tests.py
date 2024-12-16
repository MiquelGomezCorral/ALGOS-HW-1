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


def sample_q(p, d):
    x = list(p)
    
    for i in random.sample(range(len(p)), d):
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

def get_m(z, q):
    d = len(z)
    return [i for i in range(d) if q[i] == z[i]]
def update_q(q, j):
    q[j] = 1 - q[j]
    
r = 3
c = 2
z = [1,1,1] 
aux = f"* {" ".join(map(str, z))}"
aux = f"q {" ".join(map(str, z))}"
print(aux)
print(len(aux))

# for i in range(6):
#     # q = sample_q(z,r*2,r,len(z))
#     q = sample_q(z, dist)
    
#     # a = f'* {" ".join(map(str, q))}'
#     a = f'q {" ".join(map(str, q))}'
#     print(a)
    
    # print(f"{q = }")
    # dist_q_z = dist(q,z)
    # print(f"{dist_q_z = }")
    # M = get_m(z,q)
    # print(f"{M = }")
    
    
    # # # print(f"{z = }")
    # # update_q(q, i)
    # # print(f"{q = }")
    # # # # print(f"uj= {get_uj(q, get_m(z, q, len(q)), len(z))}")
    # # dist_q_z = dist(q,z)
    # # print(f"{dist_q_z = }")
    # # # # print(f"{query(q) = }")
    
    # # M = get_m(z,q)
    # # print(f"{M = }")
    # w = math.ceil(c*r) + 1 - dist_q_z
    # I = sorted(random.sample(M, w))
    # print(f"{I = }")
    # for j in range(1, w+1):
    #     uj = get_uj(q, I, j)
    #     print(f"{j = } {uj = }")        
    
    
