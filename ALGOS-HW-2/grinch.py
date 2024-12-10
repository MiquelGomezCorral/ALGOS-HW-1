import math
import random
# from ej3_global import algorithm

def hamming_dist(x, y, dim):
    return sum(x[i] != y[i] for i in range(dim))

def print_vector(x, dim):
    print(' '.join(map(str, x)))

def report_solution(x, dim):
    print('* ', end='')
    print_vector(x, dim)

class OfflineANNS:
    def __init__(self, dim, radius, approx, num_points, center):
        self.d = dim
        self.r = radius
        self.c = approx
        self.n = num_points
        self.z = center

        self.P = [center] + [list(map(int, input().split())) for _ in range(num_points - 1)]

        self.l = math.ceil(pow(self.n, math.log(1.0 - self.r / self.d) / math.log(1.0 - self.c * self.r / self.d)) * math.log(self.n))
        self.k = math.ceil(math.log(self.n) / math.log(1 / (1.0 - self.c * self.r / self.d)))

        self.h = [[random.randint(0, self.d - 1) for _ in range(self.k)] for _ in range(self.l)]
        for row in self.h:
            print(' '.join(map(str, row)))

        self.T = [{} for _ in range(self.l)]

        for u in range(self.l):
            for j in range(self.n):
                p_hash = tuple(self.P[j][self.h[u][v]] for v in range(self.k))
                if p_hash in self.T[u]:
                    self.T[u][p_hash].append(j)
                else:
                    self.T[u][p_hash] = [j]

    def query(self, q):
        for u in range(self.l):
            q_hash = tuple(q[self.h[u][v]] for v in range(self.k))
            if q_hash in self.T[u]:
                for j in self.T[u][q_hash]:
                    if hamming_dist(q, self.P[j], self.d) <= self.c * self.r:
                        return self.P[j]
        return [-1]

class OnlineANNS:
    def __init__(self, dim):
        self.d = dim

    def query(self, q):
        print('q ', end='')
        print_vector(q, self.d)
        size = int(input())
        return list(map(int, input().split()))

def main():
    random.seed()

    d, r, c, n, N = map(float, input().split())
    d, r, n, N = map(int, [d, r, n, N])
    z = list(map(int, input().split()))

    ds = OfflineANNS(d, r, c, n, z)
    # ds = OnlineANNS(d)

    # Your algorithm goes here
    #algorithm(d, r, c, n, N, z)

    # Example of interaction with the data structure
    a = ds.query(z)

    # Report solution
    report_solution(z, d)

if __name__ == "__main__":
    main()

