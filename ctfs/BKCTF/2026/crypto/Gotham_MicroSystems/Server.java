import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.SecureRandom;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server {
    // final vars
    private static final int PORT = 5000;
    private static final String FLAG = "bkctf{test_flag}";

    // TODO: Remove unused username, was a remnant of a previous challenge idea
    private static final String USERNAME = "Barbara_Gordon";

    private static String WELCOME = "Hello Unknown User! Unfortunately, the API key (%s) is hidden behind super duper secret encryption. Good luck guessing!";

    // generated keyspace and shit
    private static byte[] key;
    private static byte[] iv;

    // generated ciphertext
    private static byte[] encBytes;
    private static byte[] plaintext;
    private static String encString = ""; // TODO: Remove this

    public static void main(String[] args) throws Exception {
        // Generate key and initialization vector
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256);
        key = keyGen.generateKey().getEncoded(); 
        iv = new byte[16]; // block size of 16.

        new SecureRandom().nextBytes(iv);
        IvParameterSpec init_vec = new IvParameterSpec(iv);

        // Setup Ciphers
        Cipher encryptCipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        encryptCipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key, "AES"), init_vec);

        // Encrypt flag
        // I heard salting the key before encrypting it is supposed to be super secure
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);
        plaintext = new byte[16 + FLAG.length()];

        System.arraycopy(salt, 0, plaintext, 0, 16);
        System.arraycopy(FLAG.getBytes("UTF-8"), 0, plaintext, 16, FLAG.length());

        encBytes = encryptCipher.doFinal(plaintext);
        for (byte i : encBytes) {
            encString += String.format("%02X", i);
        }
        String iv_string = "";
        for (byte i : iv) {
            iv_string += String.format("%02X", i);
        }

        // Log to console for debugging purposes
        System.out.println(encString);
        System.out.println(iv_string);

        // Generate welcome text
        WELCOME = String.format(WELCOME, encString);

        // Start the server
        ServerSocket serverSocket = null;
        Socket socket = null;
        try {
            // sErVeR sOcKeT nEvEr ClOsEd
            serverSocket = new ServerSocket(PORT);
        } catch (Exception e) {
            System.out.println("Exception occurred");
            return;
        }

        ExecutorService pool = Executors.newFixedThreadPool(50); // max 50 clients
        while (true) {
            try {
                socket = serverSocket.accept();
                pool.execute(new ServerThread(socket));
            } catch (Exception e) {
                continue;
            }
        }
    }

    private static class ServerThread extends Thread {
        Socket socket;

        public ServerThread(Socket socket) {
            this.socket = socket;
    
        }

        public void run() {
            try (
                BufferedReader in  = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                DataOutputStream out = new DataOutputStream(socket.getOutputStream());
            ) {
               
                out.writeBytes(WELCOME + "\n\r");

                while (true) {
                    out.writeBytes("Enter a guess of the API key (hex string) > ");
                    out.flush();
                    String uInput = in.readLine();
                    // System.out.writeBytes(uInput + "\n\r");

                    if (uInput != null && uInput.equals(encString)) {
                        out.writeBytes("Nice try lmao \n\r");
                        out.flush();
                        continue;
                    }
                    
                    byte[] userBytes = null;
                    try {
                        userBytes = HexFormat.of().parseHex(uInput);
                    } catch (Exception e) {
                        out.writeBytes("Invalid Hex String. Exiting...\n\r");
                        out.flush();
                        break;
                    }
                    
                    byte[] decBytes = null;
                    try {
                        // Decrypt things
                        Cipher decryptCipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
                        decryptCipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(key, "AES"),new IvParameterSpec(iv));
                        decBytes = decryptCipher.doFinal(userBytes);
                    } catch (Exception e) {
                        if (e instanceof BadPaddingException) {
                            // Lets be a bit more forgiving here, maybe the user mistyped something
                            out.writeBytes("Bad Padding. Please try again\n\r");
                            out.flush();
                        } else {
                            out.writeBytes("An Unknown Exception Occurred. Exiting...\n\r");
                            out.flush();
                            break;
                        }
                        continue;
                    }
                    
                    // Check if we have output
                    if (decBytes != null && Arrays.equals(decBytes, plaintext)) {
                        // This will never be reached :)
                        out.writeBytes(String.format("API Key Decryption Successful. Welcome user %s. Your flag is %s\n\r", USERNAME, FLAG));
                        out.flush();
                        break;
                    } else {
                        out.writeBytes("Invalid API Key. Please Try Again \n\r");
                        out.flush();
                    }
                }
            } catch (IOException e) {
                System.out.println("ioexception");
                e.printStackTrace();
                return;
            } finally {
                try {
                    socket.close();
                } catch (IOException e) { /* ignore this */ }
            }
        }
    }
}
