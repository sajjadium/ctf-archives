import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.util.Random;
import java.util.Arrays;

class Main {
	public static void main(String[] args) throws IOException {
		// imagine not having an unsigned bytes type 🤡
		char[] flag = Files.readString(new File("flag.png").toPath(), Charset.forName("ISO-8859-1")).toCharArray();
		long[] out = new long[flag.length / 8];
		Random random = new Random();
		for (int i = 0; i < flag.length; i += 8) {
			long x = ((long) flag[i] << 56) +
					((long) flag[i + 1] << 48) +
					((long) flag[i + 2] << 40) +
					((long) flag[i + 3] << 32) +
					((long) flag[i + 4] << 24) +
					((long) flag[i + 5] << 16) +
					((long) flag[i + 6] << 8) +
					((long) flag[i + 7]);
			long r = random.nextLong();
			out[i / 8] = x ^ r;
		}
		Files.write(new File("out.txt").toPath(), Arrays.toString(out).getBytes());
	}
}
