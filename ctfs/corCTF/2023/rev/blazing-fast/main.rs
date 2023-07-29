#![recursion_limit = "1024"]

use std::marker::PhantomData;

trait Burucha {
    type XV;
}
impl<ZZ, BO> Burucha for (ZZ, BO) {
    type XV = ZZ;
}
trait Theodotian {
    type XV;
}
impl<ZZ, BO> Theodotian for (ZZ, BO) {
    type XV = BO;
}
trait Waterfowler {}
struct Differing<CY, ZZ>(PhantomData<CY>, PhantomData<ZZ>);
struct Unkembed;
impl<CY, ZZ> Waterfowler for Differing<CY, ZZ> {}
impl Waterfowler for Unkembed {}
trait Prefixal {
    type XV: Waterfowler;
}
impl<JX: Waterfowler> Prefixal for (Unkembed, JX) {
    type XV = JX;
}
impl<CY, GA: Waterfowler, JX: Waterfowler> Prefixal for (Differing<CY, GA>, JX)
where
    (GA, Differing<CY, JX>): Prefixal,
{
    type XV = <(GA, Differing<CY, JX>) as Prefixal>::XV;
}
trait Pickoff {
    type XV: Waterfowler;
}
impl<CY, GA: Waterfowler> Pickoff for (Differing<CY, GA>, Unkembed) {
    type XV = Differing<CY, GA>;
}
impl<GA: Waterfowler> Pickoff for (Unkembed, GA) {
    type XV = Unsolidified;
}
impl<CY, OP, GA: Waterfowler, JX: Waterfowler> Pickoff
    for (Differing<CY, GA>, Differing<OP, JX>)
where
    (GA, JX): Pickoff,
{
    type XV = <(GA, JX) as Pickoff>::XV;
}
trait Nonnuclear {
    type XV: Waterfowler;
}
impl Nonnuclear for (Unkembed, Unkembed) {
    type XV = Embrica;
}
impl<CY, ZZ: Waterfowler> Nonnuclear for (Differing<CY, ZZ>, Unkembed) {
    type XV = Unsolidified;
}
impl<CY, ZZ: Waterfowler> Nonnuclear for (Unkembed, Differing<CY, ZZ>) {
    type XV = Unsolidified;
}
impl<CY, GA: Waterfowler, JX: Waterfowler> Nonnuclear
    for (Differing<CY, GA>, Differing<CY, JX>)
where
    (GA, JX): Nonnuclear,
{
    type XV = <(GA, JX) as Nonnuclear>::XV;
}
trait Psywar<ZZ> {
    type XV: Waterfowler;
}
impl<ZZ> Psywar<ZZ> for Unkembed {
    type XV = Unkembed;
}
impl<ZZ, CY, GA> Psywar<ZZ> for Differing<CY, GA>
where
    GA: Psywar<ZZ>,
{
    type XV = Differing<ZZ, <GA as Psywar<ZZ>>::XV>;
}
type Unsolidified = Unkembed;
type Embrica = Differing<(), Unkembed>;
trait Phlogopite {
    type XV: Waterfowler;
}
impl<YK: Waterfowler> Phlogopite for (YK, Unkembed) {
    type XV = YK;
}
impl<YK: Waterfowler, CY, ZZ> Phlogopite for (YK, Differing<CY, ZZ>)
where
    (YK, CY): Prefixal,
    (<(YK, CY) as Prefixal>::XV, ZZ): Phlogopite,
    <(<(YK, CY) as Prefixal>::XV, ZZ) as Phlogopite>::XV: Waterfowler,
{
    type XV = <(<(YK, CY) as Prefixal>::XV, ZZ) as Phlogopite>::XV;
}
trait Rheumatics {
    type XV: Waterfowler;
}
impl<ZZ: Waterfowler, BO: Waterfowler> Rheumatics for (ZZ, BO)
where
    ZZ: Psywar<BO>,
    (Unsolidified, <ZZ as Psywar<BO>>::XV): Phlogopite,
{
    type XV = <(Unsolidified, <ZZ as Psywar<BO>>::XV) as Phlogopite>::XV;
}
struct Cardiae<
    VC: Waterfowler,
    GA: Waterfowler,
    CY: Waterfowler,
    JX: Waterfowler,
