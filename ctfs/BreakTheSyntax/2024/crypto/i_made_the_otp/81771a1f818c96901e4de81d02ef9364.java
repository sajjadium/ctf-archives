import java.io.*;
import java.util.Random;
import java.nio.file.Files;
import java.nio.file.Paths;

public class GeneratePad {
    public static void main(String args[]) throws NumberFormatException, IOException {
        if (args.length != 1) {
            System.out.println("Usage: <size of key in bytes>");
            System.exit(1);
        }
        int size = Integer.parseInt(args[0]);
        Random rand = new Random();
        byte[] randBytes = new byte[size];
        rand.nextBytes(randBytes);
        Files.write(Paths.get("key.bin"), randBytes);
    }
}
