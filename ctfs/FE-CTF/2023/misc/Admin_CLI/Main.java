import java.util.Base64;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Scanner;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.core.config.Configurator;


public class Main {

	/* flag{....} */
	private static String API_KEY = Base64.getUrlEncoder().encodeToString(System.getenv("FLAG").getBytes());
	
	/* Doesn't seem to be authorized, I don't know why... */
	/* https://backend.fe-ctf.local/removePoints?teamId=0&amount=1000&key=api_key */
	private static int HASH_CODE = -615519892;

	/* Should be safe, right? */
	private static Logger logger = LogManager.getLogger(Main.class);
	
	public static void main(String[] args) {
		Configurator.setLevel(Main.class.getName(), Level.INFO);
		Scanner s = new Scanner(System.in);
		System.out.print("Enter URL: ");
		String input = s.nextLine();
		s.close();
		try {
			URL url = new URL(input.replaceAll("API_KEY", API_KEY));
			if (url.hashCode() == HASH_CODE && url.getHost().equals("backend.fe-ctf.local")) {
				logger.info("URLs Matched, sending request to {}", url);
				/* TODO: Figure out how to send request
				HttpURLConnection con = (HttpURLConnection) url.openConnection();
				con.setRequestMethod("GET")
				*/
			} else {
				logger.warn("URLs are not equal!");
			}
		} catch (MalformedURLException e) {
			logger.error("Invalid URL");
			System.exit(1);
		}
	}
}

