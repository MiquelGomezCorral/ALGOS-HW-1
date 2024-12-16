import math
import random
from grinch import OfflineANNS 

def read_first_line():
    line = input()
    d, r, c, n, N = [i for i in line.split(" ")]
    return int(d), int(r), float(c), int(n), int(N)
def read_second_line():
    line = input()
    z = [int(i) for i in line.split(" ")]
    return z




def main():
    d, r, c, n, N = read_first_line()
    z = read_second_line()

    ds = OfflineANNS(d, r, c, n, z)
    
    while True:
        line = input()
        q = [int(i) for i in line.split(" ")]
        print(ds.query(q))
    
    
if __name__ == '__main__':
    main()