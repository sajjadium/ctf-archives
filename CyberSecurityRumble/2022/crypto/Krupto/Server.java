import java.security.*;
import java.util.Base64;
import java.util.Arrays;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.*;

class Server {
    // Message that needs to be signed
    static String MSG = "I am allowed to get a flag!";

    public static void main(String[] args) throws Throwable {
        System.out.println("Welc0me to the CSR22 Bug B0untay.");
        System.out.println("We present an extra hardend signature implementation here.");
        System.out.println("If you manage to forge a signature, you'll be rerwarded with a flag!");

        KeyPair keys = KeyPairGenerator.getInstance("EC").generateKeyPair();
        Signature sig = Signature.getInstance("SHA256WithECDSAInP1363Format");
        System.out.printf("My Public Key is:\n %s\n", keys.getPublic());

        sig.initVerify(keys.getPublic());
        sig.update(MSG.getBytes());
        
        System.out.println("Enter signature in Base64:");
        String signatureEncoded = new BufferedReader(new InputStreamReader(System.in)).readLine();

        byte[] decodedBytes = Base64.getDecoder().decode(signatureEncoded);

        if (decodedBytes.length != 64 || Arrays.equals(decodedBytes, new byte[64])) {
            System.out.println("REPELLED ATTACK OF RECENTLY FOUND VULNERABILITY!");
            System.exit(0);
        }
        if (sig.verify(decodedBytes)) {
            // this will never happen
            System.out.println("Congrats!");
            Path filePath = Path.of("/opt/flag.txt");
            String flag = Files.readString(filePath);
            System.out.println(flag);
        } else {
            System.out.println("Signature invalid!");
        }
    }
}
