class CompileMe
{
    static string X(Func<bool, string> _) => Y(_);
    static string X(Func<byte, string> _) => Y(_);
    static string X(Func<sbyte, string> _) => Y(_);
    static string X(Func<short, string> _) => Y(_);
    static string X(Func<ushort, string> _) => Y(_);
    static string X(Func<int, string> _) => Y(_);
    static string X(Func<uint, string> _) => Y(_);
    static string X(Func<long, string> _) => Y(_);
    static string X(Func<ulong, string> _) => Y(_);
    static string Y<T>(Func<T, string> _) where T : struct => typeof(T).Name + _(default);
    static string Z<A, B, C, D, E, F, G, H, I>(A a, B b, C c, D d, E e, F f, G g, H h, I i) => "";
    static void Z<AB, C, D, E, F, G, H, I>(AB a, AB b, C c, D d, E e, F f, G g, H h, I i) { }
    static void Z<AC, B, D, E, F, G, H, I>(AC a, B b, AC c, D d, E e, F f, G g, H h, I i) { }
    static void Z<AD, B, C, E, F, G, H, I>(AD a, B b, C c, AD d, E e, F f, G g, H h, I i) { }
    static void Z<AE, B, C, D, F, G, H, I>(AE a, B b, C c, D d, AE e, F f, G g, H h, I i) { }
    static void Z<AF, B, C, D, E, G, H, I>(AF a, B b, C c, D d, E e, AF f, G g, H h, I i) { }
    static void Z<AG, B, C, D, E, F, H, I>(AG a, B b, C c, D d, E e, F f, AG g, H h, I i) { }
    static void Z<AH, B, C, D, E, F, G, I>(AH a, B b, C c, D d, E e, F f, G g, AH h, I i) { }
    static void Z<AI, B, C, D, E, F, G, H>(AI a, B b, C c, D d, E e, F f, G g, H h, AI i) { }
    static void Z<A, BC, D, E, F, G, H, I>(A a, BC b, BC c, D d, E e, F f, G g, H h, I i) { }
    static void Z<A, BD, C, E, F, G, H, I>(A a, BD b, C c, BD d, E e, F f, G g, H h, I i) { }
    static void Z<A, BE, C, D, F, G, H, I>(A a, BE b, C c, D d, BE e, F f, G g, H h, I i) { }
    static void Z<A, BF, C, D, E, G, H, I>(A a, BF b, C c, D d, E e, BF f, G g, H h, I i) { }
    static void Z<A, BG, C, D, E, F, H, I>(A a, BG b, C c, D d, E e, F f, BG g, H h, I i) { }
    static void Z<A, BH, C, D, E, F, G, I>(A a, BH b, C c, D d, E e, F f, G g, BH h, I i) { }
    static void Z<A, BI, C, D, E, F, G, H>(A a, BI b, C c, D d, E e, F f, G g, H h, BI i) { }
    static void Z<A, B, CD, E, F, G, H, I>(A a, B b, CD c, CD d, E e, F f, G g, H h, I i) { }
    static void Z<A, B, CE, D, F, G, H, I>(A a, B b, CE c, D d, CE e, F f, G g, H h, I i) { }
    static void Z<A, B, CF, D, E, G, H, I>(A a, B b, CF c, D d, E e, CF f, G g, H h, I i) { }
    static void Z<A, B, CG, D, E, F, H, I>(A a, B b, CG c, D d, E e, F f, CG g, H h, I i) { }
    static void Z<A, B, CH, D, E, F, G, I>(A a, B b, CH c, D d, E e, F f, G g, CH h, I i) { }
    static void Z<A, B, CI, D, E, F, G, H>(A a, B b, CI c, D d, E e, F f, G g, H h, CI i) { }
    static void Z<A, B, C, DE, F, G, H, I>(A a, B b, C c, DE d, DE e, F f, G g, H h, I i) { }
    static void Z<A, B, C, DF, E, G, H, I>(A a, B b, C c, DF d, E e, DF f, G g, H h, I i) { }
    static void Z<A, B, C, DG, E, F, H, I>(A a, B b, C c, DG d, E e, F f, DG g, H h, I i) { }
    static void Z<A, B, C, DH, E, F, G, I>(A a, B b, C c, DH d, E e, F f, G g, DH h, I i) { }
    static void Z<A, B, C, DI, E, F, G, H>(A a, B b, C c, DI d, E e, F f, G g, H h, DI i) { }
    static void Z<A, B, C, D, EF, G, H, I>(A a, B b, C c, D d, EF e, EF f, G g, H h, I i) { }
    static void Z<A, B, C, D, EG, F, H, I>(A a, B b, C c, D d, EG e, F f, EG g, H h, I i) { }
    static void Z<A, B, C, D, EH, F, G, I>(A a, B b, C c, D d, EH e, F f, G g, EH h, I i) { }
    static void Z<A, B, C, D, EI, F, G, H>(A a, B b, C c, D d, EI e, F f, G g, H h, EI i) { }
    static void Z<A, B, C, D, E, FG, H, I>(A a, B b, C c, D d, E e, FG f, FG g, H h, I i) { }
    static void Z<A, B, C, D, E, FH, G, I>(A a, B b, C c, D d, E e, FH f, G g, FH h, I i) { }
    static void Z<A, B, C, D, E, FI, G, H>(A a, B b, C c, D d, E e, FI f, G g, H h, FI i) { }
    static void Z<A, B, C, D, E, F, GH, I>(A a, B b, C c, D d, E e, F f, GH g, GH h, I i) { }
    static void Z<A, B, C, D, E, F, GI, H>(A a, B b, C c, D d, E e, F f, GI g, H h, GI i) { }
    static void Z<A, B, C, D, E, F, G, HI>(A a, B b, C c, D d, E e, F f, G g, HI h, HI i) { }