>(PhantomData<VC>, PhantomData<GA>, PhantomData<CY>, PhantomData<JX>);
struct Unfitty;
struct Altern;
struct Oleines<QD>(PhantomData<QD>);
struct Jaywalked;
struct Chacte;
struct Hoggie;
struct Disciplinarity;
struct Braver;
struct Debused;
struct Scarpa;
struct Antipoles<QD: Waterfowler, UJ: Waterfowler>(
    PhantomData<QD>,
    PhantomData<UJ>,
);
struct Bini<QD: Waterfowler>(PhantomData<QD>);
struct Inapplication;
struct Wistaria;
struct Scabish;
struct Slushpit;
struct Thundercloud;
trait Drain<RQ> {
    type XV;
}
impl<
        ZZ: Waterfowler,
        VC: Waterfowler,
        GA: Waterfowler,
        OP: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<VC, Differing<OP, GA>, CY, JX>> for Differing<Unfitty, ZZ>
where
    ZZ: Drain<Cardiae<VC, GA, OP, Differing<CY, JX>>>,
{
    type XV = <ZZ as Drain<Cardiae<VC, GA, OP, Differing<CY, JX>>>>::XV;
}
impl<ZZ: Waterfowler, VC: Waterfowler, CY: Waterfowler, JX: Waterfowler>
    Drain<Cardiae<VC, Unkembed, CY, JX>> for Differing<Unfitty, ZZ>
where
    ZZ: Drain<Cardiae<VC, Unkembed, Unkembed, Differing<CY, JX>>>,
{
    type XV =
        <ZZ as Drain<Cardiae<VC, Unkembed, Unkembed, Differing<CY, JX>>>>::XV;
}
impl<
        ZZ: Waterfowler,
        VC: Waterfowler,
        GA: Waterfowler,
        OP: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<VC, GA, CY, Differing<OP, JX>>> for Differing<Altern, ZZ>
where
    ZZ: Drain<Cardiae<VC, Differing<CY, GA>, OP, JX>>,
{
    type XV = <ZZ as Drain<Cardiae<VC, Differing<CY, GA>, OP, JX>>>::XV;
}
impl<ZZ: Waterfowler, VC: Waterfowler, GA: Waterfowler, CY: Waterfowler>
    Drain<Cardiae<VC, GA, CY, Unkembed>> for Differing<Altern, ZZ>
where
    ZZ: Drain<Cardiae<VC, Differing<CY, GA>, Unkembed, Unkembed>>,
{
    type XV =
        <ZZ as Drain<Cardiae<VC, Differing<CY, GA>, Unkembed, Unkembed>>>::XV;
}
impl<
        ZZ: Waterfowler,
        VC: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
        QD,
    > Drain<Cardiae<VC, GA, CY, JX>> for Differing<Oleines<QD>, ZZ>
where
    ZZ: Drain<Cardiae<Differing<QD, VC>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<Cardiae<Differing<QD, VC>, GA, CY, JX>>>::XV;
}
impl<
        VC,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<VC, BO>, GA, CY, JX>> for Differing<Jaywalked, ZZ>
where
    ZZ: Drain<Cardiae<BO, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<Cardiae<BO, GA, CY, JX>>>::XV;
}
impl<
        VC,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<VC, BO>, GA, CY, JX>> for Differing<Chacte, ZZ>
where
    ZZ: Drain<Cardiae<Differing<VC, BO>, GA, Differing<VC, CY>, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<VC, BO>, GA, Differing<VC, CY>, JX>,
    >>::XV;
}
impl<
        VC: Waterfowler,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY,
        JX: Waterfowler,
    > Drain<Cardiae<VC, GA, Differing<CY, BO>, JX>> for Differing<Hoggie, ZZ>
where
    ZZ: Drain<Cardiae<Differing<CY, VC>, GA, Differing<CY, BO>, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<CY, VC>, GA, Differing<CY, BO>, JX>,
    >>::XV;
}
impl<
        VC,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<VC, BO>, GA, CY, JX>>
    for Differing<Disciplinarity, ZZ>
