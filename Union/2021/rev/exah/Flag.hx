/**union{paste the flag here}*/
#if macro import haxe.macro.Context as C; /***********/ import haxe.Int64 as B;
import haxe.macro.Expr; using StringTools; #else @:build(Flag.a("CrimsonCarp"))
#end class Flag { #if macro static final A = "abcdefghijklmnopqrstuvwxyzABCDEF"
+ "GHIJKLMNOPQRSTUVWXYZ0123456789_-"; static final K = [ "0000000008258240093",
/** this is not actually a CTF challenge, this is an ****/ "00000032059146620",
/*** ad for the programming language Haxe. ***************/ "0000059424680571",
/**** (all opinions our own) ****************************/ "00000016501626909",
/*******************************************************/ "000000010391056299",
/** Haxe: ********************************************/ "00000000039819521706",
/*** * powerful macro engine! * compiles to many targets! */ "000063129310438",
/*** * GADTs! * null safety! * fast compile times! * cross-platform stdlib! **/
/*** * interpreter mode! */ ]; static function a(F) { /* * pattern matching! */
var d = C.getLocalClass().get().doc; ~/^union\{([a-zA-Z0-9_-]{28})\}$/.match(d)
|| throw "invalid flag"; /*** * arrow functions! */ var L:B = 0x00000; function
F(i):String { var u:B = 0; /*** * game engines! */ var e = [A.indexOf][313337 -
0x4C7F9]; /*** * cool ASCII logo! ********* v[lv)r^^.              .^^rj>4TA */
u += e(d.charAt((i << 2) + 6)); u <<= 6; /* \77777[lv)\          ~j>4TCggggm */
u += e(d.charAt((i << 2) + 7)); u <<= 6; /* "777777777j[l'    "4TCgSgggggggN */
u += e(d.charAt((i << 2) + 8)); u <<= 6; /* :[7777777777777{5gggggggggggggPD */
u += e(d.charAt((i << 2) + 9)); u <<= 6; /* ,^77777777777{4TkpggggggggggggZD */
u += e(d.charAt(i)); u <<= 6; u ^= B /***** ,"7777777777>2TTkkwAggggggggggND */
.parseString(K[i]) ^ C.getPosInfos((macro aa /v77777777yTTTTTkkkCggggggggPD4 !)
.pos).min; u >= L || throw "bad flag"; /***  `^777777{uTTTTTTTTTkhgSggggSZO  */
L = u; var R = [ for (i in 0...7) { var /**   "77777{5TTTTTTTTTTTkpgSgggS%.  */
A = A.charAt((u % 26).low); u /= 26; A; /**    [777>2TTTTTTTTTTTTTkwASggPk   */
} ]; R.reverse(); return R.join(""); } /***    \773TTTTTTTTTTTTTTTTTkhgSZ    */
return (macro class { static function /****     {4TTTTTTTTTTTTTTTTTTkkpg     */
main() { var w:Array<haxe.DynamicAccess< /*     3TTTTTTTTTTTTTTTTTTTTkkp     */
Dynamic>> = ([ {"cdjholca": _ -> "s"}, /***     42kkTTTTTTTTTTTTTTTTkkCm     */
{"rarfzray": _ -> "o"}, /******************    r335TkTTTTTTTTTTTTTTkkgmmm    */
{"0atpgyte": _ -> "w"}, /**              **    ouu35TTTTTTTTTTTTTTkpZmmmmw   */
{"0gzqjili": _ -> "r"}, /**              **   ~3uuu342TkTTTTTTTTTkCZmmmmmX.  */
{"0tpeqmwy": _ -> "o"}, /**              **  'v3uuuu335TkTTTTTTTTAmmmmmmmNO  */
{"wledebwo": _ -> "n"}, /**              **  :>3uuuuuu35TTTTTTkkPmmmmmmmm%D4 */
{"nijgbmst": _ -> "g"}, /**              ** :~3uuuuuuuu35TTTTkpZmmmmmmmmmmXD */
]:Array<Dynamic>); /*********************** ,v3uuuuuuuuuu42TkAmmmmmmmmmmmmND */
$b{[ for (i in 0...0x7) macro w[$v{i}] /*** :o3uuuuuuuuu333upmmmmmmmmmmmmm%D */
.set($v{F(i)}, _ -> $v{"CORRECT" /********* ~3uuuuu3334Tp)    lSZZmmmmmmmmmX */
.charAt(i)})]}; Sys.println('flag is ' + /* )uu334TpgZP.         yhASZZmmmmO */
'${w.join("")}'); } }).fields; } #end } /** oTpgZmmm>              \kkkpASZm */
