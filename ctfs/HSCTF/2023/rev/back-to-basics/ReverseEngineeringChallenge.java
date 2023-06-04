import java.util.Scanner;

class ReverseEngineeringChallenge {
    public static void main(String args[]) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter password: ");
        String userInput = scanner.next();
        if (checkPassword(userInput)) {
            System.out.println("Access granted.");
        } else {
            System.out.println("Access denied!");
        }
    }

    public static boolean checkPassword(String password) {
        return password.length() == 20 &&
                password.charAt(0) == 'f' &&
                password.charAt(11) == '_' &&
                password.charAt(1) == 'l' &&
                password.charAt(6) == '0' &&
                password.charAt(3) == 'g' &&
                password.charAt(8) == '1' &&
                password.charAt(4) == '{' &&
                password.charAt(9) == 'n' &&
                password.charAt(7) == 'd' &&
                password.charAt(10) == 'g' &&
                password.charAt(2) == 'a' &&
                password.charAt(12) == 'i' &&
                password.charAt(5) == 'c' &&
                password.charAt(17) == 'r' &&
                password.charAt(14) == '_' &&
                password.charAt(18) == 'd' &&
                password.charAt(16) == '4' &&
                password.charAt(19) == '}' &&
                password.charAt(15) == 'h' &&
                password.charAt(13) == '5';
    }
}