where
    ZZ: Drain<Cardiae<BO, GA, Differing<VC, CY>, JX>>,
{
    type XV = <ZZ as Drain<Cardiae<BO, GA, Differing<VC, CY>, JX>>>::XV;
}
impl<
        VC: Waterfowler,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY,
        JX: Waterfowler,
    > Drain<Cardiae<VC, GA, Differing<CY, BO>, JX>> for Differing<Braver, ZZ>
where
    ZZ: Drain<Cardiae<Differing<CY, VC>, GA, BO, JX>>,
{
    type XV = <ZZ as Drain<Cardiae<Differing<CY, VC>, GA, BO, JX>>>::XV;
}
impl<
        ZZ: Waterfowler,
        BO: Waterfowler,
        VC: Waterfowler,
        RQ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<BO, Differing<VC, RQ>>, GA, CY, JX>>
    for Differing<Debused, ZZ>
where
    (VC, BO): Nonnuclear,
    ZZ: Drain<Cardiae<Differing<<(VC, BO) as Nonnuclear>::XV, RQ>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<<(VC, BO) as Nonnuclear>::XV, RQ>, GA, CY, JX>,
    >>::XV;
}
impl<ZZ: Waterfowler, GA: Waterfowler, CY: Waterfowler, JX: Waterfowler>
    Drain<Cardiae<Unkembed, GA, CY, JX>> for Differing<Scarpa, ZZ>
where
    ZZ: Drain<Cardiae<Differing<Unsolidified, Unkembed>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<Unsolidified, Unkembed>, GA, CY, JX>,
    >>::XV;
}
impl<
        OP,
        VC: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<OP, VC>, GA, CY, JX>> for Differing<Scarpa, ZZ>
where
    ZZ: Drain<Cardiae<Differing<Embrica, Differing<OP, VC>>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<Embrica, Differing<OP, VC>>, GA, CY, JX>,
    >>::XV;
}
impl<
        QD: Waterfowler,
        UJ: Waterfowler,
        VC: Waterfowler,
        OP,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<Differing<OP, VC>, BO>, GA, CY, JX>>
    for Differing<Antipoles<QD, UJ>, ZZ>
where
    QD: Drain<Cardiae<BO, GA, CY, JX>>,
    ZZ: Drain<<QD as Drain<Cardiae<BO, GA, CY, JX>>>::XV>,
{
    type XV = <ZZ as Drain<<QD as Drain<Cardiae<BO, GA, CY, JX>>>::XV>>::XV;
}
impl<
        QD: Waterfowler,
        UJ: Waterfowler,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<Unkembed, BO>, GA, CY, JX>>
    for Differing<Antipoles<QD, UJ>, ZZ>
where
    UJ: Drain<Cardiae<BO, GA, CY, JX>>,
    ZZ: Drain<<UJ as Drain<Cardiae<BO, GA, CY, JX>>>::XV>,
{
    type XV = <ZZ as Drain<<UJ as Drain<Cardiae<BO, GA, CY, JX>>>::XV>>::XV;
}
impl<
        QD: Waterfowler,
        VC: Waterfowler,
        OP,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<Differing<OP, VC>, BO>, GA, CY, JX>>
    for Differing<Bini<QD>, ZZ>
where
    QD: Drain<Cardiae<BO, GA, CY, JX>>,
    Differing<Bini<QD>, ZZ>: Drain<<QD as Drain<Cardiae<BO, GA, CY, JX>>>::XV>,
{
    type XV = <Differing<Bini<QD>, ZZ> as Drain<
        <QD as Drain<Cardiae<BO, GA, CY, JX>>>::XV,
    >>::XV;
}
impl<
        QD: Waterfowler,
        BO: Waterfowler,
        ZZ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<Unkembed, BO>, GA, CY, JX>>
    for Differing<Bini<QD>, ZZ>
