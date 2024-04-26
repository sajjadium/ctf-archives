#include <type_traits>

struct nil_t {};

template<class T, class U>
struct cons {
    using car = T;
    using cdr = U;
};

template <class T>
using car_t = typename T::car;

template <class T>
using cdr_t = typename T::cdr;

template <class ... Ts>
struct list;

template <>
struct list<> {
    using type = nil_t;
};

template <class T, class ... Ts>
struct list<T, Ts...> {
    using type = cons<T, list<Ts...>>;
};

template <class ... Ts>
using list_t = typename list<Ts...>::type;

template <int v> struct V { static const constexpr int value = v ; };

template <int ... is>
struct int_list;

template <int i>
struct int_list<i> {
    using type = cons<V<i>, nil_t>;
};

template <int i, int ... is> 
struct int_list<i, is...> {
    using type = cons<V<i>, typename int_list<is...>::type>;
};

template <int ... is>
using int_list_t = typename int_list<is...>::type;


template <int i, typename T>
struct g;

template <int v, typename R>
struct g<0, cons<V<v>, R>> {
    static const constexpr int value = v;
};

template <int N, typename X, typename R>
struct g<N, cons<X, R>> {
    static const constexpr int value = g<N-1, R>::value;
};
template <typename S>
struct A;

template <int a, int b, typename rest>
struct A<cons<V<a>, cons<V<b>, rest>>> {
    using type = cons<V<a + b>, rest>;
};

template <typename S>
using A_t = typename A<S>::type;


template <typename S>
struct M;

template <int a, int b, typename rest>
struct M<cons<V<a>, cons<V<b>, rest>>> {
    using type = cons<V<a * b>, rest>;
};

template <typename S>
using M_t = typename M<S>::type;

template <int v, typename S>
struct P {
    using type = cons<V<v>, S>;
};

template <int v, typename S>
using P_t = typename P<v, S>::type;


template <int v, typename S>
struct T;

template <int v, int v_, typename R>
struct T<v, cons<V<v_>, R>> {
    using type = std::enable_if_t<v == v_, R>;
};

template <int v, typename S>
using T_t = typename T<v, S>::type;


template <typename S, typename IT, typename In>
struct vm;

template <typename S, typename In>
struct vm<S, nil_t, In> {
    using type = S;
};

template <typename S, typename R, typename In>
struct vm<S, cons<V<0>, R>, In>  {
    using type = typename vm<A_t<S>, R, In>::type;
};

template <typename S, typename R, typename In>
struct vm<S, cons<V<1>, R>, In>  {
    using type = typename vm<M_t<S>, R, In>::type;
};

template <typename S, int PV, typename R, typename In>
struct vm<S, cons<V<2>, cons<V<PV>, R>>, In>  {
    using type = typename vm<P_t<PV, S>, R, In>::type;
};

template <typename S, int N, typename R, typename In>
struct vm<S, cons<V<3>, cons<V<N>, R>>, In> {
    using type = typename vm<cons<V<g<N, In>::value>, S>, R, In>::type;
};

template <typename S, int PV, typename R, typename In>
struct vm<S, cons<V<4>, cons<V<PV>, R>>, In>  {
    using type = typename vm<T_t<PV, S>, R, In>::type;
};

template <typename S, typename IT, typename In>
using vm_t = typename vm<S, IT, In>::type;


