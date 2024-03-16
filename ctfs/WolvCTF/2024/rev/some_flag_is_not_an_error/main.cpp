template <int x, int y>
struct C {
  static constexpr int r = x;
  static constexpr int i = y;
};

template <typename X, typename ...vals>
struct V {
  using c = X;
  using n = V<vals...>;
  template <typename Y>
  using C = V<X,vals...,Y>;
};

template <typename X>
struct V<X> {
  using c = X;
  using n = void;
  template <typename Y>
  using C = V<X,Y>;
};

template<>
struct V<void> {
  using c = void;
  using n = void;
  template <typename Y>
  using C = V<Y>;
};

using secret = V<C<438, 3190>, C<102, 2664>, C<58, 2712>, C<229, 2954>, C<219, 3452>, C<69, 2647>, C<311, 3002>, C<303, 2647>, C<284, 2988>, C<3, 3081>, C<830, 3274>, C<-170, 2991>, C<66, 2729>, C<123, 2948>, C<99, 2967>, C<55, 2881>, C<-50, 2920>, C<169, 3152>, C<204, 2551>, C<328, 2709>, C<-99, 2753>, C<184, 2620>, C<165, 2893>, C<253, 2711>, C<298, 2443>, C<195, 3000>, C<2, 2595>, C<-164, 3003>, C<555, 2977>, C<-404, 2749>, C<146, 3079>, C<283, 2578>>;

template <unsigned i, unsigned a, unsigned b, unsigned c>
struct G {
  static constexpr unsigned A = (a * 171) % 30269;
  static constexpr unsigned B = (b * 172) % 30307;
  static constexpr unsigned C = (c * 170) % 30323;
  static constexpr unsigned v = G<i-1, A, B, C>::v;
};

template <unsigned a, unsigned b, unsigned c>
struct G<0, a, b, c> {
  static constexpr unsigned A = (a * 171) % 30269;
  static constexpr unsigned B = (b * 172) % 30307;
  static constexpr unsigned C = (c * 170) % 30323;
  static constexpr unsigned v = (A + B + C) % 32;
};

template <unsigned i>
using GR = G<i, 12643, 29806, 187>;

template <unsigned i>
using GI = G<i, 3823, 25188, 24854>;

template <typename T, unsigned i, unsigned j, unsigned k, typename ...vals>
struct B {
  using M = B<T, i, j-1, k, vals..., C<GR<i*k+j>::v, GI<i*k+j>::v>>::M;
};

template <typename T, unsigned j, unsigned k>
struct B<T, 0, j, k> {
  using M = T;
};

template <typename T, unsigned i, unsigned k, typename ...vals>
struct B<T, i, 0, k, vals...> {
  using M = B<typename T::template C<V<vals...>>, i-1, k, k>::M;
};

using W = B<V<void>, 32, 32, 32>::M;

struct _a {static constexpr int r = 0, i = 1;};
struct _b {static constexpr int r = 1, i = 0;};
struct _c {static constexpr int r = 2, i = 0;};
struct _d {static constexpr int r = 1, i = 1;};
struct _e {static constexpr int r = 0, i = 2;};
struct _f {static constexpr int r = 3, i = 0;};
struct _g {static constexpr int r = 2, i = 1;};
struct _h {static constexpr int r = 1, i = 2;};
struct _i {static constexpr int r = 0, i = 3;};
struct _j {static constexpr int r = 4, i = 0;};
struct _k {static constexpr int r = 3, i = 1;};
struct _l {static constexpr int r = 2, i = 2;};
struct _m {static constexpr int r = 1, i = 3;};
struct _n {static constexpr int r = 0, i = 4;};
struct _o {static constexpr int r = 5, i = 0;};
struct _p {static constexpr int r = 4, i = 1;};
struct _q {static constexpr int r = 3, i = 2;};
struct _r {static constexpr int r = 2, i = 3;};
struct _s {static constexpr int r = 1, i = 4;};
struct _t {static constexpr int r = 0, i = 5;};
struct _u {static constexpr int r = 6, i = 0;};
struct _v {static constexpr int r = 5, i = 1;};
struct _w {static constexpr int r = 4, i = 2;};
struct _x {static constexpr int r = 3, i = 3;};
struct _y {static constexpr int r = 2, i = 4;};
struct _z {static constexpr int r = 1, i = 5;};
struct _0 {static constexpr int r = 0, i = 6;};
struct _1 {static constexpr int r = 7, i = 0;};
struct _2 {static constexpr int r = 6, i = 1;};
struct _3 {static constexpr int r = 5, i = 2;};
struct _4 {static constexpr int r = 4, i = 3;};
struct _5 {static constexpr int r = 3, i = 4;};
struct _6 {static constexpr int r = 2, i = 5;};
struct _7 {static constexpr int r = 1, i = 6;};
struct _8 {static constexpr int r = 0, i = 7;};
struct _9 {static constexpr int r = 8, i = 0;};
struct __ {static constexpr int r = 7, i = 1;};

template <int L, int R>
struct S {
  static constexpr int v = L + R;
};

template <int L, int R, int M>
struct P {
  static constexpr int v = P<L&~M,R,M*2>::v+(L&M)*R;
};

template <int R, int M>
struct P<0, R, M> {
  static constexpr int v = 0;
};

template <typename L, typename R>
struct A {
  using r = C<S<L::r,R::r>::v, S<L::i,R::i>::v>;
};

template <typename L, typename R>
struct M {
  using r = C<S<P<L::r,R::r,1>::v,-P<L::i,R::i,1>::v>::v, S<P<L::r,R::i,1>::v,P<L::i,R::r,1>::v>::v>;
};

template <typename L, typename R>
struct D {
  using r = A<typename M<typename L::c,typename R::c>::r, typename D<typename L::n,typename R::n>::r>::r;
};

template <>
struct D<void, void> {
  using r = C<0, 0>;
};

template <typename L, typename R>
struct Z {
  using r = Z<typename L::n, R>::r::template C<typename D<typename L::c, R>::r>;
};

template <typename R>
struct Z<void, R> {
  using r = V<void>;
};

template <typename L, typename R>
struct E {
  static constexpr bool valid = (L::c::r == R::c::r) && (L::c::i == R::c::i) && E<typename L::n, typename R::n>::valid;
};

template<>
struct E<void, void> {
  static constexpr bool valid = true;
};

template <typename ...Ts>
struct wctf {
  static constexpr unsigned valid = E<typename Z<W, V<Ts...>>::r, secret>::valid;
};

int main() {
  static_assert(wctf<_w, _h, _4, _t, _5, __, _t, _h, _3, __, _f, _l, _4, _g>::valid);
}
