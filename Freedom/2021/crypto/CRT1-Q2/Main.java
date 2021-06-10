
public class Main {
   public static void main(String args[]) {
      int columnCount = 8;
      int rowCount = 5;

      String word = ""; // flag
      System.out.println(word);
      String[][] letterMatrix = new String[5][8];
      letterMatrix = retArry(rowCount, columnCount, word, letterMatrix);
      String enc = enYBlock(letterMatrix); // final encrypted 
      System.out.println(enc);
      String bbstr = enXBlock(enc);
      System.out.println("flag{" + bbstr + "}");
      //  the output should be flag{74CEE12EB1C1A00FF30FD37B74EF2477B37C957D}
   }


   static String[][] retArry(int row, int col, String str, String[][] lmatr) {
      for (int r = 0; r < row; r++) {
         for (int c = 0; c < col; c++) {
            if (str.length() > (c + (r * col))) {
               lmatr[r][c] = str.substring(c + r * col, 1 + c + r * col);
            } else {
               lmatr[r][c] = "Z";
            }
         }
      }
      return lmatr;
   }

   static String enYBlock(String[][] letterMatrix) {
      int csurrentS = 0;
      String encStr = "";
      for (int i = 0; i <= csurrentS; i++) {
         for (int j = 0; j < letterMatrix.length; j++) {
            encStr += letterMatrix[j][csurrentS];
         }
         csurrentS++;
         if (csurrentS >= letterMatrix[0].length) {
            break;
         }
      }
      return encStr;
   }
   static String enXBlock(String bbstr) {
      char[] letters = bbstr.toCharArray();
      String emt = "";
      for (int i = letters.length - 1; i >= 0; i--) {
         emt += letters[i];
     }
      return emt;
   }
}
