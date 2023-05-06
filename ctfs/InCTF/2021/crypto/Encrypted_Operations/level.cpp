#include <vector>
#include <string>
#include <random>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <boost/lexical_cast.hpp>

#include "utils.cpp"

#define HIGH 9
#define LOW 0

using namespace std;

//################################################################################################

int level2()
{
    int MAT_SIZE = 5;
    vector<int64_t> p;
    vector<int64_t> msgvector;

    vector<vector<int64_t>> m1(MAT_SIZE, vector<int64_t>(MAT_SIZE));
    vector<int> row = {0, 1, 2, 3, 4};

    random_device rd;
    mt19937 g(rd());

    shuffle(row.begin(), row.end(), g);

    cout << "                   =============================\n";
    cout << "                       --------LEVEL2--------\n";
    cout << "                   =============================\n";

    for (int x = 0; x < MAT_SIZE; x++)
    {
        for (int y = 0; y < MAT_SIZE; y++)
        {
            if ((x == row[0]) || (x == row[1]))
                m1[x][y] = 0;
            else
                m1[x][y] = Genrand(LOW, HIGH);
        }
    }

    long int userInp;
    msgvector = m1[row[2]];

    FheEncrypt(msgvector);
    EncryptedOperations();

    p = FheDecrypt();
    p = vector<int64_t>(p.begin(), p.begin() + MAT_SIZE + 1);
    userInp = VecToNum(p);

    msgvector = m1[row[3]];

    FheEncrypt(msgvector);
    EncryptedOperations();

    vector<int64_t> p1;
    p = FheDecrypt();

    m1[row[1]] = p1 = vector<int64_t>(p.begin(), p.begin() + MAT_SIZE);

    msgvector = m1[row[4]];

    FheEncrypt(msgvector);
    EncryptedOperations();

    vector<int64_t> p2;
    p = FheDecrypt();

    m1[row[0]] = p2 = vector<int64_t>(p.begin(), p.begin() + MAT_SIZE);

    vector<int> numVec;

    for (int i = 0; i < 5; i++)
        if (i == row[1])
        {
            numVec.push_back(VecToNum(p1));
        }

        else if (i == row[0])
        {
            numVec.push_back(VecToNum(p2));
        }

        else
            numVec.push_back(VecToNum(m1[i]));

    long int sum = accumulate(numVec.begin(), numVec.end(), 0);

    if (sum == userInp)
    {
        cout << "\n\nYou have mastered encrypted operatoins!!\n";
        cout << "Here's the flag: " << printFlag();
    }

    else
    {
        cout << "That was close, great going, But no flag for you!!\n\n";
        exit(0);
    }

    return 0;
}

//################################################################################################
//################################################################################################

long int calc_determinant(long int a, long int x)
{
    long int res = a * ((pow(a, 2) - (a * x * (-1)))) - -1 * ((pow(a, 2) * x) - (pow(x, 2) * a * (-1))) + 0 * ((pow(a * x, 2)) - (pow(a, 2) * pow(x, 2)));
    return res;
}

//-------------------------------------------------------------------------------------------------

void gen_hint(long int a, long int x)
{

    long int hint;
    char opt;
    vector<int64_t> v = {a, x};

    FheEncrypt(v);
    EncryptedOperations();
    v = FheDecrypt();

    cout << "\nchoose(+,-,*,/): ";
    cin >> opt;

    if (opt == '+')
        hint = v[0] + v[1];
    else if (opt == '*')
        hint = v[0] * v[1];
    else if (opt == '-')
        hint = v[0] - v[1];
    else if (opt == '/')
        hint = v[0] / v[1];
    else
    {
        cout << "\n\nERROR!! "
             << "Unrecognized Operation!!";
        exit(0);
    }

    cout << "\n\nHere you go: " << hint * (a * x) << "\n";
}

//################################################################################################
//################################################################################################

