package dev.arxenix.adminplz;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@SpringBootApplication
@RestController
public class AdminApplication {
    private static final Logger logger
            = LoggerFactory.getLogger(AdminApplication.class);
    private static String ADMIN_PASSWORD;
    private static ApplicationContext app;

    public static void main(String[] args) {
        app = SpringApplication.run(AdminApplication.class, args);
        ADMIN_PASSWORD = System.getenv("ADMIN_PASSWORD");
    }

    @PostMapping(path = "/login", consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE})
    public String login(HttpSession session, User user) {
        if (user.getUsername().equals("admin") && !user.getPassword().equals(ADMIN_PASSWORD)) {
            return "not allowed";
        }
        session.setAttribute("user", user);
        return "logged in";
    }

    public boolean isAdmin(HttpServletRequest req, HttpSession session) {
        return req.getRemoteAddr().equals("127.0.0.1") || (
                isLoggedIn(session) && ((User) session.getAttribute("user")).getUsername().equals("admin")
        );
    }

    public boolean isLoggedIn(HttpSession session) {
        return session.getAttribute("user") != null;
    }

    long lastBotRun = 0;

    @PostMapping(path = "/report", consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE})
    public String report(String url) throws IOException {
        if (url == null || !(url.startsWith("http://") || url.startsWith("https://")))
            return "invalid url";

        long time = System.currentTimeMillis();
        if (time - lastBotRun < 300000) {
            return "too soon! (please wait 5min)";
        }
        lastBotRun = time;

        Runtime.getRuntime().exec(new String[]{"node", "bot.js", url});
        return "an admin will check your url!";
    }

    @GetMapping("/")
    public Resource index(HttpServletRequest req) {
        return app.getResource("index.html");
    }

    @GetMapping("/admin")
    public Resource admin(HttpServletRequest req, HttpSession session, @RequestParam String view) {
        if (isLoggedIn(session) && view.contains("flag")) {
            logger.warn("user {} [{}] attempted to access restricted view", ((User) session.getAttribute("user")).getUsername(), session.getId());
        }
        return app.getResource(isAdmin(req, session) ? view : "error.html");
    }
}
