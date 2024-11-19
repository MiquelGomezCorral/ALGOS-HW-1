import random 

def finite_field(x, p):
    return x % p
def divide_field(x, y, p): #x / y
    y_inv = 1
    while finite_field(y * y_inv, p) != 1:
        y_inv += 1
    
    return finite_field(x * y_inv, p)
    
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
    # Base case: if the matrix is 1x1, return the single element
    if len(matrix) == 1:
        return finite_field(matrix[0][0], p)
    
    # Base case: if the matrix is 2x2, return ad - bc
    if len(matrix) == 2:
        return (finite_field(matrix[0][0] * matrix[1][1], p) - 
                finite_field(matrix[0][1] * matrix[1][0], p))

    # Recursive case: expand along the first row
    det = 0
    for col in range(len(matrix)):
        # Create a submatrix by excluding the current row and column
        submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
        # Add or subtract the determinant of the submatrix
        mult1 = finite_field(matrix[0][col] * determinant(submatrix, p), p)
        mult2 = finite_field(((-1) ** col) * mult1, p)
        det = finite_field(det + mult2, p)
    
    return det

def gaussian_elimination(A, b, p):
    n = len(b)
    # Forward elimination
    for i in range(n):
        # Pivoting
        for j in range(i + 1, n):
            factor = divide_field(A[j][i], A[i][i], p)
            for k in range(i, n):
                mult1 = finite_field(factor * A[i][k], p)
                A[j][k] = finite_field(A[j][k] - mult1, p)
                
            mult1 = finite_field(factor * b[i], p)
            b[j] = finite_field(b[j] - mult1, p)

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = divide_field(b[i], A[i][i], p)
        for j in range(i - 1, -1, -1):
            mult1 = finite_field(A[j][i] * x[i], p)
            b[j] = finite_field(b[j] - mult1, p)
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
            
    c = gaussian_elimination(P, s, size_p)
    
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

for idx in range(1,m+1): 
    preference = input()
    # preference = lines[idx]
    numbers = preference.split(' ')
    i = int(numbers[0])
    j = int(numbers[1])
    cost = int(numbers[2])
    VXC[i][j] = cost

size_max = max(t*n, n*n)
size_p = next_prime(size_max)

F = list(range(size_p))

has = False
for _ in range(20):
    if has_solution(n, m, b, t, c, VXC, size_p, F):
        print("yes")
        has = True
        break
if not has: 
    print("no")
