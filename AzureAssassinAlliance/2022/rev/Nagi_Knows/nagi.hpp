#include <type_traits>

struct XW
{
    typedef int type;
};

struct SH
{
    typedef float type;
};

template <bool B, typename T, typename U>
struct NH
{
    typedef U type;
};

template <typename T, typename U>
struct NH<true, T, U>
{
    typedef T type;
};

template <int N>
struct CM
{
    static constexpr int value = N;
};

template <bool B>
struct AW
{
    static constexpr bool value = B;
};

typedef AW<false> IE;
typedef AW<true> QC;

template <typename T>
struct RO : AW<!bool(T::value)>
{
};

template <typename...>
struct HI : QC
{
};

template <typename T>
struct HI<T> : T
{
};

template <typename T, typename... U>
struct HI<T, U...> : NH<bool(T::value), HI<U...>, T>::type
{
};

template <typename T, typename... U>
struct JS : NH<bool(T::value), RO<JS<U...>>, JS<U...>>::type
{
};

template <typename T>
struct JS<T> : T
{
};

template <bool B, typename = void>
struct WH {
};

template <typename T>
struct WH<true, T> {
    typedef T type;
};

template<typename T, typename U>
struct IM :IE {
};

template<typename T>
struct IM<T, T> :QC {
};

template <typename T>
struct JJ
{
    typedef typename std::remove_reference<T>::type type;
};

template <typename T>
struct SY
{
    typedef typename std::add_lvalue_reference<T>::type type;
};

template <typename T, typename = void>
struct VT : IE
{
};

template <typename T>
struct VT<T, typename WH<std::is_reference<T>::value>::type> : QC
{
};

template <typename T, typename = void>
struct UY
{
    typedef typename std::remove_const<T>::type type;
};

template <typename T>
struct UY<T, typename WH<VT<T>::value>::type>
{
    typedef typename SY<typename std::remove_const<typename JJ<T>::type>::type>::type type;
};

template <typename T, typename = void>
struct XL
{
    typedef typename std::add_const<T>::type type;
};

template <typename T>
struct XL<T, typename WH<VT<T>::value>::type>
{
    typedef typename SY<typename std::add_const<typename JJ<T>::type>::type>::type type;
};

template <typename T, typename = void>
struct KE : IE
{
};

template <typename T>
struct KE<T, typename WH<std::is_const<typename JJ<T>::type>::value>::type>
    : QC
{
};

template <typename T, typename = void>
struct RZ
{
    typedef XW::type type;
};

template <typename T>
struct RZ<T,
    typename WH<HI<KE<T>, RO<VT<T>>>::value>::type>
{
    typedef typename XL<XW::type>::type type;
};

template <typename T>
struct RZ<T,
    typename WH<HI<RO<KE<T>>, VT<T>>::value>::type>
{
    typedef typename SY<XW::type>::type type;
};

template <typename T>
struct RZ<T,
    typename WH<HI<KE<T>, VT<T>>::value>::type>
{
    typedef typename SY<typename XL<XW::type>::type>::type type;
};

template <typename T, typename = void>
struct EK
{
    typedef SH::type type;
};

template <typename T>
struct EK<T,
    typename WH<HI<KE<T>, RO<VT<T>>>::value>::type>
{
    typedef typename XL<SH::type>::type type;
};

template <typename T>
struct EK<T,
    typename WH<HI<RO<KE<T>>, VT<T>>::value>::type>
{
    typedef typename SY<SH::type>::type type;
};

template <typename T>
struct EK<T,
    typename WH<HI<KE<T>, VT<T>>::value>::type>
{
    typedef typename SY<typename XL<SH::type>::type>::type type;
};

template <typename T, typename = void>
struct CK : IE
{
};

template <typename T>
struct CK<T, typename WH<IM<typename UY<typename JJ<T>::type>::type, SH::type>::value>::type> : QC
{
};

template <typename T, typename U, typename = void>
struct NM
{
    typedef SH::type type;
};

template <typename T, typename U>
struct NM<T, U, typename WH<RO<JS<CK<T>, CK<U>>>::value>::type>
{
    typedef XW::type type;
};

template <typename T, typename U, typename = void>
struct TZ
{
    typedef typename XL<typename NM<T, U>::type>::type type;
};

template <typename T, typename U>
struct TZ<T, U, typename WH<RO<JS<KE<T>, KE<U>>>::value>::type>
{
    typedef typename UY<typename NM<T, U>::type>::type type;
};

template <typename T, typename U, typename = void>
struct BY
{
    typedef typename SY<typename TZ<T, U>::type>::type type;
};

template <typename T, typename U>
struct BY<T, U, typename WH<RO<JS<VT<T>, VT<U>>>::value>::type>
{
    typedef typename JJ<typename TZ<T, U>::type>::type type;
};

template <typename T, typename... U>
struct IC
{
    typedef typename BY<T, typename IC<U...>::type>::type type;
};

template <typename T>
struct IC<T>
{
    typedef T type;
};

template<typename T>
struct NV {
    typedef typename NH<VT<T>::value, SH::type, XW::type>::type type;
};

template<typename T>
struct YQ {
    typedef typename NH<CK<T>::value, typename XL<typename NV<T>::type>::type, typename NV<T>::type>::type type;
};


template <typename T>
struct ZT
{
    typedef typename NH<JS<VT<T>, KE<T>>::value, typename SY<typename YQ<T>::type>::type, typename YQ<T>::type>::type type;
};

template<typename T>
struct HY {
    typedef typename NH<JS<VT<T>, KE<T>>::value, SH::type, XW::type>::type type;
};

template<typename T>
struct PG {
    typedef typename NH<VT<T>::value, typename XL<typename HY<T>::type>::type, typename HY<T>::type>::type type;
};

