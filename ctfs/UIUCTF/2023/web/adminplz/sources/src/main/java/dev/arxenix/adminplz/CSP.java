package dev.arxenix.adminplz;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class CSP implements Filter {
    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain) throws ServletException, IOException {
        ((HttpServletResponse) response).addHeader("Content-Security-Policy", "default-src 'none';");
        chain.doFilter(request, response);
    }
}
