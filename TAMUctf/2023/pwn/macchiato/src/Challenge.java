import java.util.Scanner;

public class Challenge {
    public static void displayBank(Class bank) {
        System.out.println();
        System.out.println(bank.getSimpleName());
        System.out.println("----------------------------");
        for (var f: bank.getDeclaredFields()) {
            System.out.println(f.getName());
        }
    }
    public static void listUsers() {
        displayBank(RegularBank.class);
        displayBank(BlazinglyFastBank.class);
    }
    public static Object load(String name, String field) {
        try {
            return load(Class.forName(name), field);
        } catch (Exception e) {
            return null;
        }
    }
    public static Object load(Class c, String field) {
        try {
            var f = c.getDeclaredField(field);
            f.setAccessible(true);
            return f.get(null);
        } catch (Exception e) {
            return null;
        }
    }
    public static long readLong(Scanner sc) {
        var ret = sc.nextLong();
        sc.nextLine();
        return ret;
    }
    public static void main(String[] args) {
        var sc = new Scanner(System.in);
        Account acc = null;
        var canZoom = false;

        System.out.println("Welcome to the most secure banking system on the planet!\n");
        while (true) {
            System.out.println("\n1) Login");
            System.out.println("2) Manage funds");
            System.out.println("3) Upgrade user");
            System.out.println("4) Exit");
            System.out.println("\nEnter an option:");
            switch ((int)readLong(sc)) {
                case 1:
                    System.out.println("\nHere are the available banks and users:");
                    listUsers();
                    System.out.println("\nEnter your bank name:");
                    var bank = sc.nextLine();
                    var requestedZoomies = bank.equals("BlazinglyFastBank");
                    if (requestedZoomies && !canZoom) {
                        System.out.println("\nConsider becoming a regular customer to upgrade to our blazingly fast account system.\n");
                        break;
                    }
                    System.out.println("\nEnter your username:");
                    var name = sc.nextLine();
                    var tmp = load(bank, name);
                    if (tmp == null) {
                        System.out.println("\nInvalid account.");
                        break;
                    }
                    if (requestedZoomies) {
                        acc = new BlazinglyFastAccount(long[].class.cast(tmp));
                    } else {
                        acc = new RegularAccount(Long[].class.cast(tmp));
                    }
                    System.out.printf("\nSuccessfuly logged in with ID %d!\n", acc.hashCode());
                    break;
                case 2:
                    if (acc == null) {
                        System.out.println("\nYou need to login to an account first.");
                        break;
                    }
                    var exitInner = false;
                    while (!exitInner) {
                        System.out.println("\n1) Examine balance");
                        System.out.println("2) Withdraw funds");
                        System.out.println("3) Go back");
                        System.out.println("\nEnter an option:");
                        switch ((int)readLong(sc)) {
                            case 1:
                                System.out.println("\nEnter an account number (0-10):");
                                System.out.printf("\nYour balance is now $%d\n", acc.get(readLong(sc)));
                                break;
                            case 2:
                                System.out.println("\nEnter an account number (0-10):");
                                var withdrawIndex = readLong(sc);
                                System.out.println("\nEnter an amount to withdraw:");
                                var v = readLong(sc);
                                if (v >= 0) {
                                    acc.withdraw(withdrawIndex, v);
                                } else {
                                    System.out.println("\nYou can't withdraw negative money.");
                                }
                                break;
                            case 3:
                                exitInner = true;
                                break;
                            default:
                                System.out.println("\nInvalid option.");
                        }
                    }
                    break;
                case 3:
                    if (acc == null) {
                        System.out.println("\nYou need to login to an account first.");
                        break;
                    }
                    if (acc.sum() == Long.MAX_VALUE) {
                        canZoom = true;
                    } else {
                        System.out.println("\nDeposit more money to upgrade to our blazingly fast account system.\n");
                    }
                    break;
                case 4:
                    System.out.println("Bye!");
                    return;
                default:
                    System.out.println("\nInvalid option.");
            }
        }
    }
}
