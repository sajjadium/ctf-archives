#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include <vector>

/*
	Based on KACTL's NTT, which is based on the excellent http://neerc.ifmo.ru/trains/toulouse/2017/fft2.pdf
*/

typedef long long ll;
const ll mod = (119 << 23) + 1, root = 62; // = 998244353

ll modpow(ll b, ll e) {
	ll ans = 1;
	for (; e; b = b * b % mod, e /= 2)
		if (e & 1) ans = ans * b % mod;
	return ans;
}

typedef std::vector<ll> vl;
typedef std::vector<int> vi;
void ntt(vl &a) {
	int n = a.size(), L = 31 - __builtin_clz(n);
	static vl rt(2, 1);
	for (static int k = 2, s = 2; k < n; k *= 2, s++) {
		rt.resize(n);
		ll z[] = {1, modpow(root, mod >> s)};
		for (size_t i = k; i < 2*k; ++i) {
			rt[i] = rt[i / 2] * z[i & 1] % mod;
		}
	}
	vi rev(n);
	for (size_t i = 0; i < n; ++i) {
		rev[i] = (rev[i / 2] | (i & 1) << L) / 2;
	}
	for (size_t i = 0; i < n; ++i) {
		if (i < rev[i]) std::swap(a[i], a[rev[i]]);
	}
	for (int k = 1; k < n; k *= 2) {
		for (int i = 0; i < n; i += 2 * k) {
			for (int j = 0; j < k; ++j) {
				ll z = rt[j + k] * a[i + j + k] % mod, &ai = a[i + j];
				a[i + j + k] = ai - z + (z > ai ? mod : 0);
				ai += (ai + z >= mod ? z - mod : z);
			}
		}
	}
}

vl conv(const vl &a, const vl &b) {
	if (a.empty() || b.empty()) return {};
	int s = a.size() + b.size() - 1, B = 32 - __builtin_clz(s),
	    n = 1 << B;
	int inv = modpow(n, mod - 2);
	vl L(a), R(b), out(n);
	L.resize(n), R.resize(n);
	ntt(L), ntt(R);
	for (int i = 0; i < n; ++i) {
		out[-i & (n - 1)] = (ll)L[i] * R[i] % mod * inv % mod;
	}
	ntt(out);

	return {out.begin(), out.begin() + s};
}

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(nttmul, m) {
	m.doc() = "Tehe maffs go brrr";

	m.def("conv", &conv, "Convolves two polynomials together");
}
