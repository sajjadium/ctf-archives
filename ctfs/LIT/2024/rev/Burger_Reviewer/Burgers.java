import java.util.*;

public class Burgers {
	
	public static boolean bun(String s) {
		return (s.substring(0, 7).equals("LITCTF{") && s.charAt(s.length()-1) == '}');
	}
	
	public static boolean cheese(String s) {
		return (s.charAt(13) == '_' && (int)s.charAt(17) == 95 && s.charAt(19) == '_' && s.charAt(26)+s.charAt(19) == 190 && s.charAt(29) == '_' && s.charAt(34)-5 == 90 && s.charAt(39) == '_');
	}
	
	public static boolean meat(String s) {
		boolean good = true;
		int m = 41;
		char[] meat = {'n', 'w', 'y', 'h', 't', 'f', 'i', 'a', 'i'};
		int[] dif = {4, 2, 2, 2, 1, 2, 1, 3, 3};
		for (int i = 0; i < meat.length; i++) {
			m -= dif[i];
			if (s.charAt(m) != meat[i]) {
				good = false;
				break;
			}
		}
		return good;
	}
	
	public static boolean pizzaSauce(String s) {
		boolean[] isDigit = {false, false, false, true, false, true, false, false, true, false, false, false, false, false};
		for (int i = 7; i < 21; i++) {
			if (Character.isDigit(s.charAt(i)) != isDigit[i - 7]) {
				return false;
			}
		}
		char[] sauce = {'b', 'p', 'u', 'b', 'r', 'n', 'r', 'c'};
		int a = 7; int b = 20; int i = 0; boolean good = true;
		while (a < b) {
			if (s.charAt(a) != sauce[i] || s.charAt(b) != sauce[i+1]) {
				good = false;
				break;
			}
			a++; b--; i += 2;
			while (!Character.isLetter(s.charAt(a))) a++;
			while (!Character.isLetter(s.charAt(b))) b--;
		}
		return good;
	}
	
	public static boolean veggies(String s) {
		int[] veg1 = {10, 12, 15, 22, 23, 25, 32, 36, 38, 40};
		int[] veg = new int[10];
		for (int i = 0; i < veg1.length; i++) {
			veg[i] = Integer.parseInt(s.substring(veg1[i], veg1[i]+1));
		}
		return (veg[0] + veg[1] == 14 && veg[1] * veg[2] == 20 && veg[2]/veg[3]/veg[4] == 1 && veg[3] == veg[4] && veg[3] == 2 && veg[4] - veg[5] == -3 && Math.pow(veg[5], veg[6]) == 125 && veg[7] == 4 && veg[8] % veg[7] == 3 && veg[8] + veg[9] == 9 && veg[veg.length - 1] == 2);
	}

	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		System.out.println("Can burgers be pizzas? Try making a burger...");
		System.out.print("Enter flag: ");
		String input = in.next();
		in.close();
		
		boolean gotFlag = true;
		
		if (input.length() > 42) {
			System.out.println("This burger iz too big :(");
		} else if (input.length() < 42) {
			System.out.println("This burger iz too small :(");
		} else {
			if (!bun(input)) {
				System.out.println("Wrong bun >:0");
				gotFlag = false;
			}
			
			if (gotFlag) {
				if (!cheese(input)) {
					System.out.println("Hmph. Not good chez :/");
					gotFlag = false;
				}
			}
			
			if (gotFlag) {
				if (!meat(input)) {
					System.out.println("Bah, needs better meat :S");
					gotFlag = false;
				}
			}
			
			if (gotFlag) {
				if (!pizzaSauce(input)) {
					System.out.println("Tsk tsk. You call that pizza sauce? >:|");
					gotFlag = false;
				}
			}
			
			if (gotFlag) {
				if (!veggies(input)) {
					System.out.println("Rotten veggies, ew XP");
					gotFlag = false;
				}
			}
			
			if (gotFlag) {
				System.out.println("Yesyes good burger :D");
			}
		}
	}
}