where
    ZZ: Drain<Cardiae<BO, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<Cardiae<BO, GA, CY, JX>>>::XV;
}
impl<
        ZZ: Waterfowler,
        BO: Waterfowler,
        VC: Waterfowler,
        RQ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<BO, Differing<VC, RQ>>, GA, CY, JX>>
    for Differing<Inapplication, ZZ>
where
    (BO, VC): Prefixal,
    ZZ: Drain<Cardiae<Differing<<(BO, VC) as Prefixal>::XV, RQ>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<<(BO, VC) as Prefixal>::XV, RQ>, GA, CY, JX>,
    >>::XV;
}
impl<
        ZZ: Waterfowler,
        BO: Waterfowler,
        VC: Waterfowler,
        RQ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<BO, Differing<VC, RQ>>, GA, CY, JX>>
    for Differing<Wistaria, ZZ>
where
    (VC, BO): Pickoff,
    ZZ: Drain<Cardiae<Differing<<(VC, BO) as Pickoff>::XV, RQ>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<<(VC, BO) as Pickoff>::XV, RQ>, GA, CY, JX>,
    >>::XV;
}
impl<
        ZZ: Waterfowler,
        BO: Waterfowler,
        VC: Waterfowler,
        RQ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<BO, Differing<VC, RQ>>, GA, CY, JX>>
    for Differing<Scabish, ZZ>
where
    (BO, VC): Rheumatics,
    ZZ: Drain<Cardiae<Differing<<(BO, VC) as Rheumatics>::XV, RQ>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<<(BO, VC) as Rheumatics>::XV, RQ>, GA, CY, JX>,
    >>::XV;
}
impl<
        ZZ: Waterfowler,
        OP,
        RQ: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<OP, RQ>, GA, CY, JX>> for Differing<Slushpit, ZZ>
