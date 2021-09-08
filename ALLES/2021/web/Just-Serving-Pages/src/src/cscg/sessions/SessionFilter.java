package cscg.sessions;

import javax.servlet.http.*;

import java.io.IOException;

import javax.servlet.*;

public class SessionFilter implements Filter {
	
	public void init(FilterConfig fConfig) throws ServletException {

	}

	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		HttpServletRequest httpRequest = (HttpServletRequest) request;
		SessionWrapper customRequest =
			new SessionWrapper(httpRequest);

		chain.doFilter(customRequest, response);
    }
    
    public void destroy() {
		//we can close resources here
	}

}