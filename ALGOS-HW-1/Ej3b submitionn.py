import random 
import functools


def finite_field(x, p):
    return x % p
@functools.cache
def mod_inverse(a, p):
    m0 = p
    x0, x1 = 0, 1
    while a > 1:
        q = a // p
        t = p
        p = a % p
        a = t
        t = x0
        x0 = x1 - q * x0
        x1 = t
    if x1 < 0:
        x1 += m0
    return x1

def divide_field(x, y, p):
    """Performs modular division x / y mod p."""
    y_inv = mod_inverse(y, p)  # Find modular inverse of y mod p
    return finite_field(x * y_inv, p)  # Compute x / y mod p
    
def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True  # 2 and 3 are prime
    if num % 2 == 0 or num % 3 == 0:
        return False
    # Check divisors from 5 to sqrt(num)
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n):
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate

def compute_h(y, x, n, VXC, p):
    H = []

    for i in range(n):
        H.append([])
        for j in range(n):
            wij = VXC[i][j]
            xij = x[i][j]
            if wij == -1:
                H[i].append(0)
            else: # a -> b
                H[i].append(
                    finite_field( ((y**wij) * xij), p)
                )
            
    return H
                
def determinant(matrix, p):
    n = len(matrix)
    if n == 1:
        return finite_field(matrix[0][0], p)

    det = 1  # Initialize determinant
    for i in range(n):
        # Find pivot element to avoid dividing by zero
        pivot = i
        while pivot < n and finite_field(matrix[pivot][i], p) == 0:
            pivot += 1

        # If no non-zero pivot found, determinant is zero
        if pivot == n:
            return 0

        # Swap rows if needed
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            det = finite_field(-det, p)  # Swapping rows flips the sign of determinant

        # Scale the current row to make pivot 1
        pivot_value = matrix[i][i]
        det = finite_field(det * pivot_value, p)
        pivot_inv = divide_field(1, pivot_value, p)
        for j in range(i, n):
            matrix[i][j] = finite_field(matrix[i][j] * pivot_inv, p)

        # Eliminate entries below the pivot
        for k in range(i + 1, n):
            factor = matrix[k][i]
            for j in range(i, n):
                matrix[k][j] = finite_field(matrix[k][j] - factor * matrix[i][j], p)

    # The determinant is the product of the diagonal elements
    return finite_field(det, p)

def gaussian_elimination(A, b, p, inportant_index):
    n = len(b)
    # Forward elimination
    for i in range(n):
        # Pivoting: Ensure A[i][i] is non-zero by swapping rows if needed
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]  # Swap rows
                    b[i], b[j] = b[j], b[i]
                    break
            else:
                raise ValueError("Matrix is singular or not solvable in mod p")

        # Normalize the pivot row
        pivot_inv = divide_field(1, A[i][i], p)
        for k in range(i, n):
            A[i][k] = finite_field(A[i][k] * pivot_inv, p)
        b[i] = finite_field(b[i] * pivot_inv, p)

        # Eliminate entries below the pivot
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(i, n):
                A[j][k] = finite_field(A[j][k] - factor * A[i][k], p)
            b[j] = finite_field(b[j] - factor * b[i], p)

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] = finite_field(x[i] - A[i][j] * x[j], p)
        if i == inportant_index:
            break
    
    return x

def has_solution(n, m, b, t, c, VXC, size_p, F): 
    """ INITIAL CHECK """
    if (
        (m < n) or 
        (t* n < b) or 
        (t % 2 == 0 and c % 2 == 0 and b % 2 == 1)  # t & c even & b odd -> no
    ): 
        return False
        
    
    """" COMPUTE STUFF """
    alpha = []
    for i in range(n): 
        alpha.append(random.choices(F, k=n))
        
    Y = random.sample(F, n*t + 1)
    
    s = []
    for y in Y: 
        H = compute_h(y, alpha, n, VXC, size_p)
        s.append(determinant(H, size_p))
        
    P = []
    for j, y in enumerate(Y):
        P.append([])
        for i in range(len(Y)):
            P[j].append(finite_field((y**i), size_p))
            
    c = gaussian_elimination(P, s, size_p, b)
    
    has = (c[b] % size_p) != 0
    return has



""" READ LINES """
parameters = input()
# parameters = lines[0]
numbers = parameters.split(' ')

n = int(numbers[0]) # Volunteer & Cities
m = int(numbers[1]) # Preferences
b = int(numbers[2]) # Badget
t = int(numbers[3]) # Cost Train
c = int(numbers[4]) # Cost Car

VXC = []
for i in range(n): 
    VXC.append([])
    for j in range(n):
            VXC[i].append(-1) 

preferences_save = []
for idx in range(1,m+1): 
    preference = input()
    # preference = lines[idx]
    numbers = preference.split(' ')
    i = int(numbers[0])
    j = int(numbers[1])
    cost = int(numbers[2])
    VXC[i][j] = cost
    preferences_save.append((i,j,cost))
    
temp = b - c * n
if temp < 0 or temp % (t - c) != 0:
    print("no")
    exit(0)
t_count = temp // (t - c)
c_count = n - t_count
if t_count > n:
    print("no")
    exit(0)

# Step 0.5.2: reduce edge weights to 1, 2
for (i,j,cost) in preferences_save:
    if cost == t:
        VXC[i][j] = 2
    else:
        VXC[i][j] = 1

b = t_count *  2 + c_count * 1
t = 2
c = 1

size_max = max(t*n, n*n)
size_p = next_prime(size_max)

F = list(range(size_p))

has = False
for _ in range(1):
    if has_solution(n, m, b, t, c, VXC, size_p, F):
        print("yes")
        has = True
        break
if not has: 
    print("no")
