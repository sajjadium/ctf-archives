import java.util.Random;

public class SeededRandomizer {

	public static void display(char[] arr) {
		for (char x: arr)
			System.out.print(x);
		System.out.println();
	}

	public static void sample() {
		Random rand = new Random(79808677);
		char[] test = new char[12];
		int[] b = {9, 3, 4, -1, 62, 26, -37, 75, 83, 11, 30, 3};
		for (int i = 0; i < test.length; i++) {
			int n = rand.nextInt(128) + b[i];
			test[i] = (char)n;
		}
		display(test);
	}

	public static void main(String[] args) {
		// sample();
		// Instantiate another seeded randomizer below (seed is integer between 0 and 1000, exclusive):
		char[] flag = new char[33];
		int[] c = {13, 35, 15, -18, 88, 68, -72, -51, 73, -10, 63, 
				1, 35, -47, 6, -18, 10, 20, -31, 100, -48, 33, -12, 
				13, -24, 11, 20, -16, -10, -76, -63, -18, 118};
		for (int i = 0; i < flag.length; i++) {
			int n = (int)(Math.random() * 128) + c[i];
			flag[i] = (char)n;
		}
		display(flag);
	
	}

}
