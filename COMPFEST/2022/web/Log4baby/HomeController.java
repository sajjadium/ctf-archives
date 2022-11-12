package id.compfest.ctf.log4baby;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.regex.Pattern;

import javax.servlet.http.HttpServletRequest;

// log4j-core v2.14.1
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@Controller
public class HomeController {
	private static final Logger LOG = LogManager.getLogger(HomeController.class);
	private static final String FLAG = System.getenv("SECRET");
	private static Utils utils = new Utils();
	
	@GetMapping
	public String home(HttpServletRequest request) {
		String browserName = utils.getBrowserName(request);
		if(browserName.equals(FLAG))
			return "win";
		
		if(Pattern.compile("jndi|ldap[s]?").matcher(browserName).find()) {
			LOG.warn("Someone is trying to do naughty things!");
			return "angry";
		} else {
			LOG.info("A visit using: '" + browserName + "'");
		}
		return "index";
	}
}