import java.util.Base64;
import java.util.Scanner;

public class mysteryMethods {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Flag: ");
        String userInput = scanner.nextLine();
        String encryptedInput = encryptInput(userInput);

        // Print the encrypted input for debugging
        System.out.println("Encrypted input: " + encryptedInput);

        if (checkFlag(encryptedInput)) {
            System.out.println("Correct flag! Congratulations!");
        } else {
            System.out.println("Incorrect flag! Please try again.");
        }
    }

    public static String encryptInput(String input) {
        String flag = input;
        flag = toBase64(flag, 345345345);
        System.out.println("After first Base64: " + flag);
        flag = reverseStr(flag, 54321);
        System.out.println("After reversing: " + flag);
        flag = toBase64(flag, 12345);
        System.out.println("After second Base64: " + flag);
        flag = shift(flag, 25, 67890);
        System.out.println("After shifting: " + flag);
        flag = toHex(flag, 98765);
        System.out.println("After hex conversion: " + flag);
        flag = xorWithKey(flag, 9, 56789);
        System.out.println("After XOR: " + flag);
        return flag;
    }

    public static boolean checkFlag(String encryptedInput) {
        // Known encrypted flag
        String knownEncryptedFlag = "465a38585060405f685f4465734d6a636d4f45705f4e67384565403d5d5c6e506d5d3c4d513a513c5862663c58636a736a5c404d504e6639453866676d4f3873";
        return encryptedInput.equals(knownEncryptedFlag);
    }

    public static String toBase64(String input, int dummy) {
        return Base64.getEncoder().encodeToString(input.getBytes());
    }

    public static String reverseStr(String input, int dummy) {
        return new StringBuilder(input).reverse().toString();
    }

    public static String shift(String input, int amount, int dummy) {
        StringBuilder result = new StringBuilder();
        for (char c : input.toCharArray()) {
            if (Character.isLetter(c)) {
                char base = Character.isUpperCase(c) ? 'A' : 'a';
                int offset = (c - base + amount) % 26;
                if (offset < 0) {
                    offset += 26;
                }
                c = (char) (base + offset);
            }
            result.append(c);
        }
        return result.toString();
    }

    public static String toHex(String input, int dummy) {
        StringBuilder hex = new StringBuilder();
        for (char c : input.toCharArray()) {
            hex.append(String.format("%02x", (int) c));
        }
        return hex.toString();
    }

    public static String xorWithKey(String hexInput, int key, int dummy) {
        StringBuilder xored = new StringBuilder();
        for (int i = 0; i < hexInput.length(); i += 2) {
            int hexChar = Integer.parseInt(hexInput.substring(i, i + 2), 16);
            hexChar ^= key;
            xored.append(String.format("%02x", hexChar));
        }
        return xored.toString();
    }
}
