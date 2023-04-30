public class RegularBank {
    public static Long[] me = init();
    public static Long[] someoneElse = init();
    public static Long[] anotherStranger = init();
    static Long[] init() {
        var ret = new Long[10];
        for (int i = 0; i < 10; ++i) {
            ret[i] = new Long(0);
        }
        return ret;
    }
}