int level1()
{

    int SIZE = 20;
    int val = Genrand(1, 500);
    int idx;
    long int num;
    long int sum1 = 0;
    long int sum2 = 0;
    long int a = Genrand(1, 20);
    long int x = Genrand(1, 20);

    vector<vector<int>> m(SIZE, vector<int>(SIZE));
    vector<vector<int>> v(169, vector<int>(9));
    vector<int> mat;
    vector<int64_t> msgvector;

    cout << "                     =============================\n";
    cout << "                         --------LEVEL1--------\n";
    cout << "                     =============================\n";

    for (int x = 0; x < SIZE; x++)
    {
        for (int y = 0; y < SIZE; y++)
        {
            m[x][y] = ++val;
        }
    }

    int d = m.size();
    int r = 3;
    int c = 3;

    for (int i = 0; i < d - r + 1; i++)
    {
        for (int j = 0; j < d - c + 1; j++)
        {
            for (int p = 0; p < r; p++)
            {
                for (int q = 0; q < c; q++)
                {
                    mat.push_back(m[i + p][j + q]);
                }
            }
        }
    }

    for (int j = 0; j < int(mat.size()); j += 9)
    {
        v.push_back(slice(mat, j, j + 9));
    }

    idx = Genrand(0, v.size() - 1);
    vector<int64_t> temp1(begin(v[idx]), end(v[idx]));
    vector<int64_t> mvector = temp1;

    sum1 = accumulate(mvector.begin(), mvector.end(), 0);

    FheEncrypt(mvector);

    EncryptedOperations();

    vector<int64_t> p = FheDecrypt();

    if (sum1 == 0)
    {
        cout << "\n\nCHALLENGE CORRUPTED!!!!";
        exit(0);
    }

    if (p[0] == sum1)
        cout << "\n\nYou got all the encrypted operations right! Great!!\n\nNow on to the next\n\n";
    else
        exit(0);

    v = {};

    mat = {};
    r = 5;
    c = 4;

    for (int i = 0; i < d - r + 1; i++)
    {
        for (int j = 0; j < d - c + 1; j++)
        {
            for (int p = 0; p < r; p++)
            {
                for (int q = 0; q < c; q++)
                {
                    mat.push_back(m[i + p][j + q]);
                }
            }
        }
    }

    for (int j = 0; j < int(mat.size()); j += 20)
    {
        v.push_back(slice(mat, j, j + 20));
    }

    idx = Genrand(0, v.size() - 1);
    vector<int64_t> temp2(begin(v[idx]), end(v[idx]));
    vector<int64_t> mvector2 = temp2;

    sum2 = accumulate(mvector2.begin(), mvector2.end(), 0);

    num = mvector2[0];

    long int res = calc_determinant(a, 2 * x) - calc_determinant(a, x);
    gen_hint(a, x);

    cout << "This might make it easier: " << res * num << "\n\n";

    FheEncrypt(mvector2);

    EncryptedOperations();

    p = FheDecrypt();

    if (sum2 == 0)
    {
        cout << "\n\nCHALLENGE CORRUPTED!!!!";
        exit(0);
    }

    if (p[0] == sum2)
        cout << "Seems like you got a hang of this!!\nCongrats on completing the first level.\nGo get the flag!\n\n";
    else
        exit(0);

    return 0;
}

//#########################################################################################
//###################################### MAIN() ###########################################

int main()
{

    cout << "               _______________________________________\n";
    cout << "\n               WELCOME TO 'ENCRYPTED OPERATIONS SERVER'\n";
    cout << "               _______________________________________\n\n";

    cout << "\nThe server provides you with a set of operations to perform on encrypted data\n";
    cout << "All operations are performed on vector(long int) type data.\nThe server parses a string to convert it into vector\n";
    cout << "\n\nEx of vector input ->\n```Enter the operand vector: 12 13 14 15```\nThis will be parsed into `vector<int64_t>`\n\nLoading the service......\n\n";

    atexit(sayonara);

    int ret = level1();
    ret = level2();

    if (ret == 0)
        atexit(arigato);

    return 0;
}

//###############################------------------------------#############################
//##############################------------END-----------------############################

