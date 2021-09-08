package cscg.servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.ArrayList;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import cscg.user.*;

@WebServlet("/register")
public class RegistrationServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;


	public RegistrationServlet() {
		super();
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		String username = request.getParameter("username");
        String password = request.getParameter("password");

        java.util.logging.Logger.getLogger("register").info("Creating user with username: " + username);
       

        HttpSession session = request.getSession(true);
        UserConfig userConfig = (UserConfig)session.getAttribute("config");

		ArrayList<User> users = (ArrayList<User>) request.getServletContext().getAttribute("users");
        
        for (User u : users) {
            if (u.getUsername().equals(username)) {
                RequestDispatcher dispatcher = request.getRequestDispatcher("register.jsp");
                request.setAttribute("message", "Username already exists");
                dispatcher.forward(request, response);
                return;
            }
        }

        User user = new User(users.size(), username, password, false);
        userConfig.setUser(user);
        session.setAttribute("config", userConfig);

        users.add(user);
		
        RequestDispatcher dispatcher = request.getRequestDispatcher("home.jsp");
		dispatcher.forward(request, response);
    }
    
    private static int tryParseInt(String value, int defaultVal) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return defaultVal;
        }
    }

}
