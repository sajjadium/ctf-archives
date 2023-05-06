package cscg.sessions;

import javax.servlet.http.*;

import org.apache.catalina.connector.Request;

import cscg.user.UserConfig;

public class SessionWrapper extends HttpServletRequestWrapper {
    private HttpServletRequest request;

	public SessionWrapper(HttpServletRequest original) {
		super(original);
	}

	public HttpSession getSession() {
		return getSession(true);
	}

	public HttpSession getSession(boolean createNew) {
        HttpSession session = super.getSession(false);
        if (session == null) {
            session = super.getSession(true);
            session.setAttribute("config", new UserConfig());
        }
       
        return session;
	}
}