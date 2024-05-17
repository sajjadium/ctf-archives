import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

public class OTPCrypt {
    public static void main(String args[]) throws IOException {
        if (args.length != 2) {
            System.out.println("Usage: <infile> <outfile>");
            System.exit(1);
        }
        String inFileName = args[0];
        String outFileName = args[1];
        byte[] fileData = Files.readAllBytes(Paths.get(inFileName));
        byte[] keyData = Files.readAllBytes(Paths.get("key.bin"));
        if (keyData.length < fileData.length) {
            System.out.println("Key file cannot be shorter than data file");
            System.exit(2);
        }
        for (int i=0; i < fileData.length; i++) {
            fileData[i] ^= keyData[i];
        }
        Files.write(Paths.get(outFileName), fileData);
        System.out.println("Operation finished");
    }
}
