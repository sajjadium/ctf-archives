import Data.Bits (xor)
encrypt = ((<~)<$>). ((.) (@++) $mess .unzip .t .(fromEnum<$>))
(.:) = (.)(.)(.)
t = let t // [] = t; t // (x:xs) = ((x,head $xs):t) // tail xs in (//)[]
mess a = ((((.) head $((.)(($3)<$>) $((<$>) $flip (.)(*2)) .((<$>)(-))) .(:[]))<$>) .(.:) fst id id $a, (!) .snd $a)
     where (!) (x:xs) = (:)x $(@++) .unzip $t xs
(@++)(a,b) = (++) a $map (xor 104) $uncurry xor <$> zip a b
(<~) = (.) id ($) (toEnum::Int->Char) .foldl1(*) .(:[])
main = (putStrLn.show) $encrypt "ictf{REDACTED}" == "f-Yefl*Y+E:Y.Y-.uncs#E~fa/npA?e/H;rKlg"