template <typename T>
struct RX
{
    typedef typename NH<JS<VT<T>, KE<T>, CK<T>>::value, typename SY<typename PG<T>::type>::type, typename PG<T>::type>::type type;
};

template <typename T, typename U, typename = void>
struct WP
{
    typedef XW::type type;
};

template <typename T, typename U>
struct WP<T, U, typename WH<CK<U>::value>::type>
{
    typedef T type;
};

template <typename T, typename U, typename = void>
struct WX
{
    typedef typename WP<T, U>::type type;
};

template <typename T, typename U>
struct WX<T, U, typename WH<KE<U>::value>::type>
{
    typedef typename IC<typename ZT<T>::type, typename WP<T, U>::type>::type type;
};

template <typename T, typename U, typename = void>
struct GR
{
    typedef typename WX<T, U>::type type;
};

template <typename T, typename U>
struct GR<T, U, typename WH<VT<U>::value>::type>
{
    typedef typename IC<typename RX<T>::type, typename WX<T, U>::type>::type type;
};

template <typename T, typename... U>
struct HN
{
    typedef typename GR<T, typename HN<U...>::type>::type type;
};

template <typename T>
struct HN<T>
{
    typedef T type;
};

template<typename T>
struct PZ {
    typedef typename HN<XW::type, T>::type type;
};

template<typename T>
struct RJ {
    typedef typename HN<SH::type, T>::type type;
};

template<typename T>
struct KH {
    typedef typename HN<XL<XW::type>::type, T>::type type;
};

template<typename T>
struct TO {
    typedef typename HN<XL<SH::type>::type, T>::type type;
};

template<typename T>
struct UI {
    typedef typename HN<XL<XW::type>::type, T, XL<XW::type>::type>::type type;
};

template<typename T>
struct UD {
    typedef typename HN<XL<SH::type>::type, XL<SH::type>::type, T>::type type;
};

template<typename T>
struct TC {
    typedef typename HN<XL<XW::type>::type, T, XL<SH::type>::type>::type type;
};

template<typename T>
struct VG {
    typedef typename HN<XL<XW::type>::type, T, XL<XW::type>::type, XL<XW::type>::type, XL<XW::type>::type>::type type;
};

