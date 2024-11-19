import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;
import java.util.Arrays;

public class FiniteFieldSolver {

    // Finite field operation: x % p
    public static int finiteField(int x, int p) {
        return (x % p + p) % p; // Handles negative values correctly
    }

    // Modular division: x / y in field mod p
    public static int divideField(int x, int y, int p) {
        int yInv = 1;
        while (finiteField(y * yInv, p) != 1) {
            yInv++;
        }
        return finiteField(x * yInv, p);
    }

    // Check if a number is prime
    public static boolean isPrime(int num) {
        if (num <= 1) return false;
        if (num <= 3) return true;
        if (num % 2 == 0 || num % 3 == 0) return false;

        for (int i = 5; i * i <= num; i += 6) {
            if (num % i == 0 || num % (i + 2) == 0) return false;
        }
        return true;
    }

    // Find the next prime greater than n
    public static int nextPrime(int n) {
        int candidate = n + 1;
        while (!isPrime(candidate)) {
            candidate++;
        }
        return candidate;
    }

    // Compute the H matrix
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

    // Compute the determinant of a matrix mod p
    public static int determinant(int[][] matrix, int p) {
        int n = matrix.length;
        if (n == 1) return finiteField(matrix[0][0], p);
        if (n == 2) {
            return finiteField(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0], p);
        }

        int det = 0;
        for (int col = 0; col < n; col++) {
            int[][] subMatrix = new int[n - 1][n - 1];
            for (int i = 1; i < n; i++) {
                int subCol = 0;
                for (int j = 0; j < n; j++) {
                    if (j == col) continue;
                    subMatrix[i - 1][subCol++] = matrix[i][j];
                }
            }
            int cofactor = finiteField(matrix[0][col] * determinant(subMatrix, p), p);
            det = finiteField(det + ((col % 2 == 0 ? 1 : -1) * cofactor), p);
        }
        return det;
    }

    // Gaussian elimination mod p
    public static int[] gaussianElimination(int[][] A, int[] b, int p) {
        int n = b.length;

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int factor = divideField(A[j][i], A[i][i], p);
                for (int k = i; k < n; k++) {
                    A[j][k] = finiteField(A[j][k] - finiteField(factor * A[i][k], p), p);
                }
                b[j] = finiteField(b[j] - finiteField(factor * b[i], p), p);
            }
        }

        int[] x = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            x[i] = divideField(b[i], A[i][i], p);
            for (int j = i - 1; j >= 0; j--) {
                b[j] = finiteField(b[j] - finiteField(A[j][i] * x[i], p), p);
            }
        }
        return x;
    }

    // Check if the system has a solution
    public static boolean hasSolution(int n, int m, int b, int t, int c, int[][] VXC, int sizeP, List<Integer> F) {
        if (m < n || t * n < b || (t % 2 == 0 && c % 2 == 0 && b % 2 == 1)) {
            return false;
        }

        Random random = new Random();
        int[][] alpha = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                alpha[i][j] = F.get(random.nextInt(F.size()));
            }
        }

        List<Integer> Y = new ArrayList<>();
        for (int i = 0; i < n * t + 1; i++) {
            Y.add(F.get(random.nextInt(F.size())));
        }

        int[] s = new int[Y.size()];
        for (int i = 0; i < Y.size(); i++) {
            int y = Y.get(i);
            int[][] H = computeH(y, alpha, n, VXC, sizeP);
            s[i] = determinant(H, sizeP);
        }

        int[][] P = new int[Y.size()][Y.size()];
        for (int j = 0; j < Y.size(); j++) {
            for (int i = 0; i < Y.size(); i++) {
                P[j][i] = finiteField((int) Math.pow(Y.get(j), i), sizeP);
            }
        }

        int[] cVector = gaussianElimination(P, s, sizeP);
        return finiteField(cVector[b], sizeP) != 0;
    }

    // Main method
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Read the parameters
        String parameters = scanner.nextLine();
        String[] numbers = parameters.split(" ");

        int n = Integer.parseInt(numbers[0]); // Volunteers & Cities
        int m = Integer.parseInt(numbers[1]); // Preferences
        int b = Integer.parseInt(numbers[2]); // Budget
        int t = Integer.parseInt(numbers[3]); // Cost of Train
        int c = Integer.parseInt(numbers[4]); // Cost of Car

        // Initialize the VXC matrix with -1
        int[][] VXC = new int[n][n];
        for (int i = 0; i < n; i++) {
            Arrays.fill(VXC[i], -1);
        }

        // Read preferences and populate the VXC matrix
        for (int idx = 0; idx < m; idx++) {
            String preference = scanner.nextLine();
            String[] preferenceNumbers = preference.split(" ");
            int i = Integer.parseInt(preferenceNumbers[0]);
            int j = Integer.parseInt(preferenceNumbers[1]);
            int cost = Integer.parseInt(preferenceNumbers[2]);
            VXC[i][j] = cost;
        }

        scanner.close();

        int sizeMax = Math.max(t * n, n * n);
        int sizeP = nextPrime(sizeMax);

        List<Integer> F = new ArrayList<>();
        for (int i = 0; i < sizeP; i++) {
            F.add(i);
        }

        boolean hasSolution = false;
        for (int i = 0; i < 20; i++) {
            if (hasSolution(n, m, b, t, c, VXC, sizeP, F)) {
                System.out.println("yes");
                hasSolution = true;
                break;
            }
        }
        if (!hasSolution) {
            System.out.println("no");
        }
    }
}