    public static void Main()
    {
        var key =
            Y<long>(H=>X(He=>X(Li=>X(Be=>X(B=>X(C=>X(N=>X(O=>X(F=>
            X(Ne=>X(Na=>Y<sbyte>(Mg=>Y<int>(Al=>X(Si=>X(P=>X(S=>X(Cl=>X(Ar=>
            X(K=>Y<uint>(Ca=>X(Sc=>X(Ti=>Y<ulong>(V=>X(Cr=>Y<byte>(Mn=>X(Fe=>X(Co=>
            X(Ni=>Y<ushort>(Cu=>X(Zn=>X(Ga=>X(Ge=>Y<uint>(As=>X(Se=>X(Br=>X(Kr=>
            X(Rb=>X(Sr=>X(Y=>X(Zr=>Y<short>(Nb=>Y<ushort>(Mo=>Y<uint>(Tc=>X(Ru=>X(Rh=>
            X(Pd=>X(Ag=>X(Cd=>Y<bool>(In=>X(Sn=>X(Sb=>X(Te=>Y<sbyte>(I=>X(Xe=>
            X(Cs=>X(Ba=>Y<bool>(La=>X(Ce=>X(Pr=>X(Nd=>X(Pm=>Y<int>(Sm=>Y<long>(Eu=>
            X(Gd=>X(Tb=>Y<long>(Dy=>Y<ushort>(Ho=>X(Er=>X(Tm=>X(Yb=>Y<bool>(Lu=>X(Hf=>
            X(Ta=>Y<ulong>(W=>X(Re=>X(Os=>X(Ir=>X(Pt=>Y<short>(Au=>X(Hg=>X(Tl=>string.Concat(
                Z(H, He, Li, Be, B, C, N, O, F),
                Z(Ne, Na, Mg, Al, Si, P, S, Cl, Ar),
                Z(K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co),
                Z(Ni, Cu, Zn, Ga, Ge, As, Se, Br, Kr),
                Z(Rb, Sr, Y, Zr, Nb, Mo, Tc, Ru, Rh),
                Z(Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe),
                Z(Cs, Ba, La, Ce, Pr, Nd, Pm, Sm, Eu),
                Z(Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf),
                Z(Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl),
                Z(H, Ne, K, Ni, Rb, Pd, Cs, Gd, Ta),
                Z(He, Na, Ca, Cu, Sr, Ag, Ba, Tb, W),
                Z(Li, Mg, Sc, Zn, Y, Cd, La, Dy, Re),
                Z(Be, Al, Ti, Ga, Zr, In, Ce, Ho, Os),
                Z(B, Si, V, Ge, Nb, Sn, Pr, Er, Ir),
                Z(C, P, Cr, As, Mo, Sb, Nd, Tm, Pt),
                Z(N, S, Mn, Se, Tc, Te, Pm, Yb, Au),
                Z(O, Cl, Fe, Br, Ru, I, Sm, Lu, Hg),
                Z(F, Ar, Co, Kr, Rh, Xe, Eu, Hf, Tl),
                Z(H, He, Li, Ne, Na, Mg, K, Ca, Sc),
                Z(Be, B, C, Al, Si, P, Ti, V, Cr),
                Z(N, O, F, S, Cl, Ar, Mn, Fe, Co),
                Z(Ni, Cu, Zn, Rb, Sr, Y, Pd, Ag, Cd),
                Z(Ga, Ge, As, Zr, Nb, Mo, In, Sn, Sb),
                Z(Se, Br, Kr, Tc, Ru, Rh, Te, I, Xe),
                Z(Cs, Ba, La, Gd, Tb, Dy, Ta, W, Re),
                Z(Ce, Pr, Nd, Ho, Er, Tm, Os, Ir, Pt),
                Z(Pm, Sm, Eu, Yb, Lu, Hf, Au, Hg, Tl)
            ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))));

        var enc = Convert.FromBase64String("To8nQU1OWzL4qzlMYUPPeCI68VIueVeBrtZYuNkHv5TfVXoriYjNIW23S0DHdPNQW84enVObbXmPF6O1xs1+9MiWVAu6T39L");
        Console.WriteLine(string.Concat(new Rfc2898DeriveBytes(key, 0).GetBytes(99).Zip(enc, (a, b) => (char)(a ^ b))));
    }
}
