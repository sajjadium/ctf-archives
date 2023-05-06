class Encrypt {
    public static void main(String[] args) {
        String phrase = "";
       /* flag{*/ System.out.println(encr(apjubh(phrase))); /* } */
       // put it in a flag format
    }

    public static String apjubh(String word) {
        String rw = "";
        for (int j = word.length() -1; j >= 0; j--) {
            rw = rw + word.charAt(j);
        }
        return rw;
    }

    public static String encr(String jjm) {
        char[] chars = jjm.toCharArray();
        String res = "";
        int key = (int)(Math.random() * 5) + 1;
        for (char c : chars) {
            c += key;
            res += Character.toString(c);
        }
        res = res.replace('~', 'Z');
        res = res.replace('%', 'Q');
        return res;
    }

}