template<typename U, typename V, typename W, typename X>
struct IQ {
    typedef typename IC<typename UI<U>::type, typename TC<V>::type, XW::type, typename VG<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct BX {
    typedef typename IC<typename PZ<U>::type, typename PZ<V>::type, XW::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct AX {
    typedef typename IC<typename TC<U>::type, typename KH<V>::type, XW::type, typename UD<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct UW {
    typedef typename IC<typename TO<U>::type, typename VG<V>::type, XW::type, typename VG<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct HC {
    typedef typename IC<typename TO<U>::type, typename RJ<V>::type, XW::type, typename TC<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct NN {
    typedef typename IC<typename PZ<U>::type, typename PZ<V>::type, XW::type, typename UI<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct UC {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, XW::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct OK {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, XW::type, typename TO<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct PY {
    typedef typename IC<typename KH<U>::type, typename RJ<V>::type, XW::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct XF {
    typedef typename IC<typename RJ<U>::type, typename KH<V>::type, XW::type, typename UI<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct KC {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, XW::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct VM {
    typedef typename IC<typename UI<U>::type, typename RJ<V>::type, XW::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct OW {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, XW::type, typename PZ<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct XQ {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, XW::type, typename UD<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct MG {
    typedef typename IC<typename TO<U>::type, typename UI<V>::type, XW::type, typename VG<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct SQ {
    typedef typename IC<typename UD<U>::type, typename VG<V>::type, XW::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct UZ {
    typedef typename IC<typename RJ<U>::type, typename UI<V>::type, XW::type, typename PZ<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct JT {
    typedef typename IC<typename RJ<U>::type, typename TO<V>::type, XW::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct ES {
    typedef typename IC<typename KH<U>::type, typename UI<V>::type, XW::type, typename TO<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct GJ {
    typedef typename IC<typename TC<U>::type, typename PZ<V>::type, XW::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct NJ {
    typedef typename IC<typename UI<U>::type, typename KH<V>::type, XW::type, typename PZ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct KM {
    typedef typename IC<typename RJ<U>::type, typename UI<V>::type, XW::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct YZ {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, XW::type, typename TC<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct WA {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, XW::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct CW {
    typedef typename IC<typename UD<U>::type, typename KH<V>::type, XW::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct OP {
    typedef typename IC<typename TC<U>::type, typename RJ<V>::type, XW::type, typename UD<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct SI {
    typedef typename IC<typename PZ<U>::type, typename UI<V>::type, XW::type, typename UD<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct WI {
    typedef typename IC<typename PZ<U>::type, typename RJ<V>::type, XW::type, typename RJ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct FY {
    typedef typename IC<typename UI<U>::type, typename PZ<V>::type, XW::type, typename VG<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct XK {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, XW::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct EY {
    typedef typename IC<typename PZ<U>::type, typename TC<V>::type, XW::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X>
struct XS {
    typedef typename IC<typename KH<U>::type, typename VG<V>::type, XW::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UX {
    typedef typename IC<typename PZ<U>::type, typename RJ<V>::type, typename IQ<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DY {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename BX<Y...>::type, typename TC<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LJ {
    typedef typename IC<typename PZ<U>::type, typename PZ<V>::type, typename AX<Y...>::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NB {
    typedef typename IC<typename TO<U>::type, typename RJ<V>::type, typename UW<Y...>::type, typename TC<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZQ {
    typedef typename IC<typename KH<U>::type, typename RJ<V>::type, typename HC<Y...>::type, typename KH<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FZ {
    typedef typename IC<typename TC<U>::type, typename PZ<V>::type, typename NN<Y...>::type, typename VG<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SM {
    typedef typename IC<typename UI<U>::type, typename UD<V>::type, typename UC<Y...>::type, typename KH<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MC {
    typedef typename IC<typename PZ<U>::type, typename TC<V>::type, typename OK<Y...>::type, typename PZ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BZ {
    typedef typename IC<typename RJ<U>::type, typename UI<V>::type, typename PY<Y...>::type, typename VG<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LR {
    typedef typename IC<typename TO<U>::type, typename PZ<V>::type, typename XF<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BQ {
    typedef typename IC<typename PZ<U>::type, typename KH<V>::type, typename KC<Y...>::type, typename UD<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FO {
    typedef typename IC<typename UD<U>::type, typename UD<V>::type, typename VM<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HS {
    typedef typename IC<typename VG<U>::type, typename PZ<V>::type, typename OW<Y...>::type, typename VG<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CT {
    typedef typename IC<typename UD<U>::type, typename KH<V>::type, typename XQ<Y...>::type, typename TC<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AK {
    typedef typename IC<typename RJ<U>::type, typename KH<V>::type, typename MG<Y...>::type, typename TC<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OD {
    typedef typename IC<typename VG<U>::type, typename TO<V>::type, typename SQ<Y...>::type, typename VG<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KP {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, typename UZ<Y...>::type, typename TC<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZH {
    typedef typename IC<typename KH<U>::type, typename TO<V>::type, typename JT<Y...>::type, typename PZ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XJ {
    typedef typename IC<typename UD<U>::type, typename UD<V>::type, typename ES<Y...>::type, typename UI<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DP {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, typename GJ<Y...>::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RP {
    typedef typename IC<typename TC<U>::type, typename TC<V>::type, typename NJ<Y...>::type, typename TC<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LY {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, typename KM<Y...>::type, typename UD<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UP {
    typedef typename IC<typename UI<U>::type, typename UD<V>::type, typename YZ<Y...>::type, typename UD<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QN {
    typedef typename IC<typename UI<U>::type, typename UD<V>::type, typename WA<Y...>::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SF {
    typedef typename IC<typename PZ<U>::type, typename UD<V>::type, typename CW<Y...>::type, typename TO<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PM {
    typedef typename IC<typename VG<U>::type, typename TO<V>::type, typename OP<Y...>::type, typename TC<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CU {
    typedef typename IC<typename PZ<U>::type, typename VG<V>::type, typename SI<Y...>::type, typename UD<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LM {
    typedef typename IC<typename KH<U>::type, typename UD<V>::type, typename WI<Y...>::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DG {
    typedef typename IC<typename RJ<U>::type, typename VG<V>::type, typename FY<Y...>::type, typename RJ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AP {
    typedef typename IC<typename KH<U>::type, typename RJ<V>::type, typename XK<Y...>::type, typename UI<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PA {
    typedef typename IC<typename TC<U>::type, typename KH<V>::type, typename EY<Y...>::type, typename TC<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RR {
    typedef typename IC<typename TC<U>::type, typename TO<V>::type, typename XS<Y...>::type, typename VG<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WE {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename UX<Y...>::type, typename UI<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GS {
    typedef typename IC<typename UD<U>::type, typename KH<V>::type, typename DY<Y...>::type, typename VG<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WO {
    typedef typename IC<typename KH<U>::type, typename TO<V>::type, typename LJ<Y...>::type, typename TC<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VX {
    typedef typename IC<typename UI<U>::type, typename TC<V>::type, typename NB<Y...>::type, typename TC<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KJ {
    typedef typename IC<typename KH<U>::type, typename RJ<V>::type, typename ZQ<Y...>::type, typename VG<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AH {
    typedef typename IC<typename UI<U>::type, typename TC<V>::type, typename FZ<Y...>::type, typename RJ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MV {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename SM<Y...>::type, typename PZ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TF {
    typedef typename IC<typename UD<U>::type, typename TO<V>::type, typename MC<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZX {
    typedef typename IC<typename VG<U>::type, typename RJ<V>::type, typename BZ<Y...>::type, typename UD<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AU {
    typedef typename IC<typename KH<U>::type, typename UD<V>::type, typename LR<Y...>::type, typename VG<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YX {
    typedef typename IC<typename TC<U>::type, typename TO<V>::type, typename BQ<Y...>::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KL {
    typedef typename IC<typename UD<U>::type, typename VG<V>::type, typename FO<Y...>::type, typename UD<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LI {
    typedef typename IC<typename PZ<U>::type, typename VG<V>::type, typename HS<Y...>::type, typename UD<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OU {
    typedef typename IC<typename TC<U>::type, typename RJ<V>::type, typename CT<Y...>::type, typename TO<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct IH {
    typedef typename IC<typename KH<U>::type, typename VG<V>::type, typename AK<Y...>::type, typename TC<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SU {
    typedef typename IC<typename TO<U>::type, typename PZ<V>::type, typename OD<Y...>::type, typename VG<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OT {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename KP<Y...>::type, typename TC<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AJ {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, typename ZH<Y...>::type, typename TC<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WK {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, typename XJ<Y...>::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VL {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename DP<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BW {
    typedef typename IC<typename PZ<U>::type, typename VG<V>::type, typename RP<Y...>::type, typename TC<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MP {
    typedef typename IC<typename RJ<U>::type, typename KH<V>::type, typename LY<Y...>::type, typename KH<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FD {
    typedef typename IC<typename RJ<U>::type, typename UI<V>::type, typename UP<Y...>::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DZ {
    typedef typename IC<typename VG<U>::type, typename TO<V>::type, typename QN<Y...>::type, typename RJ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UV {
    typedef typename IC<typename PZ<U>::type, typename RJ<V>::type, typename SF<Y...>::type, typename UD<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YJ {
    typedef typename IC<typename PZ<U>::type, typename RJ<V>::type, typename PM<Y...>::type, typename PZ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DW {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename CU<Y...>::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AN {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, typename LM<Y...>::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TL {
    typedef typename IC<typename TC<U>::type, typename PZ<V>::type, typename DG<Y...>::type, typename UD<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AE {
    typedef typename IC<typename VG<U>::type, typename RJ<V>::type, typename AP<Y...>::type, typename TO<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OA {
    typedef typename IC<typename UI<U>::type, typename TO<V>::type, typename PA<Y...>::type, typename UD<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UG {
    typedef typename IC<typename UI<U>::type, typename TO<V>::type, typename RR<Y...>::type, typename KH<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BK {
    typedef typename IC<typename UI<U>::type, typename KH<V>::type, typename WE<Y...>::type, typename PZ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FJ {
    typedef typename IC<typename RJ<U>::type, typename TO<V>::type, typename GS<Y...>::type, typename UD<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NR {
    typedef typename IC<typename UD<U>::type, typename UI<V>::type, typename WO<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UT {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, typename VX<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EW {
    typedef typename IC<typename UD<U>::type, typename PZ<V>::type, typename KJ<Y...>::type, typename TO<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QP {
    typedef typename IC<typename VG<U>::type, typename RJ<V>::type, typename AH<Y...>::type, typename TC<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LF {
    typedef typename IC<typename TC<U>::type, typename PZ<V>::type, typename MV<Y...>::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FL {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, typename TF<Y...>::type, typename VG<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TU {
    typedef typename IC<typename TO<U>::type, typename RJ<V>::type, typename ZX<Y...>::type, typename UI<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BU {
    typedef typename IC<typename RJ<U>::type, typename VG<V>::type, typename AU<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HF {
    typedef typename IC<typename PZ<U>::type, typename UD<V>::type, typename YX<Y...>::type, typename UI<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MK {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename KL<Y...>::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SK {
    typedef typename IC<typename TO<U>::type, typename UD<V>::type, typename LI<Y...>::type, typename UI<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OH {
    typedef typename IC<typename KH<U>::type, typename KH<V>::type, typename OU<Y...>::type, typename UI<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RK {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, typename IH<Y...>::type, typename TC<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MA {
    typedef typename IC<typename VG<U>::type, typename VG<V>::type, typename SU<Y...>::type, typename KH<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NX {
    typedef typename IC<typename TC<U>::type, typename TC<V>::type, typename OT<Y...>::type, typename TC<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct JW {
    typedef typename IC<typename TC<U>::type, typename TC<V>::type, typename AJ<Y...>::type, typename TC<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LS {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, typename WK<Y...>::type, typename UI<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PQ {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename VL<Y...>::type, typename TC<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MN {
    typedef typename IC<typename KH<U>::type, typename VG<V>::type, typename BW<Y...>::type, typename VG<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BR {
    typedef typename IC<typename PZ<U>::type, typename UD<V>::type, typename MP<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OI {
    typedef typename IC<typename VG<U>::type, typename TC<V>::type, typename FD<Y...>::type, typename PZ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RM {
    typedef typename IC<typename VG<U>::type, typename TO<V>::type, typename DZ<Y...>::type, typename UD<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RY {
    typedef typename IC<typename UD<U>::type, typename PZ<V>::type, typename UV<Y...>::type, typename RJ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NY {
    typedef typename IC<typename UI<U>::type, typename PZ<V>::type, typename YJ<Y...>::type, typename VG<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WN {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename DW<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UH {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename AN<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QX {
    typedef typename IC<typename KH<U>::type, typename TC<V>::type, typename TL<Y...>::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FI {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename AE<Y...>::type, typename UD<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UR {
    typedef typename IC<typename RJ<U>::type, typename UI<V>::type, typename OA<Y...>::type, typename UD<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KG {
    typedef typename IC<typename TC<U>::type, typename PZ<V>::type, typename UG<Y...>::type, typename TC<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NA {
    typedef typename IC<typename UD<U>::type, typename UD<V>::type, typename BK<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TI {
    typedef typename IC<typename KH<U>::type, typename UD<V>::type, typename FJ<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GA {
    typedef typename IC<typename TO<U>::type, typename RJ<V>::type, typename NR<Y...>::type, typename RJ<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PC {
    typedef typename IC<typename UD<U>::type, typename RJ<V>::type, typename UT<Y...>::type, typename VG<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VN {
    typedef typename IC<typename UD<U>::type, typename UD<V>::type, typename EW<Y...>::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GN {
    typedef typename IC<typename KH<U>::type, typename TO<V>::type, typename QP<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CO {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename LF<Y...>::type, typename UD<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YD {
    typedef typename IC<typename PZ<U>::type, typename VG<V>::type, typename FL<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PI {
    typedef typename IC<typename UD<U>::type, typename UI<V>::type, typename TU<Y...>::type, typename TC<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RW {
    typedef typename IC<typename UD<U>::type, typename KH<V>::type, typename BU<Y...>::type, typename PZ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HT {
    typedef typename IC<typename TO<U>::type, typename UI<V>::type, typename HF<Y...>::type, typename RJ<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct US {
    typedef typename IC<typename VG<U>::type, typename PZ<V>::type, typename MK<Y...>::type, typename VG<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YG {
    typedef typename IC<typename UD<U>::type, typename TC<V>::type, typename SK<Y...>::type, typename UI<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CI {
    typedef typename IC<typename UD<U>::type, typename UI<V>::type, typename OH<Y...>::type, typename UD<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OS {
    typedef typename IC<typename VG<U>::type, typename RJ<V>::type, typename RK<Y...>::type, typename RJ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CN {
    typedef typename IC<typename KH<U>::type, typename PZ<V>::type, typename MA<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EB {
    typedef typename IC<typename TO<U>::type, typename UI<V>::type, typename NX<Y...>::type, typename UI<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct JC {
    typedef typename IC<typename VG<U>::type, typename PZ<V>::type, typename JW<Y...>::type, typename VG<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DD {
    typedef typename IC<typename RJ<U>::type, typename VG<V>::type, typename LS<Y...>::type, typename UI<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FP {
    typedef typename IC<typename UD<U>::type, typename RJ<V>::type, typename PQ<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NF {
    typedef typename IC<typename KH<U>::type, typename PZ<V>::type, typename MN<Y...>::type, typename VG<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QE {
    typedef typename IC<typename UD<U>::type, typename VG<V>::type, typename BR<Y...>::type, typename VG<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZS {
    typedef typename IC<typename UI<U>::type, typename PZ<V>::type, typename OI<Y...>::type, typename RJ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FG {
    typedef typename IC<typename UI<U>::type, typename TO<V>::type, typename RM<Y...>::type, typename UD<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AM {
    typedef typename IC<typename UD<U>::type, typename TC<V>::type, typename RY<Y...>::type, typename UI<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QD {
    typedef typename IC<typename UI<U>::type, typename UD<V>::type, typename NY<Y...>::type, typename UD<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct IV {
    typedef typename IC<typename UD<U>::type, typename UD<V>::type, typename WN<Y...>::type, typename PZ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CR {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename UH<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FC {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, typename QX<Y...>::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TP {
    typedef typename IC<typename KH<U>::type, typename PZ<V>::type, typename FI<Y...>::type, typename PZ<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MO {
    typedef typename IC<typename KH<U>::type, typename KH<V>::type, typename UR<Y...>::type, typename RJ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XO {
    typedef typename IC<typename TO<U>::type, typename VG<V>::type, typename KG<Y...>::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SO {
    typedef typename IC<typename TO<U>::type, typename PZ<V>::type, typename NA<Y...>::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LA {
    typedef typename IC<typename TO<U>::type, typename TC<V>::type, typename TI<Y...>::type, typename UD<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QH {
    typedef typename IC<typename TO<U>::type, typename TC<V>::type, typename GA<Y...>::type, typename RJ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PB {
    typedef typename IC<typename RJ<U>::type, typename UD<V>::type, typename PC<Y...>::type, typename UD<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AF {
    typedef typename IC<typename KH<U>::type, typename KH<V>::type, typename VN<Y...>::type, typename VG<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EM {
    typedef typename IC<typename KH<U>::type, typename VG<V>::type, typename GN<Y...>::type, typename VG<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RB {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename CO<Y...>::type, typename RJ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BJ {
    typedef typename IC<typename UI<U>::type, typename UD<V>::type, typename YD<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XZ {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, typename PI<Y...>::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MH {
    typedef typename IC<typename UD<U>::type, typename TC<V>::type, typename RW<Y...>::type, typename TO<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CD {
    typedef typename IC<typename TC<U>::type, typename TO<V>::type, typename HT<Y...>::type, typename UD<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OQ {
    typedef typename IC<typename TO<U>::type, typename TO<V>::type, typename US<Y...>::type, typename VG<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VJ {
    typedef typename IC<typename PZ<U>::type, typename UD<V>::type, typename YG<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct JX {
    typedef typename IC<typename UI<U>::type, typename PZ<V>::type, typename CI<Y...>::type, typename PZ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HK {
    typedef typename IC<typename TC<U>::type, typename TO<V>::type, typename OS<Y...>::type, typename UI<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PF {
    typedef typename IC<typename KH<U>::type, typename TO<V>::type, typename CN<Y...>::type, typename KH<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YH {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename EB<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct JK {
    typedef typename IC<typename TC<U>::type, typename KH<V>::type, typename JC<Y...>::type, typename RJ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MX {
    typedef typename IC<typename UI<U>::type, typename TC<V>::type, typename DD<Y...>::type, typename RJ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct IB {
    typedef typename IC<typename PZ<U>::type, typename TC<V>::type, typename FP<Y...>::type, typename UI<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DK {
    typedef typename IC<typename TO<U>::type, typename UI<V>::type, typename NF<Y...>::type, typename KH<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BV {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename QE<Y...>::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VW {
    typedef typename IC<typename UI<U>::type, typename TC<V>::type, typename ZS<Y...>::type, typename RJ<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SA {
    typedef typename IC<typename TO<U>::type, typename VG<V>::type, typename FG<Y...>::type, typename TO<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VO {
    typedef typename IC<typename PZ<U>::type, typename VG<V>::type, typename AM<Y...>::type, typename KH<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QT {
    typedef typename IC<typename TC<U>::type, typename KH<V>::type, typename QD<Y...>::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BI {
    typedef typename IC<typename UD<U>::type, typename UI<V>::type, typename IV<Y...>::type, typename TO<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KX {
    typedef typename IC<typename KH<U>::type, typename VG<V>::type, typename CR<Y...>::type, typename VG<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CZ {
    typedef typename IC<typename KH<U>::type, typename KH<V>::type, typename FC<Y...>::type, typename TC<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct RD {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename TP<Y...>::type, typename KH<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YF {
    typedef typename IC<typename KH<U>::type, typename VG<V>::type, typename MO<Y...>::type, typename KH<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ON {
    typedef typename IC<typename TC<U>::type, typename RJ<V>::type, typename XO<Y...>::type, typename TC<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct VS {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename SO<Y...>::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KV {
    typedef typename IC<typename UD<U>::type, typename UD<V>::type, typename LA<Y...>::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZC {
    typedef typename IC<typename UI<U>::type, typename VG<V>::type, typename QH<Y...>::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PD {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename PB<Y...>::type, typename PZ<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AS {
    typedef typename IC<typename RJ<U>::type, typename KH<V>::type, typename AF<Y...>::type, typename RJ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct IT {
    typedef typename IC<typename UD<U>::type, typename PZ<V>::type, typename EM<Y...>::type, typename UI<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LB {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename RB<Y...>::type, typename RJ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct LC {
    typedef typename IC<typename PZ<U>::type, typename UI<V>::type, typename BJ<Y...>::type, typename RJ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GC {
    typedef typename IC<typename KH<U>::type, typename UD<V>::type, typename XZ<Y...>::type, typename PZ<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DV {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename MH<Y...>::type, typename TC<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QA {
    typedef typename IC<typename RJ<U>::type, typename KH<V>::type, typename CD<Y...>::type, typename TO<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EC {
    typedef typename IC<typename RJ<U>::type, typename TO<V>::type, typename OQ<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WY {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, typename VJ<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HO {
    typedef typename IC<typename KH<U>::type, typename RJ<V>::type, typename JX<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FR {
    typedef typename IC<typename VG<U>::type, typename TC<V>::type, typename HK<Y...>::type, typename PZ<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KZ {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename PF<Y...>::type, typename VG<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HL {
    typedef typename IC<typename UI<U>::type, typename VG<V>::type, typename YH<Y...>::type, typename UD<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZW {
    typedef typename IC<typename TO<U>::type, typename TC<V>::type, typename JK<Y...>::type, typename VG<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CV {
    typedef typename IC<typename TO<U>::type, typename VG<V>::type, typename MX<Y...>::type, typename RJ<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct KT {
    typedef typename IC<typename UI<U>::type, typename UD<V>::type, typename IB<Y...>::type, typename VG<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AA {
    typedef typename IC<typename KH<U>::type, typename UD<V>::type, typename DK<Y...>::type, typename UI<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HM {
    typedef typename IC<typename UD<U>::type, typename UI<V>::type, typename BV<Y...>::type, typename UI<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OM {
    typedef typename IC<typename TC<U>::type, typename RJ<V>::type, typename VW<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NI {
    typedef typename IC<typename RJ<U>::type, typename PZ<V>::type, typename SA<Y...>::type, typename RJ<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DS {
    typedef typename IC<typename PZ<U>::type, typename KH<V>::type, typename VO<Y...>::type, typename VG<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WV {
    typedef typename IC<typename UD<U>::type, typename RJ<V>::type, typename QT<Y...>::type, typename KH<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NZ {
    typedef typename IC<typename UD<U>::type, typename RJ<V>::type, typename BI<Y...>::type, typename UI<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct DJ {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, typename KX<Y...>::type, typename TO<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MZ {
    typedef typename IC<typename VG<U>::type, typename PZ<V>::type, typename CZ<Y...>::type, typename KH<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct AL {
    typedef typename IC<typename UI<U>::type, typename VG<V>::type, typename RD<Y...>::type, typename VG<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GW {
    typedef typename IC<typename UI<U>::type, typename VG<V>::type, typename YF<Y...>::type, typename VG<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OE {
    typedef typename IC<typename KH<U>::type, typename KH<V>::type, typename ON<Y...>::type, typename KH<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YL {
    typedef typename IC<typename UD<U>::type, typename VG<V>::type, typename VS<Y...>::type, typename VG<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct SR {
    typedef typename IC<typename UI<U>::type, typename RJ<V>::type, typename KV<Y...>::type, typename TO<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WS {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename ZC<Y...>::type, typename UI<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XU {
    typedef typename IC<typename VG<U>::type, typename KH<V>::type, typename PD<Y...>::type, typename KH<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct OF {
    typedef typename IC<typename TO<U>::type, typename VG<V>::type, typename AS<Y...>::type, typename PZ<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YU {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename IT<Y...>::type, typename KH<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NO {
    typedef typename IC<typename UD<U>::type, typename VG<V>::type, typename LB<Y...>::type, typename PZ<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GF {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, typename LC<Y...>::type, typename UI<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XX {
    typedef typename IC<typename RJ<U>::type, typename RJ<V>::type, typename GC<Y...>::type, typename RJ<W>::type, typename VG<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GB {
    typedef typename IC<typename VG<U>::type, typename UI<V>::type, typename DV<Y...>::type, typename TC<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct ZV {
    typedef typename IC<typename VG<U>::type, typename UD<V>::type, typename QA<Y...>::type, typename TO<W>::type, typename UI<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BB {
    typedef typename IC<typename PZ<U>::type, typename TC<V>::type, typename EC<Y...>::type, typename VG<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct CS {
    typedef typename IC<typename TC<U>::type, typename RJ<V>::type, typename WY<Y...>::type, typename TO<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct MW {
    typedef typename IC<typename UI<U>::type, typename RJ<V>::type, typename HO<Y...>::type, typename UI<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct NS {
    typedef typename IC<typename KH<U>::type, typename PZ<V>::type, typename FR<Y...>::type, typename RJ<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EO {
    typedef typename IC<typename TC<U>::type, typename UI<V>::type, typename KZ<Y...>::type, typename UD<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct JO {
    typedef typename IC<typename TO<U>::type, typename UD<V>::type, typename HL<Y...>::type, typename TC<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct QW {
    typedef typename IC<typename TO<U>::type, typename KH<V>::type, typename ZW<Y...>::type, typename TO<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XH {
    typedef typename IC<typename TO<U>::type, typename RJ<V>::type, typename CV<Y...>::type, typename RJ<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct HG {
    typedef typename IC<typename KH<U>::type, typename UI<V>::type, typename KT<Y...>::type, typename TC<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct WC {
    typedef typename IC<typename PZ<U>::type, typename KH<V>::type, typename AA<Y...>::type, typename RJ<W>::type, typename RJ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EU {
    typedef typename IC<typename TC<U>::type, typename RJ<V>::type, typename HM<Y...>::type, typename KH<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct FV {
    typedef typename IC<typename TC<U>::type, typename PZ<V>::type, typename OM<Y...>::type, typename VG<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct PP {
    typedef typename IC<typename TO<U>::type, typename UD<V>::type, typename NI<Y...>::type, typename TO<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct BO {
    typedef typename IC<typename UI<U>::type, typename TO<V>::type, typename DS<Y...>::type, typename RJ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TW {
    typedef typename IC<typename RJ<U>::type, typename TC<V>::type, typename WV<Y...>::type, typename PZ<W>::type, typename TC<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct GQ {
    typedef typename IC<typename UD<U>::type, typename UI<V>::type, typename NZ<Y...>::type, typename PZ<W>::type, typename PZ<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct UM {
    typedef typename IC<typename RJ<U>::type, typename UD<V>::type, typename DJ<Y...>::type, typename UD<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct TJ {
    typedef typename IC<typename UI<U>::type, typename UI<V>::type, typename MZ<Y...>::type, typename UD<W>::type, typename KH<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct EE {
    typedef typename IC<typename TC<U>::type, typename VG<V>::type, typename AL<Y...>::type, typename PZ<W>::type, typename TO<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct YP {
    typedef typename IC<typename PZ<U>::type, typename UD<V>::type, typename GW<Y...>::type, typename TC<W>::type, typename UD<X>::type>::type type;
};


template<typename U, typename V, typename W, typename X, typename... Y>
struct XG {
    typedef typename IC<typename TC<U>::type, typename TC<V>::type, typename OE<Y...>::type, typename KH<W>::type, typename UI<X>::type>::type type;
};


template<typename... T>
struct KD {
    typedef typename YL<T...>::type type;
};


template<typename... T>
struct JG {
    typedef typename SR<T...>::type type;
};


template<typename... T>
struct AQ {
    typedef typename WS<T...>::type type;
};


template<typename... T>
struct PT {
    typedef typename XU<T...>::type type;
};


template<typename... T>
struct VI {
    typedef typename OF<T...>::type type;
};


template<typename... T>
struct UB {
    typedef typename YU<T...>::type type;
};


template<typename... T>
struct XN {
    typedef typename NO<T...>::type type;
};


template<typename... T>
struct CQ {
    typedef typename GF<T...>::type type;
};


template<typename... T>
struct AC {
    typedef typename XX<T...>::type type;
};


template<typename... T>
struct ZJ {
    typedef typename GB<T...>::type type;
};


template<typename... T>
struct FF {
    typedef typename ZV<T...>::type type;
};


template<typename... T>
struct FE {
    typedef typename BB<T...>::type type;
};


template<typename... T>
struct GG {
    typedef typename CS<T...>::type type;
};


template<typename... T>
struct ZO {
    typedef typename MW<T...>::type type;
};


template<typename... T>
struct HQ {
    typedef typename NS<T...>::type type;
};


template<typename... T>
struct KB {
    typedef typename EO<T...>::type type;
};


template<typename... T>
struct KF {
    typedef typename JO<T...>::type type;
};


template<typename... T>
struct RG {
    typedef typename QW<T...>::type type;
};


template<typename... T>
struct ZZ {
    typedef typename XH<T...>::type type;
};


template<typename... T>
struct FQ {
    typedef typename HG<T...>::type type;
};


template<typename... T>
struct SX {
    typedef typename WC<T...>::type type;
};


template<typename... T>
struct SD {
    typedef typename EU<T...>::type type;
};


template<typename... T>
struct FA {
    typedef typename FV<T...>::type type;
};


template<typename... T>
struct MM {
    typedef typename PP<T...>::type type;
};


template<typename... T>
struct YR {
    typedef typename BO<T...>::type type;
};


template<typename... T>
struct GM {
    typedef typename TW<T...>::type type;
};


template<typename... T>
struct AZ {
    typedef typename GQ<T...>::type type;
};


template<typename... T>
struct NW {
    typedef typename UM<T...>::type type;
};


template<typename... T>
struct BN {
    typedef typename TJ<T...>::type type;
};


template<typename... T>
struct CJ {
    typedef typename EE<T...>::type type;
};


template<typename... T>
struct CX {
    typedef typename YP<T...>::type type;
};


template<typename... T>
struct SS {
    typedef typename XG<T...>::type type;
};


template<typename...U>
struct II :HI<QC, IM<typename KD<U...>::type, VG<SH::type>::type>> {
};


template<typename...U>
struct ZU :HI<II<U...>, IM<typename JG<U...>::type, KH<SH::type>::type>> {
};


template<typename...U>
struct EG :HI<ZU<U...>, IM<typename AQ<U...>::type, UI<SH::type>::type>> {
};


template<typename...U>
struct ZA :HI<EG<U...>, IM<typename PT<U...>::type, UD<SH::type>::type>> {
};


template<typename...U>
struct OJ :HI<ZA<U...>, IM<typename VI<U...>::type, UD<SH::type>::type>> {
};


template<typename...U>
struct LL :HI<OJ<U...>, IM<typename UB<U...>::type, TO<SH::type>::type>> {
};


template<typename...U>
struct SN :HI<LL<U...>, IM<typename XN<U...>::type, PZ<SH::type>::type>> {
};


template<typename...U>
struct MI :HI<SN<U...>, IM<typename CQ<U...>::type, TO<SH::type>::type>> {
};


template<typename...U>
struct ZL :HI<MI<U...>, IM<typename AC<U...>::type, KH<SH::type>::type>> {
};


template<typename...U>
struct QG :HI<ZL<U...>, IM<typename ZJ<U...>::type, RJ<SH::type>::type>> {
};


template<typename...U>
struct KS :HI<QG<U...>, IM<typename FF<U...>::type, RJ<SH::type>::type>> {
};


template<typename...U>
struct UF :HI<KS<U...>, IM<typename FE<U...>::type, TC<SH::type>::type>> {
};


template<typename...U>
struct TD :HI<UF<U...>, IM<typename GG<U...>::type, UD<SH::type>::type>> {
};


template<typename...U>
struct RN :HI<TD<U...>, IM<typename ZO<U...>::type, VG<SH::type>::type>> {
};


template<typename...U>
struct GH :HI<RN<U...>, IM<typename HQ<U...>::type, PZ<SH::type>::type>> {
};


template<typename...U>
struct SZ :HI<GH<U...>, IM<typename KB<U...>::type, VG<SH::type>::type>> {
};


template<typename...U>
struct HH :HI<SZ<U...>, IM<typename KF<U...>::type, RJ<SH::type>::type>> {
};


template<typename...U>
struct EI :HI<HH<U...>, IM<typename RG<U...>::type, TC<SH::type>::type>> {
};


template<typename...U>
struct PX :HI<EI<U...>, IM<typename ZZ<U...>::type, TC<SH::type>::type>> {
};


template<typename...U>
struct ZY :HI<PX<U...>, IM<typename FQ<U...>::type, TC<SH::type>::type>> {
};


template<typename...U>
struct LV :HI<ZY<U...>, IM<typename SX<U...>::type, TC<SH::type>::type>> {
};


template<typename...U>
struct HU :HI<LV<U...>, IM<typename SD<U...>::type, PZ<SH::type>::type>> {
};


template<typename...U>
struct CP :HI<HU<U...>, IM<typename FA<U...>::type, UI<SH::type>::type>> {
};


template<typename...U>
struct DA :HI<CP<U...>, IM<typename MM<U...>::type, TC<SH::type>::type>> {
};


template<typename...U>
struct IS :HI<DA<U...>, IM<typename YR<U...>::type, VG<SH::type>::type>> {
};


template<typename...U>
struct NT :HI<IS<U...>, IM<typename GM<U...>::type, UI<SH::type>::type>> {
};


template<typename...U>
struct BF :HI<NT<U...>, IM<typename AZ<U...>::type, RJ<SH::type>::type>> {
};


template<typename...U>
struct UE :HI<BF<U...>, IM<typename NW<U...>::type, UI<SH::type>::type>> {
};


template<typename...U>
struct NE :HI<UE<U...>, IM<typename BN<U...>::type, TO<SH::type>::type>> {
};


template<typename...U>
struct TE :HI<NE<U...>, IM<typename CJ<U...>::type, TO<SH::type>::type>> {
};


template<typename...U>
struct BD :HI<TE<U...>, IM<typename CX<U...>::type, TO<SH::type>::type>> {
};


template<typename...U>
struct RT :HI<BD<U...>, IM<typename SS<U...>::type, VG<SH::type>::type>> {
};

template<typename T, typename = void>
struct HA :CM<3> {};

template<typename T>
struct HA<T, typename WH<HI<RO<VT<T>>, RO<KE<T>>, CK<T>>::value>::type> :CM<5> {};

template<typename T>
struct HA<T, typename WH<HI<RO<VT<T>>, KE<T>, RO<CK<T>>>::value>::type> :CM<7> {};

template<typename T>
struct HA<T, typename WH<HI<RO<VT<T>>, KE<T>, CK<T>>::value>::type> :CM<11> {};

template<typename T>
struct HA<T, typename WH<HI<VT<T>, RO<KE<T>>, RO<CK<T>>>::value>::type> :CM<13> {};

template<typename T>
struct HA<T, typename WH<HI<VT<T>, RO<KE<T>>, CK<T>>::value>::type> :CM<17> {};

template<typename T>
struct HA<T, typename WH<HI<VT<T>, KE<T>, RO<CK<T>>>::value>::type> :CM<19> {};

template<typename T>
struct HA<T, typename WH<HI<VT<T>, KE<T>, CK<T>>::value>::type> :CM<21> {};

template<typename...U>
struct Nagi {
    static char buf[108];
    static const char* GetFlag() {
        if (RT<U...>::value == false) {
            return "I don't know the flag, ask some else!";
        }
        int key[] = { HA<U>::value... };
        int S[256];
        int i, j = 0, t;
        for (i = 0; i < 256; i++) { S[i] = i; }
        for (i = 0; i < 256; i++) {
            j = (j + S[i] + key[i % sizeof...(U)]) & 0xff;
            t = S[i], S[i] = S[j], S[j] = t;
        }
        i = j = 0;
        for (int k = 0; k < 107; k++) {
            i = (i + 1) & 0xff;
            j = (j + S[i]) & 0xff;
            t = S[i], S[i] = S[j], S[j] = t;
            buf[k] ^= S[(S[i] + S[j]) & 0xff];
        }
        return buf;
    }
};

template<typename...U>
char Nagi<U...>::buf[108] = "\xb0\x0d\x1f\x0e\x2a\x27\x08\xd4\x1b\x8a\xf9\xde\x67\x86\x95\x80\x4f\x92\xca\xa1\x70\x2c\x53\xae\xd7\x4e\xf2\x86\x4f\x37\x03\xdc\xbe\xf2\xc4\x0e\x7c\x8f\x8a\x00\x09\x93\xf0\xd0\xf3\x37\xd4\x7e\x6f\x83\x6d\x3e\x16\x99\x63\x25\x7a\x3c\x30\x51\xaf\xf6\x3e\xc5\x0f\xc8\x93\xeb\x4f\x6b\xbd\xc2\xa1\x96\x2b\x4e\xc4\xca\x91\xcd\x70\xc2\x24\xe8\xa2\x92\xbe\x1e\xea\x48\xf9\x16\xb0\x78\x00\x6b\x7c\x95\xb1\xa0\xcb\xf7\x06\xaf\x4d\xe8\x96";
