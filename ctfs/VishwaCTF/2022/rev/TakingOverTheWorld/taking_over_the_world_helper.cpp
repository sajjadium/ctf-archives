#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <map>
#include <algorithm>
#include <climits>

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::queue;
using std::multimap;
using std::min;

struct Node {
	int to, cap, rev;
	Node(int t, int c, int r) : to(t), cap(c), rev(r) {}
};

void die() {
	puts("Incorrect!");
	exit(1);
}

int vid(const int v, const bool o) {
	return v * 2 + (o ? 1 : 0);
}

void add_edge(const int i, 
				const int j, 
				const int c, 
				vector<vector<Node>> *adj) {
	(*adj)[i].emplace_back(j, c, (*adj)[j].size());
	(*adj)[j].emplace_back(i, 0, (*adj)[i].size() - 1);
}

vector<int> dijkstra(const vector<bool>& guard,
					 const vector<vector<int>>& A,
					 const int s) {
	vector<int> dst(A.size(), INT_MAX);
	multimap<int, int> que;
}

bool levelize(const int V, const int S, const int T,
			  vector<vector<Node>> *adj,
			  vector<int> *lev) {
}

vector<bool> min_cut(const int V, const int S,
					 const vector<vector<Node>>& adj) {

}

int taking_over_the_world() {
	int N, M, K; cin >> N >> M >> K;
	vector<vector<int>> A(N, vector<int>(N));
	for (int i = 0; i < M; ++i) {
		int u, v;
		cin >> u >> v;
		A[u][v] = A[v][u] = true;
	}

	const int GUARD = 1000;
	vector<bool> guard(N);
	while (true) {

		if (max_flow(V, S, T, &adj) <= K) {
		}
		} else {
			break;
		}
}

int main() {
	int T = 5;

	for (int test = 0; test < T; ++test) {

		int x = taking_over_the_world();
		if(num_array1[test] != x){
			die();
		}
		if(num_array2[test] != x){
			die();
		}
	}

	// false flag
	cout << "VishwaCTF{";
	for(int i = 0; i < T*2; i++){
	}
	cout << "}";
}