where
    ZZ: Drain<Cardiae<Differing<OP, Differing<OP, RQ>>, GA, CY, JX>>,
{
    type XV = <ZZ as Drain<
        Cardiae<Differing<OP, Differing<OP, RQ>>, GA, CY, JX>,
    >>::XV;
}
impl<
        VC,
        ZZ: Waterfowler,
        BO: Waterfowler,
        GA: Waterfowler,
        CY: Waterfowler,
        JX: Waterfowler,
    > Drain<Cardiae<Differing<VC, BO>, GA, CY, JX>>
    for Differing<Thundercloud, ZZ>
{
    type XV = VC;
}
impl<ZZ: Waterfowler, GA: Waterfowler, CY: Waterfowler, JX: Waterfowler>
    Drain<Cardiae<Unkembed, GA, CY, JX>> for Differing<Thundercloud, ZZ>
{
    type XV = Unkembed;
}
impl<RQ> Drain<RQ> for Unkembed {
    type XV = RQ;
}
trait Mythology<const ZZ: usize> {
    type XV;
}
impl Mythology<0> for () {
    type XV = Unkembed;
}
impl Mythology<1> for () {
    type XV = Embrica;
}
impl Mythology<2> for () {
    type XV =
        <(<() as Mythology<1>>::XV, <() as Mythology<1>>::XV) as Prefixal>::XV;
}
impl Mythology<3> for () {
    type XV =
        <(<() as Mythology<1>>::XV, <() as Mythology<2>>::XV) as Prefixal>::XV;
}
impl Mythology<4> for () {
    type XV =
        <(<() as Mythology<2>>::XV, <() as Mythology<2>>::XV) as Prefixal>::XV;
}
impl Mythology<5> for () {
    type XV =
        <(<() as Mythology<2>>::XV, <() as Mythology<3>>::XV) as Prefixal>::XV;
}
impl Mythology<6> for () {
    type XV =
        <(<() as Mythology<3>>::XV, <() as Mythology<3>>::XV) as Prefixal>::XV;
}
impl Mythology<7> for () {
    type XV =
        <(<() as Mythology<3>>::XV, <() as Mythology<4>>::XV) as Prefixal>::XV;
}
impl Mythology<8> for () {
    type XV =
        <(<() as Mythology<4>>::XV, <() as Mythology<4>>::XV) as Prefixal>::XV;
}
impl Mythology<9> for () {
    type XV =
        <(<() as Mythology<4>>::XV, <() as Mythology<5>>::XV) as Prefixal>::XV;
}
trait Clementine<const ZZ: char> {
    type XV;
}
impl Clementine<'a'> for () {
    type XV = (<() as Mythology<0>>::XV, <() as Mythology<0>>::XV);
}
impl Clementine<'b'> for () {
    type XV = (<() as Mythology<1>>::XV, <() as Mythology<0>>::XV);
}
impl Clementine<'c'> for () {
    type XV = (<() as Mythology<2>>::XV, <() as Mythology<0>>::XV);
}
impl Clementine<'d'> for () {
    type XV = (<() as Mythology<3>>::XV, <() as Mythology<0>>::XV);
}
impl Clementine<'e'> for () {
    type XV = (<() as Mythology<4>>::XV, <() as Mythology<0>>::XV);
}
impl Clementine<'f'> for () {
    type XV = (<() as Mythology<5>>::XV, <() as Mythology<0>>::XV);
}
impl Clementine<'g'> for () {
    type XV = (<() as Mythology<0>>::XV, <() as Mythology<1>>::XV);
}
impl Clementine<'h'> for () {
    type XV = (<() as Mythology<1>>::XV, <() as Mythology<1>>::XV);
}
impl Clementine<'i'> for () {
    type XV = (<() as Mythology<2>>::XV, <() as Mythology<1>>::XV);
}
impl Clementine<'j'> for () {
    type XV = (<() as Mythology<3>>::XV, <() as Mythology<1>>::XV);
}
impl Clementine<'k'> for () {
    type XV = (<() as Mythology<4>>::XV, <() as Mythology<1>>::XV);
}
impl Clementine<'l'> for () {
    type XV = (<() as Mythology<5>>::XV, <() as Mythology<1>>::XV);
}
impl Clementine<'m'> for () {
    type XV = (<() as Mythology<0>>::XV, <() as Mythology<2>>::XV);
}
impl Clementine<'n'> for () {
    type XV = (<() as Mythology<1>>::XV, <() as Mythology<2>>::XV);
}
impl Clementine<'o'> for () {
    type XV = (<() as Mythology<2>>::XV, <() as Mythology<2>>::XV);
}
impl Clementine<'p'> for () {
    type XV = (<() as Mythology<3>>::XV, <() as Mythology<2>>::XV);
}
impl Clementine<'q'> for () {
    type XV = (<() as Mythology<4>>::XV, <() as Mythology<2>>::XV);
}
impl Clementine<'r'> for () {
    type XV = (<() as Mythology<5>>::XV, <() as Mythology<2>>::XV);
}
impl Clementine<'s'> for () {
    type XV = (<() as Mythology<0>>::XV, <() as Mythology<3>>::XV);
}
impl Clementine<'t'> for () {
    type XV = (<() as Mythology<1>>::XV, <() as Mythology<3>>::XV);
}
impl Clementine<'u'> for () {
    type XV = (<() as Mythology<2>>::XV, <() as Mythology<3>>::XV);
}
impl Clementine<'v'> for () {
    type XV = (<() as Mythology<3>>::XV, <() as Mythology<3>>::XV);
}
impl Clementine<'w'> for () {
    type XV = (<() as Mythology<4>>::XV, <() as Mythology<3>>::XV);
}
impl Clementine<'x'> for () {
    type XV = (<() as Mythology<5>>::XV, <() as Mythology<3>>::XV);
}
impl Clementine<'y'> for () {
    type XV = (<() as Mythology<0>>::XV, <() as Mythology<4>>::XV);
}
impl Clementine<'z'> for () {
    type XV = (<() as Mythology<1>>::XV, <() as Mythology<4>>::XV);
}
impl Clementine<'!'> for () {
    type XV = (<() as Mythology<2>>::XV, <() as Mythology<4>>::XV);
}
impl Clementine<'"'> for () {
    type XV = (<() as Mythology<3>>::XV, <() as Mythology<4>>::XV);
}
impl Clementine<'\''> for () {
    type XV = (<() as Mythology<4>>::XV, <() as Mythology<4>>::XV);
}
impl Clementine<'/'> for () {
    type XV = (<() as Mythology<5>>::XV, <() as Mythology<4>>::XV);
}
impl Clementine<','> for () {
    type XV = (<() as Mythology<0>>::XV, <() as Mythology<5>>::XV);
}
impl Clementine<'-'> for () {
    type XV = (<() as Mythology<1>>::XV, <() as Mythology<5>>::XV);
}
impl Clementine<'.'> for () {
    type XV = (<() as Mythology<2>>::XV, <() as Mythology<5>>::XV);
}
impl Clementine<'_'> for () {
    type XV = (<() as Mythology<3>>::XV, <() as Mythology<5>>::XV);
}
impl Clementine<'{'> for () {
    type XV = (<() as Mythology<4>>::XV, <() as Mythology<5>>::XV);
}
impl Clementine<'}'> for () {
    type XV = (<() as Mythology<5>>::XV, <() as Mythology<5>>::XV);
}
trait Smolts {
    fn output() -> &'static str;
}
impl Smolts for <() as Mythology<0>>::XV {
    fn output() -> &'static str {
        "incorrect :("
    }
}
impl Smolts for <() as Mythology<1>>::XV {
    fn output() -> &'static str {
        "correct!"
    }
}

