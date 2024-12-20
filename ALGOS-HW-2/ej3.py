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

BAD_ANS = [-1]
IS_LOCAL = False
SEED = 42

class OfflineANNS:
    def __init__(self, dim, radius, approx,  numPoints, center):
        self.d = dim
        self.r = radius
        self.c = approx
        self.n = numPoints
        self.z = center

        self.P = [[0 for _ in range(self.d)] for _ in range(self.n)]

        for i in range(self.d):
            self.P[0][i] = self.z[i]

        # read the rest of the dataset
        for j in range(1, self.n):
            self.P[j] = [int(tmp) for tmp in input().split()]

        # initialize the data structure by sampling the hash functions and filling the corresponding hash tables
        self.l = math.ceil(pow(self.n, math.log(1.0-float(self.r)/float(self.d))/math.log(1.0-self.c*float(self.r)/float(self.d)))*math.log(self.n))
        self.k = math.ceil(math.log(self.n) / math.log(1/(1.0-self.c*float(self.r)/float(self.d))))

        self.h = [[-1 for _ in range(self.k)] for _ in range(self.l)] 

        for u in range(self.l):
            for v in range(self.k):
                self.h[u][v] = random.randint(0, self.d - 1)
                print(self.h[u][v])

        self.T = [{} for _ in range(self.l)]

        for u in range(self.l):
            for j in range(self.n):
                pHash = [-1 for _ in range(self.k)]
                for v in range(self.k):
                    pHash[v] = self.P[j][self.h[u][v]]
                
                
                pHash = tuple(pHash)    # list is not hashable
                if pHash in self.T[u].keys():
                    self.T[u][pHash].append(j)
                else:
                    self.T[u][pHash] = [j]
    
    def query(self, q):
        """issues a query to the ANNS data structure and returns the answer"""
        a = []
        found = -1

        for u in range(self.l):
            if found != -1:
                break

            qHash = [-1 for _ in range(self.k)]
            for v in range(self.k):
                qHash[v] = q[self.h[u][v]]
            
            qHash = tuple(qHash)    # list is not hashable
            if qHash in self.T[u].keys():
                size = len(self.T[u][qHash])
                for e in range(size):
                    j = self.T[u][qHash][e]
                    if found != -1:
                        break
                    if dist_1(q, self.P[j]) <= self.c * self.r:   # dist declared below
                        found = j

        if found == -1:
            a = [-1]
        else:
            a = [-1 for _ in range(self.d)]
            for i in range(self.d):
                a[i] = self.P[found][i]

        return a

# Becase
offlineANNS = None


def read_first_line():
    line = input()
    d, r, c, n, N = [i for i in line.split()]
    return int(d), int(r), float(c), int(n), int(N)
def read_second_line():
    line = input()
    z = [int(i) for i in line.split()]
    return z

def query(q):
    # global N
    # N -= 1
    
    print(f'q {" ".join(map(str, q))}')
    if IS_LOCAL:
        p = offlineANNS.query(q)
    else:
        line = input().split()
        # m = int(line[0])
        p = [int(i) for i in line[1:]]
    return p  
def print_q_star(q):
    print(f'* {" ".join(map(str, q))}')
    if IS_LOCAL:
        print(offlineANNS.query(q))
    
def dist_1(q, z):
    dist = 0
    for qi, zi in zip(q, z):
        if qi != zi: 
            dist += 1
            
    return dist 

def sample_q(z, r_mu_diff , d):
    """
    Change rhs elements from z so x is at rhs distance from z 
    """
    x = list(z)
    
    """ CHOICES?? """
    for i in random.choices(range(d), k=r_mu_diff): 
        x[i] = 1 - x[i]
    
    return x

def get_m(z, q):
    d = len(z)
    return [i for i in range(d) if q[i] == z[i]]
    
def find_j_div(q, I, w):
    ini, end = 0, w
    
    while ini + 1 < end:
        mid = (ini + end) // 2
        # uj = get_uj(q, I, mid)
        uj = list(q)
        for i in range(mid):
            uj[I[i]] = 1-uj[I[i]]
        
        if query(uj) == BAD_ANS: # return _|_
            end = mid
        else: ini = mid # return z
        
    return ini

def find_j(q, I, w):
    uj = list(q)
    for j in range(w):
        uj[I[j]] = 1-uj[I[j]]
        if query(uj) == BAD_ANS:
            return j
        
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
def algorithm(d, r, c, n, z, linear):
    mu = min(
        r,
        math.ceil(2*math.e*math.e * (math.log(n)+1))
    )
    r_mu_diff = r - mu
    loop = True
    while loop:
        q = sample_q(z, r_mu_diff, d)
        dist_q_z = dist_1(q,z) 
        
        while dist_q_z < r and loop:
            if query(q) == BAD_ANS: # first coordinate is -1 -> not found
                print_q_star(q)
                loop = False
                break
                
            M = get_m(z,q)
            w = math.ceil(c*r) + 1 - dist_q_z
            I = random.sample(M, w)
            # I = sorted(random.sample(M, w))

            if linear:
                j = find_j(q, I, w)
            else: 
                j = find_j_div(q, I, w)
            
            # Update q
            q[I[j]] = 1 - q[I[j]]
            dist_q_z = dist_1(q,z) 
        # End while
        
        if dist_q_z <= r and loop:
            if query(q) == BAD_ANS: # first coordinate is -1 -> not found
                print_q_star(q)
                loop = False
                break
    

if __name__ == "__main__":    
    random.seed(SEED)
    d, r, c, n, N = read_first_line()
    z = read_second_line()

    if IS_LOCAL:
        offlineANNS = OfflineANNS(d, r, c, n, z)
    
    algorithm(d, r, c, n, z, False) # True Linear, False Binary Search
