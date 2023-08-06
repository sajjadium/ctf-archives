#include <bits/stdc++.h>
#define int long long

using namespace std;

int N, A[500][500];
int tl = 0, tot = 0, ya = 0, xa = 0;

void test(int x, int y){
	ya = 0;
	xa = 0;
	tl = 0;
	tot = 0;
	for(int i = 0; i < N; i++){
		for(int j = 0; j < N; j++){
			ya += abs(j-y) * A[i][j];
			xa += abs(i-x) * A[i][j]; 
			if(j <= y) tl += A[i][j];
			tot += A[i][j];
		}
	}
}

void mvr(int x, int y){ // angular momentum
	int tr = tot - tl;
	ya += tl - tr;
	for(int i = 0; i < N; i++){
		tl += A[i][y];
	}
}

int solve(){
	int x = 0, y = 0, sum = 0;
	for(int i = 0; i < N; i++){
		for(int j = 0; j < N; j++){
			x += i * A[i][j];
			y += j * A[i][j];
			sum += A[i][j];
		}
	}
	int ans = 1e18;
	int mx = x/sum, my = y/sum;
	int r = max(1LL, (N-1)/2);
	for(int i = max(0LL, mx-r); i <= min(N-1, mx+r); i++){
		test(i, max(0LL, my-r));
		for(int j = max(0LL, my-r); j <= min(N-1, my+r); j++){
			ans = min(ans, xa + ya);
			mvr(i, j+1);
		}
	}
	return ans;
}

int check(){
	int ans = 1e18;
	for(int i = 0; i < N; i++){
		test(i, 0);
		for(int j = 0; j < N; j++){
			ans = min(ans, xa + ya);
			mvr(i, j+1);
		}
	}
	return ans;
}

int32_t main(){
	cin >> N;
	assert(N >= 1);
	assert(N <= 500);
	for(int i = 0; i < N; i++){
		for(int j = 0; j < N; j++){
			cin >> A[i][j];
			assert(A[i][j] >= 0);
			assert(A[i][j] <= 1000);
		}
	}
	ifstream f("flag.txt");
	if(solve() == check()){
		cout << "AC yay" << endl;
	}else{
		cout << "WA oops" << endl;
		cout << f.rdbuf() << endl;
	}
}