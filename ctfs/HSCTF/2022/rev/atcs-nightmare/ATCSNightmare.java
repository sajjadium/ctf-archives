import java.util.*;

public class ATCSNightmare {

	public static String stackAttack(String in) {
		Stack<Character> s = new Stack<>();
		for (char c: in.toCharArray())
			s.push(c);
		String res = "";
		int i = 0;
		while (!s.isEmpty()) {
			res += (char)(s.pop() - i);
			i = (i + 1) % 4;
		}
		return res;
	}

	public static String recurses(String in, String out, int i) {
		if (in.isEmpty())
			return out;
		String res = out;
		if (i == 0)
			res += in.charAt(i);
		else
			res = in.charAt(i) + res;
		if (i == 0)
			return recurses(in.substring(1), res, 1);
		return recurses(in.charAt(0) + in.substring(2), res, 0);
	}

	public static String linkDemLists(String in) {
		LinkedList<Character> lin = new LinkedList<>();
		for (char x: in.toCharArray())
			lin.add(x);
		String res = "";
		ListIterator<Character> iter = lin.listIterator(in.length()/2);
		while (iter.hasNext())
			res += iter.next();
		iter = lin.listIterator(in.length()/2);
		while (iter.hasPrevious())
			res += iter.previous();
		return res;
	}

	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		System.out.print("Enter the flag: ");
		String f = in.next();
		if (f.length() == 34 && f.substring(0, 4).equals("flag") && f.charAt(33) == '}') {
			f = f.substring(5, 33);
			if (linkDemLists(recurses(stackAttack(f), "", 1)).equals("20_a1qti0]n/5f642kb\\2`qq4\\0q"))
				System.out.println("Congrats! That is your flag!");
			else
				System.out.println("Sorry, that is incorrect.");
		} else
			System.out.println("Sorry, that is incorrect.");
		in.close();
	}
}
