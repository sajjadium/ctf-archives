
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;

vector<int> comb(vector<int> in) {
    vector<int> out;
    for (int i = 0; i < in.size(); i++) {
        for (int j = i + 1; j < in.size(); j++) {
            out.push_back(in[i] * in[j]);
        }
        out.push_back((in[i] * (in[i] - 1) / 2));
    }
    return out;
}
int main() {
    ifstream fin("input.txt");
    ofstream fout("slow.out");
    int n, k;
    fin >> n >> k;
    vector<int> score;
    for (int i = 0; i < k; i++) {
        int temp;
        fin >> temp;
        score.push_back(temp);
    }
    for (int i = k; i < n; i++) {
        score.push_back(1);
    }
    uint64_t output = 0;
    for (int j = n; j >= k; j -= 3) {
        vector<int> part = vector<int>(score.begin(), score.begin() + j);
        vector<int> res = comb(comb(part));
        for (int i = 0; i < res.size(); i++) {
            output += res[i];
        }
    }
    fout << "bcactf{" << output << "}" << endl;
}