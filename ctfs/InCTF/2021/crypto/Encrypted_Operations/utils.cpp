#include <vector>
#include <string>
#include <random>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include <iostream>
#include <algorithm>

#include "homomorphic_system.cpp" // c++ pallisade library is used to implement FHE

homomorphic_system r1;
/* 
  If u want to check out pallisade library and test out is functionalities the following documentation specifies the build procedure :
    https://gitlab.com/palisade/palisade-release#build-instructions ( for installing pallisade locally )
    pls be aware that installation can take a while and and on PC's with lower specs might slow down PC performance drastically/crash during installation

    PLS NOTE: pallisade installation is NOT NECESSARY in any way for solving this challenge!
*/

CryptoContext<DCRTPoly> cryptoContext = r1.genCC();      // Generates the cryptocontext
LPKeyPair<DCRTPoly> keyPair = r1.genKeys(cryptoContext); // Generates the private key

//################################################################################################

int VecToNum(vector<int64_t> vec)
{
    std::vector<int> values(begin(vec), end(vec));

    int res = std::accumulate(values.begin(), values.end(), 0, [](int acc, int val)
                              { return 10 * acc + val; });

    return res;
}

//################################################################################################

int Genrand(int lr, int hr)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(lr, hr);

    int rnum = distr(gen);
    return rnum;
}

//################################################################################################

vector<int> slice(const vector<int> &v, int start = 0, int end = -1)
{
    int olen = v.size();
    int nlen;

    if (end == -1 or end >= olen)
    {
        nlen = olen - start;
    }
    else
    {
        nlen = end - start;
    }

    vector<int> nv(nlen);

    for (int i = 0; i < nlen; i++)
    {
        nv[i] = v[start + i];
    }

    return nv;
}

//################################################################################################

/* operations list:
   - '+' adds operand vector to encrypted vector 
   - '*' multiplies operand vector to encrypted vector
   - '<' shifts the elements of encrypted vector to left by value specified in 'samt'
   - '>' shifts elements of encrypted vector to right by value specified in 'samt'
*/
/* eg operation:

    if the following vector -> {1,1,1,1} is encrypted
    and operand vector is given as {-2,-2,-2,-2} 
    operations is '+'
    shift amount can be any value in specified range ( since not used )
    resultant vector after decrypting will be {-1,-1,-1,-1}
    
    if above operation was '<'
    samt = 1
    resultant vector after decrypting will be {1,1,1,0}
    while shifting operand vector can be given as 0 i.e {0} as it is not used
 */

void EncryptedOperations()
{
    char choice = 'y';
    char operation; // '+','*','<',">"
    int samt;       // shift amount
    int cnt = 0;

    std::cout << "\n\nThe plaintext has been encrypted.\n\n"
              << std::flush;
    ;

    while (choice == 'y' && cnt < 4)
    {
        std::cout << "\nEnter the operand vector: " << std::flush;
        std::string s;
        std::getline(std::cin >> std::ws, s);

        std::stringstream iss(s);
        int number;
        std::vector<int64_t> operandVector;
        while (iss >> number)
            operandVector.push_back(number);

        assert(1 <= operandVector.size() && operandVector.size() <= 20);

        std::cout << "\nSpecify Operation: ";
        std::cin >> operation;

        std::cout << "\nEnter shift amount: ";
        std::cin >> samt;

        assert(1 <= samt && samt < 20);

        r1.compute(cryptoContext, operation, samt, operandVector); // performs the operation specified on encrypted vector/ on encrypted and operand vector

        std::cout << "\nperform another operation(y/n): ";
        std::cin >> choice;

        assert(choice == 'y' || choice == 'n');
        cnt += 1;
    };
    std::cout << "\n";
}

//################################################################################################

// msg vector is encrypted using fhe

void FheEncrypt(vector<int64_t> msgvector)
{
    r1.genCiphertexts(msgvector, keyPair, cryptoContext);
}

//################################################################################################

// resultant vector after performing the operations is decrypted

vector<int64_t> FheDecrypt()
{
    std::vector<int64_t> dt;
    dt = r1.decrypt(keyPair, cryptoContext);

    return dt;
}

//################################################################################################

std::string printFlag()
{
    std::fstream flagfile;
    flagfile.open("flag.txt", std::ios::in);

    std::string flag;
    if (flagfile.is_open())
    {

        std::string l;
        while (getline(flagfile, l))
        {
            flag += l;
        }

        flagfile.close();
    }

    return flag;
}

//################################################################################################

void sayonara(void)
{
    std::cout << "\n\n\nExiting!!";
}

//################################################################################################

void arigato(void)
{
    std::cout << "\n\n\n"
              << "Thankyou for using the service! Sucessfully performed all operatoions!!";
}

//#############################--------------------------------#####################################
//#############################--------------END---------------#####################################
