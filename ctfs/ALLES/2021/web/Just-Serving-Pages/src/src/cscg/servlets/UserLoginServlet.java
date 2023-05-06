package cscg.servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;
import java.sql.SQLException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import cscg.user.*;

@WebServlet("/login")
public class UserLoginServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;


	public UserLoginServlet() {
		super();
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		String username = request.getParameter("username");
		String password = request.getParameter("password");
		
		UserDAO userDao = new UserDAO();
		
		User user = userDao.checkLogin(request, username, password);
		String destPage = "login.jsp";
		
		HttpSession session = request.getSession(true);
		UserConfig userConfig = (UserConfig)session.getAttribute("config");
		if (user != null) {
			
			userConfig.setUser(user);;
			session.setAttribute("config", userConfig);
			destPage = "home.jsp";
		} else {
			String message = "";
			if (userConfig.getLanguage() == 0) {
				message = "Invalid email/password";
			}
			else {
				message = "Ungültige Email/Passwort";
			}
			request.setAttribute("message", message);
		}
		
		RequestDispatcher dispatcher = request.getRequestDispatcher(destPage);
		dispatcher.forward(request, response);
	}

}
