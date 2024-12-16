import random 
import math 


def sample_q(p, d):
    x = list(p)
    
    for i in random.sample(range(len(p)), d):
        x[i] = 1 - x[i]
    
    return x

    
r = 3
c = 2
z = [1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0,  0,0,0,0,0] #20
dist = 2*math.ceil(c*r) + 2
print(f"{dist = }")
print(f"{" ".join(map(str, z))}")

for i in range(6):
    # q = sample_q(z,r*2,r,len(z))
    q = sample_q(z, dist)
    
    # a = f'* {" ".join(map(str, q))}'
    a = f'{" ".join(map(str, q))}'
    print(a)
    

    