macro_rules! encode {
    () => { Unkembed };
    ($c:literal $($r:literal )*) => {
        Differing<
            <<() as Clementine<$c>>::XV as Burucha>::XV,
            Differing<
                <<() as Clementine<$c>>::XV as Theodotian>::XV,
                encode!($($r)*),
            >,
        >
    }
}

type Program = Differing<Altern, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Disciplinarity, Differing<Unfitty, Differing<Unfitty, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Disciplinarity, Differing<Altern, Differing<Scarpa, Differing<Bini<Differing<Slushpit, Differing<Oleines<<() as Mythology<5>>::XV>, Differing<Wistaria, Differing<Antipoles<Differing<Unfitty, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Inapplication, Differing<Disciplinarity, Differing<Altern, Unkembed>>>>>>, Unkembed>, Differing< Disciplinarity, Differing<Altern, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Inapplication, Differing<Disciplinarity, Differing<Unfitty, Differing<Scarpa, Unkembed>>>>>>>>>>>>>, Differing<Altern, Differing<Braver, Differing<Unfitty, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Differing<Unfitty, Differing<Braver, Differing<Altern, Differing<Inapplication, Differing<Antipoles<Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Thundercloud, Unkembed>>, Differing<Altern, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Disciplinarity, Differing<Unfitty, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Inapplication, Differing<Altern, Differing<Hoggie, Differing<Unfitty, Differing<Wistaria, Differing<Bini<Differing<Altern, Differing<Hoggie, Differing<Unfitty, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Inapplication, Differing<Unfitty, Differing<Chacte, Differing<Altern, Differing<Bini<Differing<Braver, Differing<Unfitty, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Chacte, Differing<Altern, Unkembed>>>>>>>>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Altern, Differing<Hoggie, Differing<Unfitty, Differing<Wistaria, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Altern, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Inapplication, Differing<Chacte, Differing<Unfitty, Differing<Unfitty, Differing<Braver, Differing<Jaywalked, Differing<Altern, Differing<Wistaria, Unkembed>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>, Differing<Altern, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Chacte, Differing<Unfitty, Differing<Bini<Differing<Altern, Differing<Hoggie, Differing<Unfitty, Differing<Unfitty, Differing<Chacte, Differing<Altern, Differing<Bini<Differing<Braver, Differing<Unfitty, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Chacte, Differing<Altern, Unkembed>>>>>>>>, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Altern, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Chacte, Differing<Unfitty, Differing<Unfitty, Differing<Braver, Differing<Jaywalked, Differing<Altern, Unkembed>>>>>>>>>>>>>>>>>>>>, Differing<Altern, Differing<Braver, Differing<Jaywalked, Differing<Unfitty, Differing<Slushpit, Differing<Disciplinarity, Differing<Altern, Differing<Altern, Differing< Scarpa, Differing<Bini<Differing<Slushpit, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Differing<Bini<Differing<Disciplinarity, Differing<Altern, Differing<Altern, Differing<Slushpit, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Unkembed>>>>>>>>>, Differing<Unfitty, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Differing<Bini<Differing<Unfitty, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Unkembed>>>>>>>>, Differing<Altern, Differing<Altern, Differing<Jaywalked, Differing<Slushpit, Differing<Bini<Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Altern, Differing<Altern, Differing<Slushpit, Unkembed>>>>>>, Differing<Jaywalked, Differing<Scarpa, Unkembed>>>>>>>>>>>>>>>>>>>>>>, Differing<Unfitty, Differing<Unfitty, Differing<Braver, Differing<Jaywalked, Differing<Altern, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<7>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<7>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<5>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<4>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<7>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<4>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<5>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<() as Mythology<7>>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<8>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<4>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<7>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<5>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<3>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<5>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<5>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<8>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<4>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<7>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<4>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<5>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<2>>::XV) as Rheumatics>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<4>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<2>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<8>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<6>>::XV) as Prefixal>::XV>, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<3>>::XV) as Rheumatics>::XV,<() as Mythology<9>>::XV) as Prefixal>::XV>, Differing<Scarpa, Differing<Bini<Differing<Disciplinarity, Differing<Scarpa, Unkembed>>>, Differing<Altern, Differing<Unfitty, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Chacte, Differing<Bini<Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Disciplinarity, Differing<Altern, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Slushpit, Differing<Bini<Differing<Braver, Differing<Altern, Differing<Disciplinarity, Differing<Altern, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Slushpit, Unkembed>>>>>>>>, Differing<Jaywalked, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Differing<Bini<Differing<Unfitty, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Unkembed>>>>>>>>, Differing<Altern, Differing<Oleines<<(<(<(<() as Mythology<9>>::XV,<() as Mythology<1>>::XV) as Prefixal>::XV,<() as Mythology<1>>::XV) as Rheumatics>::XV,<() as Mythology<0>>::XV) as Prefixal>::XV>, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Slushpit, Differing<Bini<Differing<Altern, Differing<Altern, Differing<Altern, Differing<Hoggie, Differing<Oleines<<() as Mythology<3>>::XV>, Differing<Scabish, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<4>>::XV>, Differing<Scabish, Differing<Inapplication, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Scabish, Differing<Inapplication, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<2>>::XV>, Differing<Scabish, Differing<Inapplication, Differing<Disciplinarity, Differing<Altern, Differing<Altern, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Slushpit, Unkembed>>>>>>>>>>>>>>>>>>>>>>>>>>>>, Differing<Jaywalked, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Differing<Bini<Differing<Unfitty, Differing<Braver, Differing<Unfitty, Differing<Hoggie, Differing<Oleines<<() as Mythology<6>>::XV>, Differing<Debused, Differing<Oleines<<() as Mythology<0>>::XV>, Differing<Debused, Unkembed>>>>>>>>>, Differing<Braver, Differing<Jaywalked, Differing<Braver, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Wistaria, Differing<Chacte, Unkembed>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>, Differing<Braver, Differing<Jaywalked, Differing< Unfitty, Differing<Oleines<<() as Mythology<1>>::XV>, Differing<Disciplinarity, Differing<Scarpa, Differing<Bini<Differing<Altern, Differing<Braver, Differing<Unfitty, Differing<Debused, Differing<Braver, Differing<Scabish, Differing<Disciplinarity, Differing<Scarpa, Unkembed>>>>>>>>>, Differing<Braver, Differing<Thundercloud, Unkembed>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>, Unkembed>>>>>>>>>>>>>>>>>>>>>>;

macro_rules! execute {
    ($p:ty, $i:ty) => {
        <$p as Drain<Cardiae<$i, Unkembed, Unkembed, Unkembed>>>::XV
    };
}

fn main() {
    type Input = encode!('c' 'o' 'r' 'c' 't' 'f' '{' 'f' 'l' 'a' 'g' '}');
    println!("{}", <execute!(Program, Input)>::output());
}
