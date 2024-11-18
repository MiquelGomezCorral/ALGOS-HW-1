import random 

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
                H[i].append(((y**wij) * xij) % p)
            
    return H
                
def determinant(matrix):
    # Base case: if the matrix is 1x1, return the single element
    if len(matrix) == 1:
        return matrix[0][0]
    
    # Base case: if the matrix is 2x2, return ad - bc
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # Recursive case: expand along the first row
    det = 0
    for col in range(len(matrix)):
        # Create a submatrix by excluding the current row and column
        submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
        # Add or subtract the determinant of the submatrix
        det += ((-1) ** col) * matrix[0][col] * determinant(submatrix)
    
    return det

def gaussian_elimination(A, b):
    n = len(b)
    # Forward elimination
    for i in range(n):
        # Pivoting
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i] / A[i][i]
        for j in range(i - 1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x


def has_solution():
    """ READ LINES """
    # parameters = input()
    parameters = lines[0]
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
        # preference = input()
        preference = lines[idx]
        numbers = preference.split(' ')
        i = int(numbers[0])
        j = int(numbers[1])
        cost = int(numbers[2])
        VXC[i][j] = cost
    
    """ INITIAL CHECK """
    if (
        (m < n) or 
        (t* n < b) or 
        (t % 2 == 0 and c % 2 == 0 and b % 2 == 1)  # t & c even & b odd -> no
    ): 
        print("no"); return
        
    
    """" COMPUTE STUFF """
    size_max = max(t*n, n*n)
    size_p = next_prime(size_max)
    
    F = list(range(size_p))
    
    alpha = []
    for i in range(n): 
        alpha.append(random.choices(F, k=n))
        
    Y = random.sample(F, n*t + 1)
    
    s = []
    for y in Y: 
        H = compute_h(y, alpha, n, VXC, size_p)
        s.append(determinant(H) % size_p)
        
    P = []
    for j, y in enumerate(Y):
        P.append([])
        for i in range(len(Y)):
            P[j].append((y**i) % size_p)
            
    c = gaussian_elimination(P, s)
    
    has = (c[b+1] % size_p) != 0
    #print("yes" if has else "no")
    return has
    
    
for test in range(3):
    yes_n = 0
    print(f"{test = }")
    if test == 0:
        lines = [
            "3 6 7 3 1",
            "0 0 1",
            "1 1 3",
            "2 2 1",
            "1 0 3",
            "0 2 3",
            "2 1 1",
        ]
    elif test == 1:
        lines = [
            "3 6 7 3 1",
            "0 0 3",
            "1 1 3",
            "2 2 3",
            "0 1 3",
            "1 2 1",
            "2 0 1",
        ]
    elif test == 2:
        lines = [
        "2 2 7 5 3",
        "0 0 3",
        "1 1 5",   
    ]
    
    for iterations in range(1,10001):
        if has_solution():
            yes_n+=1
        
        if iterations % 2500 == 0:
            print(f"YES PROPORTION: {yes_n*100 / iterations:.4}%")


# %%
for test in range(3):
    lines = []
    answer = ""
    if test == 0:
        lines = [
            "3 6 7 3 1",
            "0 0 1",
            "1 1 3",
            "2 2 1",
            "1 0 3",
            "0 2 3",
            "2 1 1",
        ]
        answer = "yes"
    elif test == 1:
        lines = [
            "3 6 7 3 1",
            "0 0 3",
            "1 1 3",
            "2 2 3",
            "0 1 3",
            "1 2 1",
            "2 0 1",
        ]
        answer = "no"
    elif test == 2:
        lines = [
        "2 2 7 5 3",
        "0 0 3",
        "1 1 5",   
    ]
        answer = "no"
        
    for _ in lines:
        input()
    print(answer)
    
# %%
