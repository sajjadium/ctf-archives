#![recursion_limit = "10000"]
use std::marker::PhantomData;
struct DidGongGong<DiceDiceGice>(PhantomData<DiceDiceGice>);
struct DangGong;
trait DangGangGang<DidGang> {
    type DidGong;
}
impl<DiceDiceGice> DangGangGang<DangGong> for DiceDiceGice {
    type DidGong = DiceDiceGice;
}
impl<DiceDiceGice, DanceDanceGig> DangGangGang<DidGongGong<DanceDanceGig>> for DiceDiceGice
where
    DiceDiceGice: DangGangGang<DanceDanceGig>,
{
    type DidGong = DidGongGong<<DiceDiceGice as DangGangGang<DanceDanceGig>>::DidGong>;
}
trait DidGigGig<DidGang> {
    type DidGong;
}
impl<DiceDiceGice> DidGigGig<DangGong> for DiceDiceGice {
    type DidGong = DangGong;
}
impl<DiceDiceGice, DanceDanceGig> DidGigGig<DidGongGong<DanceDanceGig>> for DiceDiceGice
where
    DiceDiceGice: DidGigGig<DanceDanceGig>,
    DiceDiceGice: DangGangGang<<DiceDiceGice as DidGigGig<DanceDanceGig>>::DidGong>,
{
    type DidGong = <DiceDiceGice as DangGangGang<<DiceDiceGice as DidGigGig<DanceDanceGig>>::DidGong>>::DidGong;
}
trait DangGig<DidGang> {
    type DidGong;
}
impl<DiceDiceGice> DangGig<DangGong> for DiceDiceGice {
    type DidGong = DiceDiceGice;
}
impl<DiceDiceGice, DanceDanceGig> DangGig<DidGongGong<DanceDanceGig>> for DidGongGong<DiceDiceGice>
where
    DiceDiceGice: DangGig<DanceDanceGig>,
{
    type DidGong = <DiceDiceGice as DangGig<DanceDanceGig>>::DidGong;
}
trait DanceDanceGang<DidGang> {
    type DidGong;
}
impl DanceDanceGang<DangGong> for DangGong {
    type DidGong = DangGong;
}
impl<DiceDiceGice> DanceDanceGang<DangGong> for DidGongGong<DiceDiceGice> {
    type DidGong = DidGongGong<DangGong>;
}
impl<DiceDiceGice> DanceDanceGang<DidGongGong<DiceDiceGice>> for DangGong {
    type DidGong = DidGongGong<DangGong>;
}
impl<DiceDiceGice, DanceDanceGig> DanceDanceGang<DidGongGong<DanceDanceGig>> for DidGongGong<DiceDiceGice>
where
    DiceDiceGice: DanceDanceGang<DanceDanceGig>,
{
    type DidGong = <DiceDiceGice as DanceDanceGang<DanceDanceGig>>::DidGong;
}
struct DiceGice;
struct DiceGig<DanceGigGig, DiceDiceGice>(PhantomData<DanceGigGig>, PhantomData<DiceDiceGice>);
trait DanceGang {
    type DidGong;
}
struct DiceGang;
impl DanceGang for DiceGang {
    type DidGong = DiceGang;
}
struct DangGice;
impl DanceGang for DangGice {
    type DidGong = DangGice;
}
struct DiceGongGong;
impl DanceGang for DiceGongGong {
    type DidGong = DiceGongGong;
}
struct DanceGig;
impl DanceGang for DanceGig {
    type DidGong = DanceGig;
}
struct DidGig;
impl DanceGang for DidGig {
    type DidGong = DidGig;
}
struct DangDangGang;
impl DanceGang for DangDangGang {
    type DidGong = DangDangGang;
}
struct DidDidGice;
impl DanceGang for DidDidGice {
    type DidGong = DidDidGice;
}
struct DangGang;
impl DanceGang for DangGang {
    type DidGong = DangGang;
}
struct DiceDiceGang;
impl DanceGang for DiceDiceGang {
    type DidGong = DiceDiceGang;
}
struct DanceGice;
impl DanceGang for DanceGice {
    type DidGong = DanceGice;
}
struct DidGangGang;
impl DanceGang for DidGangGang {
    type DidGong = DidGangGang;
}
struct DidGice;
impl DanceGang for DidGice {
    type DidGong = DidGice;
}
struct DiceGong;
impl DanceGang for DiceGong {
    type DidGong = DiceGong;
}
struct DanceGiceGice;
impl DanceGang for DanceGiceGice {
    type DidGong = DanceGiceGice;
}
impl DanceGang for DangGong {
    type DidGong = DangGong;
}
impl<DiceDiceGice> DanceGang for DidGongGong<DiceDiceGice> {
    type DidGong = DidGongGong<DiceDiceGice>;
}
impl DanceGang for DiceGig<DidGig, DiceGice> {
    type DidGong = DiceGice;
}
impl<DanceGigGig, DiceDiceGice> DanceGang for DiceGig<DidGig, DiceGig<DanceGigGig, DiceDiceGice>>
where
    DanceGigGig: DanceGang,
{
    type DidGong = DiceGig<<DanceGigGig as DanceGang>::DidGong, DiceDiceGice>;
}
impl<DangDangGice, DanceGangGang> DanceGang for DiceGig<DiceGongGong, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGice>>>
where
    DangDangGice: DanceGang,
    DanceGangGang: DanceGang,
    <DangDangGice as DanceGang>::DidGong: DangGig<<DanceGangGang as DanceGang>::DidGong>,
{
    type DidGong = <<DangDangGice as DanceGang>::DidGong as DangGig<<DanceGangGang as DanceGang>::DidGong>>::DidGong;
}
impl<DiceDiceGice> DanceGang for DiceGig<DangDangGang, DiceGig<DiceDiceGice, DiceGice>>
where
    DiceDiceGice: DanceGang,
{
    type DidGong = <DiceDiceGice as DanceGang>::DidGong;
}
impl<DiceDiceGice, DanceDanceGig, DangGigGig> DanceGang for DiceGig<DangDangGang, DiceGig<DiceDiceGice, DiceGig<DanceDanceGig, DangGigGig>>>
where
    DiceGig<DangDangGang, DiceGig<DanceDanceGig, DangGigGig>>: DanceGang,
    DiceDiceGice: DanceGang,
{
    type DidGong = <DiceGig<DangDangGang, DiceGig<DanceDanceGig, DangGigGig>> as DanceGang>::DidGong;
}
impl<DiceDiceGice> DanceGang for DiceGig<DidDidGice, DiceGig<DiceDiceGice, DiceGice>> {
    type DidGong = DangGong;
}
impl<DiceDiceGice, DanceDanceGig, DangGigGig> DanceGang for DiceGig<DidDidGice, DiceGig<DiceDiceGice, DiceGig<DanceDanceGig, DangGigGig>>>
where
    DiceDiceGice: DanceGang,
    DanceDanceGig: DanceGang,
    <DiceDiceGice as DanceGang>::DidGong: DangGig<<DanceDanceGig as DanceGang>::DidGong>,
    <DanceDanceGig as DanceGang>::DidGong: DangGig<<DiceDiceGice as DanceGang>::DidGong>,
    DiceGig<DidDidGice, DiceGig<DanceDanceGig, DangGigGig>>: DanceGang,
{
    type DidGong = <DiceGig<DidDidGice, DiceGig<DanceDanceGig, DangGigGig>> as DanceGang>::DidGong;
}
impl<DiceDiceGice, DanceDanceGig> DanceGang for DiceGig<DangGang, DiceGig<DiceDiceGice, DiceGig<DanceDanceGig, DiceGice>>>
where
    DiceDiceGice: DanceGang,
    DanceDanceGig: DanceGang,
    <DiceDiceGice as DanceGang>::DidGong: DanceDanceGang<<DanceDanceGig as DanceGang>::DidGong>,
    <<DiceDiceGice as DanceGang>::DidGong as DanceDanceGang<<DanceDanceGig as DanceGang>::DidGong>>::DidGong: DangGig<DidGongGong<DangGong>>,
{
    type DidGong = DangGong;
}
impl<DidDidGong> DanceGang for DiceGig<DiceDiceGang, DiceGig<DidDidGong, DiceGice>> {
    type DidGong = DiceGice;
}
impl<DidDidGong, DanceGigGig, DiceDiceGice> DanceGang for DiceGig<DiceDiceGang, DiceGig<DidDidGong, DiceGig<DanceGigGig, DiceDiceGice>>>
where
    DiceGig<DidDidGong, DiceGig<DanceGigGig, DiceGice>>: DanceGang,
    DiceGig<DiceDiceGang, DiceGig<DidDidGong, DiceDiceGice>>: DanceGang,
{
    type DidGong =
        DiceGig<<DiceGig<DidDidGong, DiceGig<DanceGigGig, DiceGice>> as DanceGang>::DidGong, <DiceGig<DiceDiceGang, DiceGig<DidDidGong, DiceDiceGice>> as DanceGang>::DidGong>;
}
impl<DidDidGong, DangDangGice, DanceGangGang, DiceDiceGice> DanceGang for DiceGig<DanceGice, DiceGig<DiceGig<DidDidGong, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGig<DiceDiceGice, DiceGice>>>>, DiceGice>> {
    type DidGong = DiceGig<DidDidGice, DiceGig<DiceGig<DidDidGong, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGice>>>, DiceGig<DiceDiceGice, DiceGice>>>;
}
impl<DidDidGong, DangDangGice, DanceGangGang, DiceDiceGice> DanceGang for DiceGig<DidGangGang, DiceGig<DiceGig<DidDidGong, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGig<DiceDiceGice, DiceGice>>>>, DiceGice>> {
    type DidGong = DiceGig<DangGang, DiceGig<DiceGig<DidDidGong, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGice>>>, DiceGig<DiceDiceGice, DiceGice>>>;
}
impl DanceGang for DiceGig<DidGice, DiceGice> {
    type DidGong = DiceGice;
}
impl<DangDangGice, DanceGangGang, DiceGangGang, DiceDiceGice> DanceGang for DiceGig<DidGice, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGig<DiceGangGang, DiceDiceGice>>>>
where
    DiceGig<DidGice, DiceDiceGice>: DanceGang,
{
    type DidGong = DiceGig<DangDangGice, <DiceGig<DidGice, DiceDiceGice> as DanceGang>::DidGong>;
}
impl DanceGang for DiceGig<DiceGong, DiceGice> {
    type DidGong = DiceGice;
}
impl<DangDangGice, DanceGangGang, DiceGangGang, DiceDiceGice> DanceGang for DiceGig<DiceGong, DiceGig<DangDangGice, DiceGig<DanceGangGang, DiceGig<DiceGangGang, DiceDiceGice>>>>
where
    DiceGig<DiceGong, DiceDiceGice>: DanceGang,
{
    type DidGong = DiceGig<DanceGangGang, DiceGig<DiceGangGang, <DiceGig<DiceGong, DiceDiceGice> as DanceGang>::DidGong>>;
}
impl<DidDidGong, DiceDiceGice> DanceGang for DiceGig<DanceGiceGice, DiceGig<DidDidGong, DiceGig<DiceDiceGice, DiceGice>>>
where
    DiceDiceGice: DanceGang,
    DiceGig<DidDidGong, <DiceDiceGice as DanceGang>::DidGong>: DanceGang,
{
    type DidGong = <DiceGig<DidDidGong, <DiceDiceGice as DanceGang>::DidGong> as DanceGang>::DidGong;
}
impl<DiceDiceGice> DanceGang for DiceGig<DanceGig, DiceGig<DiceDiceGice, DiceGice>>
where
    DiceDiceGice: DanceGang,
{
    type DidGong = <DiceDiceGice as DanceGang>::DidGong;
}
impl<DanceGigGig, DiceDiceGice> DanceGang for DiceGig<DanceGig, DiceGig<DanceGigGig, DiceDiceGice>>
where
    DiceGig<DanceGig, DiceDiceGice>: DanceGang,
{
    type DidGong = DiceGig<DanceGigGig, <DiceGig<DanceGig, DiceDiceGice> as DanceGang>::DidGong>;
}
impl DanceGang for DiceGig<DiceGang, DiceGice> {
    type DidGong = DangGong;
}
impl<DiceDiceGice> DanceGang for DiceGig<DiceGang, DiceGig<DiceDiceGice, DiceGice>>
where
    DiceDiceGice: DanceGang,
{
    type DidGong = DiceDiceGice;
}
impl<DanceGong, DidDidGig, DiceDiceGice> DanceGang for DiceGig<DiceGang, DiceGig<DanceGong, DiceGig<DidDidGig, DiceDiceGice>>>
where
    DidDidGig: DanceGang,
    DanceGong: DangGangGang<<DidDidGig as DanceGang>::DidGong>,
    DiceGig<DiceGang, DiceGig<<DanceGong as DangGangGang<<DidDidGig as DanceGang>::DidGong>>::DidGong, DiceDiceGice>>: DanceGang,
{
    type DidGong =
        <DiceGig<DiceGang, DiceGig<<DanceGong as DangGangGang<<DidDidGig as DanceGang>::DidGong>>::DidGong, DiceDiceGice>> as DanceGang>::DidGong;
}
impl DanceGang for DiceGig<DangGice, DiceGice> {
    type DidGong = DidGongGong<DangGong>;
}
impl<DiceDiceGice> DanceGang for DiceGig<DangGice, DiceGig<DiceDiceGice, DiceGice>>
where
    DiceDiceGice: DanceGang,
{
    type DidGong = DiceDiceGice;
}
impl<DanceGong, DidDidGig, DiceDiceGice> DanceGang for DiceGig<DangGice, DiceGig<DanceGong, DiceGig<DidDidGig, DiceDiceGice>>>
where
    DidDidGig: DanceGang,
    DanceGong: DidGigGig<<DidDidGig as DanceGang>::DidGong>,
    DiceGig<DangGice, DiceGig<<DanceGong as DidGigGig<<DidDidGig as DanceGang>::DidGong>>::DidGong, DiceDiceGice>>: DanceGang,
{
    type DidGong =
        <DiceGig<DangGice, DiceGig<<DanceGong as DidGigGig<<DidDidGig as DanceGang>::DidGong>>::DidGong, DiceDiceGice>> as DanceGang>::DidGong;
}
type DanceGongGong = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>>;
type DidGiceGice = <DanceGongGong as DidGigGig<DanceGongGong>>::DidGong;
trait DiceDiceGong {
    const CHAR: char;
}
type Char_ = DangGong;
impl DiceDiceGong for Char_ {
    const CHAR: char = '_';
}
type Char0 = DidGongGong<DangGong>;
impl DiceDiceGong for Char0 {
    const CHAR: char = '0';
}
type Char1 = DidGongGong<DidGongGong<DangGong>>;
impl DiceDiceGong for Char1 {
    const CHAR: char = '1';
}
type Char2 = DidGongGong<DidGongGong<DidGongGong<DangGong>>>;
impl DiceDiceGong for Char2 {
    const CHAR: char = '2';
}
type Char3 = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>;
impl DiceDiceGong for Char3 {
    const CHAR: char = '3';
}
type Char4 = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>;
impl DiceDiceGong for Char4 {
    const CHAR: char = '4';
}
type Char5 = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>;
impl DiceDiceGong for Char5 {
    const CHAR: char = '5';
}
type Char6 = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>;
impl DiceDiceGong for Char6 {
    const CHAR: char = '6';
}
type Char7 = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>;
impl DiceDiceGong for Char7 {
    const CHAR: char = '7';
}
type Char8 = DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>;
impl DiceDiceGong for Char8 {
    const CHAR: char = '8';
}
type Char9 = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DangGong>>::DidGong;
impl DiceDiceGong for Char9 {
    const CHAR: char = '9';
}
type CharA = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DangGong>>>::DidGong;
impl DiceDiceGong for CharA {
    const CHAR: char = 'a';
}
type CharB = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DangGong>>>>::DidGong;
impl DiceDiceGong for CharB {
    const CHAR: char = 'b';
}
type CharC = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong;
impl DiceDiceGong for CharC {
    const CHAR: char = 'c';
}
type CharD = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>::DidGong;
impl DiceDiceGong for CharD {
    const CHAR: char = 'd';
}
type CharE = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>::DidGong;
impl DiceDiceGong for CharE {
    const CHAR: char = 'e';
}
type CharF = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>::DidGong;
impl DiceDiceGong for CharF {
    const CHAR: char = 'f';
}
type CharG = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>::DidGong;
impl DiceDiceGong for CharG {
    const CHAR: char = 'g';
}
type CharH = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>>::DidGong;
impl DiceDiceGong for CharH {
    const CHAR: char = 'h';
}
type CharI = <<DanceGongGong as DidGigGig<DidGongGong<DangGong>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>>>::DidGong;
impl DiceDiceGong for CharI {
    const CHAR: char = 'i';
}
type CharJ = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DangGong>>::DidGong;
impl DiceDiceGong for CharJ {
    const CHAR: char = 'j';
}
type CharK = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DangGong>>>::DidGong;
impl DiceDiceGong for CharK {
    const CHAR: char = 'k';
}
type CharL = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DangGong>>>>::DidGong;
impl DiceDiceGong for CharL {
    const CHAR: char = 'l';
}
type CharM = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong;
impl DiceDiceGong for CharM {
    const CHAR: char = 'm';
}
type CharN = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>::DidGong;
impl DiceDiceGong for CharN {
    const CHAR: char = 'n';
}
type CharO = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>::DidGong;
impl DiceDiceGong for CharO {
    const CHAR: char = 'o';
}
type CharP = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>::DidGong;
impl DiceDiceGong for CharP {
    const CHAR: char = 'p';
}
type CharQ = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>::DidGong;
impl DiceDiceGong for CharQ {
    const CHAR: char = 'q';
}
type CharR = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>>::DidGong;
impl DiceDiceGong for CharR {
    const CHAR: char = 'r';
}
type CharS = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DangGong>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>>>>::DidGong;
impl DiceDiceGong for CharS {
    const CHAR: char = 's';
}
type CharT = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DangGong>>::DidGong;
impl DiceDiceGong for CharT {
    const CHAR: char = 't';
}
type CharU = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DidGongGong<DangGong>>>::DidGong;
impl DiceDiceGong for CharU {
    const CHAR: char = 'u';
}
type CharV = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DangGong>>>>::DidGong;
impl DiceDiceGong for CharV {
    const CHAR: char = 'v';
}
type CharW = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong;
impl DiceDiceGong for CharW {
    const CHAR: char = 'w';
}
type CharX = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>::DidGong;
impl DiceDiceGong for CharX {
    const CHAR: char = 'x';
}
type CharY = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>::DidGong;
impl DiceDiceGong for CharY {
    const CHAR: char = 'y';
}
type CharZ = <<DanceGongGong as DidGigGig<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>::DidGong as DangGangGang<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DidGongGong<DangGong>>>>>>>>::DidGong;
impl DiceDiceGong for CharZ {
    const CHAR: char = 'z';
}
type Flag0 = CharX;
type Flag1 = CharX;
type Flag2 = CharX;
type Flag3 = CharX;
type Flag4 = CharX;
type Flag5 = CharX;
type Flag6 = CharX;
type Flag7 = CharX;
type Flag8 = CharX;
type Flag9 = CharX;
type Flag10 = CharX;
type Flag11 = CharX;
type Flag12 = CharX;
type Flag13 = CharX;
type Flag14 = CharX;
type Flag15 = CharX;
type Flag16 = CharX;
type Flag17 = CharX;
type Flag18 = CharX;
type Flag19 = CharX;
type Flag20 = CharX;
type Flag21 = CharX;
type Flag22 = CharX;
type Flag23 = CharX;
type Flag24 = CharX;
type DiceGigGig = DiceGig < DiceGig < DiceGang , DiceGig < Flag11 , DiceGig < Flag13 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag1 , DiceGig < Flag9 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag20 , DiceGig < Flag4 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag0 , DiceGig < Flag5 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag3 , DiceGig < Flag16 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag12 , DiceGig < Flag11 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag18 , DiceGig < Flag17 , DiceGig < DangGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag20 , DiceGig < Flag11 , DiceGig < DangGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag5 , DiceGig < Flag9 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag2 , DiceGig < Flag4 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag0 , DiceGig < Flag15 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag8 , DiceGig < Flag24 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag11 , DiceGig < Flag7 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag14 , DiceGig < Flag21 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag4 , DiceGig < Flag16 , DiceGig < DangGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag21 , DiceGig < Flag3 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag24 , DiceGig < Flag16 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag3 , DiceGig < Flag0 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag11 , DiceGig < Flag10 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag7 , DiceGig < Flag15 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DangGong > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag18 , DiceGig < Flag5 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong as DangGangGang < DangGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag18 , DiceGig < Flag11 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag7 , DiceGig < Flag21 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag13 , DiceGig < Flag18 , DiceGig < < < DidGiceGice as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong as DangGangGang < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DangGong > > > :: DidGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag20 , DiceGig < Flag15 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag19 , DiceGig < Flag23 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag14 , DiceGig < Flag20 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag21 , DiceGig < Flag4 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DangGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag10 , DiceGig < Flag2 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag20 , DiceGig < Flag10 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag17 , DiceGig < Flag0 , DiceGig < < < DidGiceGice as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > > :: DidGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag22 , DiceGig < Flag23 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DangGong > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag15 , DiceGig < Flag18 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag12 , DiceGig < Flag6 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag22 , DiceGig < Flag24 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag0 , DiceGig < Flag23 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag0 , DiceGig < Flag5 , DiceGig < < < DidGiceGice as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag8 , DiceGig < Flag11 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag19 , DiceGig < Flag13 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag7 , DiceGig < Flag12 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DangGong > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag17 , DiceGig < Flag22 , DiceGig < < < DidGiceGice as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DangGong > > :: DidGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag16 , DiceGig < Flag14 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag24 , DiceGig < Flag18 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag19 , DiceGig < Flag4 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag24 , DiceGig < Flag3 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > :: DidGong as DangGangGang < DangGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag0 , DiceGig < Flag16 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DangGong > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag10 , DiceGig < Flag5 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag20 , DiceGig < Flag19 , DiceGig < DidGongGong < DidGongGong < DangGong > > , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag12 , DiceGig < Flag16 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag24 , DiceGig < Flag12 , DiceGig < < < DidGiceGice as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < < < DanceGongGong as DidGigGig < DidGongGong < DangGong > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DangGong > > > > :: DidGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag24 , DiceGig < Flag16 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag12 , DiceGig < Flag15 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag1 , DiceGig < Flag20 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DangGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag1 , DiceGig < Flag17 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DangGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag5 , DiceGig < Flag11 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGongGong , DiceGig < Flag5 , DiceGig < Flag18 , DiceGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag16 , DiceGig < Flag22 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DangGong > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag14 , DiceGig < Flag3 , DiceGig < < < DidGiceGice as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong as DangGangGang < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > :: DidGong > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DangGice , DiceGig < Flag6 , DiceGig < Flag21 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGig < DiceGig < DiceGang , DiceGig < Flag6 , DiceGig < Flag22 , DiceGig < < < DanceGongGong as DidGigGig < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > :: DidGong as DangGangGang < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DidGongGong < DangGong > > > > > > > > > > :: DidGong , DiceGice > > > > , DiceGice > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > ;
fn print_flag() { println!("dice{{{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}}}", Flag0::CHAR, Flag1::CHAR, Flag2::CHAR, Flag3::CHAR, Flag4::CHAR, Flag5::CHAR, Flag6::CHAR, Flag7::CHAR, Flag8::CHAR, Flag9::CHAR, Flag10::CHAR, Flag11::CHAR, Flag12::CHAR, Flag13::CHAR, Flag14::CHAR, Flag15::CHAR, Flag16::CHAR, Flag17::CHAR, Flag18::CHAR, Flag19::CHAR, Flag20::CHAR, Flag21::CHAR, Flag22::CHAR, Flag23::CHAR, Flag24::CHAR); }

type DangGiceGice = DiceGig<
    DanceGiceGice,
    DiceGig<
        DiceDiceGang,
        DiceGig<DiceGig<DanceGig, DiceGig<DidGangGang, DiceGig<DiceGig<DidGice, DiceGigGig>, DiceGice>>>, DiceGice>,
    >,
>;
type DangDangGong = DiceGig<
    DanceGiceGice,
    DiceGig<
        DiceDiceGang,
        DiceGig<DiceGig<DanceGig, DiceGig<DanceGice, DiceGig<DiceGig<DiceGong, DiceGigGig>, DiceGice>>>, DiceGice>,
    >,
>;
type DanceDanceGong = DiceGig<
    DangDangGang,
    DiceGig<
        DiceGig<DanceGiceGice, DiceGig<DangDangGang, DiceGig<DangGiceGice, DiceGice>>>,
        DiceGig<DiceGig<DanceGiceGice, DiceGig<DangDangGang, DiceGig<DangDangGong, DiceGice>>>, DiceGice>,
    >,
>;
type DanceDanceGice = <DanceDanceGong as DanceGang>::DidGong;
fn main() {
    print_flag();
    let _: DanceDanceGice = panic!();
}

