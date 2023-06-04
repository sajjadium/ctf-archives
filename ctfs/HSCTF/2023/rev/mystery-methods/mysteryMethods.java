import java.util.Base64;
import java.util.Scanner;

public class mysteryMethods{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Flag: ");
        String userInput = scanner.nextLine();
        String encryptedInput = encryptInput(userInput);

        if (checkFlag(encryptedInput)) {
            System.out.println("Correct flag! Congratulations!");
        } else {
            System.out.println("Incorrect flag! Please try again.");
        }
    }

    public static String encryptInput(String input) {
        String flag = input;
        flag = unknown2(flag, 345345345);
        flag = unknown1(flag);
        flag = unknown2(flag, 00000);
        flag = unknown(flag, 25);
        return flag;
    }

    public static boolean checkFlag(String encryptedInput) {
        return encryptedInput.equals("OS1QYj9VaEolaDgTSTXxSWj5Uj5JNVwRUT4vX290L1ondF1z");
    }

    public static String unknown(String input, int something) {
        StringBuilder result = new StringBuilder();
        for (char c : input.toCharArray()) {
            if (Character.isLetter(c)) {
                char base = Character.isUpperCase(c) ? 'A' : 'a';
                int offset = (c - base + something) % 26;
                if (offset < 0) {
                    offset += 26;
                }
                c = (char) (base + offset);
            }
            result.append(c);
        }
        return result.toString();
    }

    public static String unknown1(String xyz) {
        return new StringBuilder(xyz).reverse().toString();
    }

    public static String unknown2(String xyz, int integer) {
        return Base64.getEncoder().encodeToString(xyz.getBytes());
    }
}
