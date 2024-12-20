import copy
import math
from math import ceil, log
import random
import sys

__RNG_SEED = 111111111
# Because Codeforces does not have ONLINE_JUDGE for python
__IS_LOCAL = True
__BAD_REPLY = [-1]
__IS_3_4_2 = True

# Offline grader
# This is not the main part of the implementation
# This is a python transaltion from grinch.cpp because why the hell not ¯\_(ツ)_/¯
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
        self.l = ceil(pow(self.n, log(1.0-float(self.r)/float(self.d))/log(1.0-self.c*float(self.r)/float(self.d)))*log(n))
        self.k = ceil(log(self.n) / log(1/(1.0-self.c*float(self.r)/float(self.d))))

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
                    if dist(q, self.P[j], self.d) <= self.c * self.r:   # dist declared below
                        found = j

        if found == -1:
            a = [-1]
        else:
            a = [-1 for _ in range(self.d)]
            for i in range(self.d):
                a[i] = self.P[found][i]

        return a

##########################
# Because why not using a global variable to make our life easier
offlineANNS = None

# Manhattan distance
def dist(x, y, n_dim):
    return sum([abs(x[i] - y[i]) for i in range(n_dim)])

def anns_query(x):
    """Send queries to the local/codeforces grader."""
    print("q", *[xi for xi in x])
    sys.stdout.flush()
    if __IS_LOCAL:
        reply = offlineANNS.query(x)
    else:
        line = [x for x in input().split()]
        reply = [int(x) for x in line[1:]]
    return reply

def answer(x):
    print("*", *[xi for xi in x])
    sys.stdout.flush()
    if __IS_LOCAL:
        print(offlineANNS.query(x))

def algo(n_dim, radius, anns_c, n_kids, n_queries, isolated_kid):
    """Algo

    `z` is isolated_kid
    """
    T = 10 # Number of trials, should be a term that depends on d and n
    
    # Step 1
    mu = min(radius, ceil(2 * math.e**2 * (math.log(n_kids) + 1)))
    radius_mu_diff = radius - mu

    # Step 2
    for _ in range(T):
        # Step 2.a - Sample q uniformly
        ## Choose positions to flip
        flip_pos = random.choices(range(n_dim), k=radius_mu_diff)
        query_loc = copy.deepcopy(isolated_kid) # `q`
        for pos in flip_pos:
            query_loc[pos] = 1 - query_loc[pos]
        
        # Step 2.b
        anns_return = None
        while True:
            # Condition
            anns_return = anns_query(query_loc)
            
            if anns_return == __BAD_REPLY:
                break
            if dist(isolated_kid, query_loc, n_dim) >= r:
                break
            
            # anns_query(query_loc) must be equals to the isolated_kid

            # Step 2.b.i
            Mzq = [i for i in range(n_dim) if query_loc[i] == isolated_kid[i]]
            w = ceil(anns_c * radius) + 1 - dist(isolated_kid, query_loc, n_dim)
            I = random.sample(Mzq, k=w) # SAMPLE NOT .choices() !!!
            
            # Step 2.b.ii
            # Linear scan
            if __IS_3_4_2 == False:
                u = copy.deepcopy(query_loc)    # this is u_0 - homework notation
                for i in range(w):
                    u[I[i]] = 1 - u[I[i]]
                    if anns_query(u) == __BAD_REPLY:   # this if is always reachable
                        query_loc[I[i]] = 1 - query_loc[I[i]]
                        break
            # Binary search
            else:
                # Bin search for R - this is ugly to understand but clean
                bin_search_L = 0
                bin_search_R = w  
                while bin_search_L + 1 < bin_search_R:
                    bin_mid = (bin_search_L + bin_search_R) // 2 
                    u = copy.deepcopy(query_loc)
                    for i in range(bin_mid):
                        u[I[i]] = 1 - u[I[i]]

                    if anns_query(u) == __BAD_REPLY:
                        bin_search_R = bin_mid
                    else:
                        bin_search_L = bin_mid

                j_star = bin_search_L
                query_loc[I[j_star]] = 1 - query_loc[I[j_star]]

        # Step 2.c
        if anns_return == __BAD_REPLY and dist(isolated_kid, query_loc, n_dim) <= r:
            return query_loc
    
    raise RuntimeError()

if __name__ == "__main__":
    random.seed(__RNG_SEED)
    first_line = input().split()
    d = int(first_line[0])
    r = int(first_line[1])
    c = float(first_line[2])
    n = int(first_line[3])
    N = int(first_line[4])

    z = [int(x) for x in input().split()]

    if __IS_LOCAL:
        offlineANNS = OfflineANNS(d, r, c, n, z)

    ans = algo(d, r, c, n, N, z)
    answer(ans)