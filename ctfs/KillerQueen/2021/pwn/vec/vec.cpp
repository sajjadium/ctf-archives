#include <iostream>
#include <vector>
#include <assert.h>
using namespace std;
#define ll long long

const int mxn = 1000;

void answer(){
	int n, q;
	cin >> n >> q;
	assert(n >= 1 && n <= mxn);

	vector<ll> v;
	for(ll i = 0, x; i < n; i++) cin >> x, v.push_back(x);

	for(int i = 0; i < q; i++){
		int t;
		cin >> t;
		if(t & 1){
			ll x, y;
			cin >> x >> y;
			assert(x >= 0 && x <= n);
			v[--x] = y;
		}else{
			int x;
			cin >> x;
			x--;
			assert(x >= 0 && x <= n);
			cout << v[x] << endl;
		}
	}
}

int main(){
	int t;
	cin >> t;

	for(int i = 0; i < t; i++) answer();

	return 0;
}
