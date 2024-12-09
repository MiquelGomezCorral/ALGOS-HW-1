#include <iostream>
#include <vector>
#include <map>
#include <time.h>

using namespace std;

int hammingDist(const vector<int> &x, const vector<int> &y, int dim)
{
    int count = 0;
    for(int i = 0; i < dim; i++)
    {
        if(x[i] != y[i])
        {
            count++;
        }
    }

    return count;
}

void printVector(const vector<int> &x, int dim)
{
    for(int i = 0; i < dim; i++)
    {
        cout << x[i] << (i != dim-1 ? " " : "");
    }
    cout << endl;
    cout.flush();
}

/* reports a solution using the format demanded by the Codeforces problem */
void reportSolution(const vector<int> &x, int dim)
{
    cout << "* ";
    cout.flush();
    printVector(x, dim);
}

/* to be used when running locally */
class offlineANNS
{
    private:
        int d;
        int n;
        int r;
        double c;
        vector<int> z;
        vector< vector<int> > P;

        int k;
        int l;
        vector< vector<int> > h;
        vector< map< vector<int>, vector<int> > > T;
    
    public:
        offlineANNS(int dim, int radius, double approx, int numPoints, vector<int> center)
        {
            d = dim;
            r = radius;
            c = approx;
            n = numPoints;
            z = center;

            P = vector< vector<int> >(n, vector<int>(d, 0));

            for(int i = 0; i < d; i++)
            {
                P[0][i] = z[i];
            }

            /* read the rest of the dataset */
            for(int j = 1; j < n; j++)
            {
                for(int i = 0; i < d; i++)
                {
                    cin >> P[j][i];
                }
            }

            /* initialize the data structure by sampling the hash functions and filling the corresponding hash tables */
            l = ceil(pow(n, log(1.0-double(r)/double(d))/log(1.0-c*double(r)/double(d)))*log(n));
            k = ceil(log(n) / log(1/(1.0-c*double(r)/double(d))));

            h = vector< vector<int> >(l, vector<int>(k, -1));

            for(int u = 0; u < l; u++)
            {
                for(int v = 0; v < k; v++)
                {
                    h[u][v] = rand()%d;
                    cout << h[u][v] << endl;
                }
            }

            T = vector< map< vector<int>, vector<int> > >(l, map< vector<int>, vector<int> >());

            for(int u = 0; u < l; u++)
            {
                for(int j = 0; j < n; j++)
                {
                    vector<int> pHash = vector<int>(k, -1);
                    for(int v = 0; v < k; v++)
                    {
                        pHash[v] = P[j][h[u][v]];
                    }
                    
                    map< vector<int>, vector<int> >::iterator it = T[u].find(pHash);

                    if(it != T[u].end())
                    {
                        (it -> second).push_back(j);
                    }
                    else
                    {
                        T[u][pHash] = vector<int>(1, j);
                    }
                }
            }
        }

        /* issues a query to the ANNS data structure and returns the answer */
        vector<int> query(const vector<int> &q)
        {
            vector<int> a;

            int found = -1;
            for(int u = 0; u < l && found == -1; u++)
            {
                vector<int> qHash = vector<int>(k, -1);
                for(int v = 0; v < k; v++)
                {
                    qHash[v] = q[h[u][v]];
                }

                map< vector<int>, vector<int> >::iterator it = T[u].find(qHash);
                if(it != T[u].end())
                {
                    int size = (it -> second).size();
                    for(int e = 0; e < size && found == -1; e++)
                    {
                        int j = (it -> second)[e];
                        if(hammingDist(q, P[j], d) <= c*r)
                        {
                            found = j;
                        }
                    }
                }
            }

            if(found == -1)
            {
                a = vector<int>(1,-1);
            }
            else
            {
                a = vector<int>(d, -1);
                for(int i = 0; i < d; i++)
                {
                    a[i] = P[found][i];
                }
            }

            return a;
        }
};

/* to be used for submitting to Codeforces */
class onlineANNS
{
    private:
        int d; // dimension of the hypercube
    
    public:
        onlineANNS(int dim)
        {
            d = dim;
        }

        /* issues a query using the format demanded by the Codeforces problem, reads the answer and returns it */
        vector<int> query(const vector<int> &q)
        {
            cout << "q ";
            cout.flush();
            printVector(q, d);

            vector<int> answer = vector<int>();
            int size;
            
            cin >> size;
            for(int i = 0; i < size; i++)
            {
                int elem;
                cin >> elem;
                answer.push_back(elem);
            }

            return answer;
        }
};

int main()
{
    srand(time(NULL));

    int d;
    int r;
    double c;
    int n;
    int N;
    vector<int> z;

    /* read parameters */
    cin >> d;
    cin >> r;
    cin >> c;
    cin >> n;
    cin >> N;

    /* read center point */
    z = vector<int>(d, 0);
    for(int i = 0; i < d; i++)
    {
        cin >> z[i];
    }

    /* use offlineANNS to test locally, use onlineANNS for submitting to Codeforces */
    offlineANNS ds(d, r, c, n, z); // this also reads the remaining n-1 points in the dataset
    // onlineANNS ds(d);

    /* your algorithm goes here */

    /* example of interaction with the data structure */
    vector<int> a;
    a = ds.query(z);

    /* report solution */
    reportSolution(z, d);

    return 0;
}