package cscg.servlets;

import java.io.*;
import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.fasterxml.jackson.databind.ObjectMapper;

import cscg.user.UserConfig;

@WebServlet("/config")
public class ConfigServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

	public ConfigServlet() {
		super();
    }
    
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
        RequestDispatcher dispatcher = request.getRequestDispatcher("config.jsp");

            request.setAttribute("message", "Invalid request");
            request.setAttribute("type", "danger");
            dispatcher.forward(request, response);
    }

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
        RequestDispatcher dispatcher = request.getRequestDispatcher("config.jsp");

        String jsonConfig = getBody(request);

        if (jsonConfig == null) {
            request.setAttribute("message", "Invalid request");
            request.setAttribute("type", "danger");
            dispatcher.forward(request, response);
            return;
        }

        HttpSession session = request.getSession(true);
        
        ObjectMapper objectMapper = new ObjectMapper();
        UserConfig userConfig = objectMapper.readValue(jsonConfig, UserConfig.class);

        

        if (userConfig == null) {
            request.setAttribute("message", "Failed to parse user configuration");
            request.setAttribute("type", "danger");
        }
        else if (userConfig.getUser() != null) {
            request.setAttribute("type", "danger");
            request.setAttribute("message", "Hacking detected!");
        }
        else {
            request.setAttribute("type", "success");
            request.setAttribute("message", "User configuration updated");
            session.setAttribute("config", userConfig);
        }

        dispatcher.forward(request, response);
    }

    public static String getBody(HttpServletRequest request) throws IOException {

        String body = null;
        StringBuilder stringBuilder = new StringBuilder();
        BufferedReader bufferedReader = null;
    
        try {
            InputStream inputStream = request.getInputStream();
            if (inputStream != null) {
                bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
                char[] charBuffer = new char[128];
                int bytesRead = -1;
                while ((bytesRead = bufferedReader.read(charBuffer)) > 0) {
                    stringBuilder.append(charBuffer, 0, bytesRead);
                }
            } else {
                stringBuilder.append("");
            }
        } catch (IOException ex) {
            return null;
        } finally {
            if (bufferedReader != null) {
                try {
                    bufferedReader.close();
                } catch (IOException ex) {
                    return null;
                }
            }
        }
    
        body = stringBuilder.toString();
        return body;
    }

}
