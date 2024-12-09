import java.util.*;

public class New {

    // Function to compute finite field x % p
    public static int finiteField(int x, int p) {
        return x % p;
    }

    // Function to divide in finite field (x / y) in mod p
    public static int divideField(int x, int y, int p) {
        int y_inv = 1;
        while (finiteField(y * y_inv, p) != 1) {
            y_inv++;
        }
        return finiteField(x * y_inv, p);
    }

    // Function to check if a number is prime
    public static boolean isPrime(int num) {
        if (num <= 1) return false;
        if (num <= 3) return true;  // 2 and 3 are prime
        if (num % 2 == 0 || num % 3 == 0) return false;
        int i = 5;
        while (i * i <= num) {
            if (num % i == 0 || num % (i + 2) == 0) return false;
            i += 6;
        }
        return true;
    }

    // Function to get the next prime after n
    public static int nextPrime(int n) {
        int candidate = n + 1;
        while (!isPrime(candidate)) {
            candidate++;
        }
        return candidate;
    }

    // Function to compute matrix H
    public static int[][] computeH(int y, int[][] x, int n, int[][] VXC, int p) {
        int[][] H = new int[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int wij = VXC[i][j];
                int xij = x[i][j];
                if (wij == -1) {
                    H[i][j] = 0;
                } else {
                    H[i][j] = finiteField((int) (Math.pow(y, wij) * xij), p);
                }
            }
        }
        return H;
    }

    // Function to compute determinant of a matrix modulo p
    public static int determinant(int[][] matrix, int p) {
        int n = matrix.length;
        if (n == 1) {
            return finiteField(matrix[0][0], p);
        }

        int det = 1;
        for (int i = 0; i < n; i++) {
            int pivot = i;
            while (pivot < n && finiteField(matrix[pivot][i], p) == 0) {
                pivot++;
            }

            if (pivot == n) {
                return 0;
            }

            if (pivot != i) {
                int[] temp = matrix[i];
                matrix[i] = matrix[pivot];
                matrix[pivot] = temp;
                det = finiteField(-det, p);
            }

            int pivotValue = matrix[i][i];
            det = finiteField(det * pivotValue, p);
            int pivotInv = divideField(1, pivotValue, p);
            for (int j = i; j < n; j++) {
                matrix[i][j] = finiteField(matrix[i][j] * pivotInv, p);
            }

            for (int k = i + 1; k < n; k++) {
                int factor = matrix[k][i];
                for (int j = i; j < n; j++) {
                    matrix[k][j] = finiteField(matrix[k][j] - factor * matrix[i][j], p);
                }
            }
        }

        return finiteField(det, p);
    }

    // Function for Gaussian elimination to solve Ax = b modulo p
    public static int[] gaussianElimination(int[][] A, int[] b, int p, int importantIndex) {
        int n = b.length;
        for (int i = 0; i < n; i++) {
            if (A[i][i] == 0) {
                for (int j = i + 1; j < n; j++) {
                    if (A[j][i] != 0) {
                        int[] temp = A[i];
                        A[i] = A[j];
                        A[j] = temp;
                        int tempB = b[i];
                        b[i] = b[j];
                        b[j] = tempB;
                        break;
                    }
                }
            }

            int pivotInv = divideField(1, A[i][i], p);
            for (int k = i; k < n; k++) {
                A[i][k] = finiteField(A[i][k] * pivotInv, p);
            }
            b[i] = finiteField(b[i] * pivotInv, p);

            for (int j = i + 1; j < n; j++) {
                int factor = A[j][i];
                for (int k = i; k < n; k++) {
                    A[j][k] = finiteField(A[j][k] - factor * A[i][k], p);
                }
                b[j] = finiteField(b[j] - factor * b[i], p);
            }
        }

        int[] x = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            x[i] = b[i];
            for (int j = i + 1; j < n; j++) {
                x[i] = finiteField(x[i] - A[i][j] * x[j], p);
            }
            if (i == importantIndex) {
                break;
            }
        }

        return x;
    }

    // Function to check if there is a solution
    public static boolean hasSolution(int n, int m, int b, int t, int c, int[][] VXC, int sizeP, List<Integer> F) {
        if (m < n || t * n < b || (t % 2 == 0 && c % 2 == 0 && b % 2 == 1)) {
            return false;
        }

        List<int[]> alpha = new ArrayList<>();
        Random rand = new Random();
        for (int i = 0; i < n; i++) {
            alpha.add(new int[n]);
            for (int j = 0; j < n; j++) {
                alpha.get(i)[j] = F.get(rand.nextInt(F.size()));
            }
        }

        List<Integer> Y = new ArrayList<>();
        for (int i = 0; i < n * t + 1; i++) {
            Y.add(F.get(rand.nextInt(F.size())));
        }

        List<Integer> s = new ArrayList<>();
        for (int y : Y) {
            int[][] H = computeH(y, alpha.toArray(new int[0][]), n, VXC, sizeP);
            s.add(determinant(H, sizeP));
        }

        int[][] P = new int[Y.size()][Y.size()];
        for (int j = 0; j < Y.size(); j++) {
            for (int i = 0; i < Y.size(); i++) {
                P[j][i] = finiteField((int) Math.pow(Y.get(j), i), sizeP);
            }
        }

        int[] c = gaussianElimination(P, s.stream().mapToInt(i -> i).toArray(), sizeP, b);
        return finiteField(c[b], sizeP) != 0;
    }

    // Main method
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String[] parameters = scanner.nextLine().split(" ");
        int n = Integer.parseInt(parameters[0]); // Volunteer & Cities
        int m = Integer.parseInt(parameters[1]); // Preferences
        int b = Integer.parseInt(parameters[2]); // Budget
        int t = Integer.parseInt(parameters[3]); // Cost Train
        int c = Integer.parseInt(parameters[4]); // Cost Car

        int[][] VXC = new int[n][n];
        for (int i = 0; i < n; i++) {
            Arrays.fill(VXC[i], -1);
        }

        for (int i = 0; i < m; i++) {
            String[] preference = scanner.nextLine().split(" ");
            int i1 = Integer.parseInt(preference[0]);
            int j = Integer.parseInt(preference[1]);
            int cost = Integer.parseInt(preference[2]);
            VXC[i1][j] = cost;
        }

        int sizeMax = Math.max(t * n, n * n);
        int sizeP = nextPrime(sizeMax);

        List<Integer> F = new ArrayList<>();
        for (int i = 0; i < sizeP; i++) {
            F.add(i);
        }

        boolean hasSolution = false;
        for (int i = 0; i < 1; i++) {
            if (hasSolution(n, m, b, t, c, VXC, sizeP, F)) {
                System.out.println("yes");
                hasSolution = true;
                break;
            }
        }
        if (!hasSolution) {
            System.out.println("no");
        }

        scanner.close();
    }
}
