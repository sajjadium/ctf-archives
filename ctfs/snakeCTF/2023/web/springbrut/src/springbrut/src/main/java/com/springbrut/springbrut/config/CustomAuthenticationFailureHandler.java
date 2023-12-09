package com.springbrut.springbrut.config;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class CustomAuthenticationFailureHandler
    implements AuthenticationFailureHandler {

  public CustomAuthenticationFailureHandler() { super(); }

  @Override
  public void onAuthenticationFailure(HttpServletRequest request,
                                      HttpServletResponse response,
                                      AuthenticationException exception)
      throws IOException, ServletException {
    log.info("onAuthenticationFailure called");
    response.setStatus(HttpStatus.UNAUTHORIZED.value());
    // Sleep to avoid side channels
    try {
      Thread.sleep(200);
    } catch (Exception e) {
    }
    response.addHeader("Exception", exception.getMessage());
    response.getWriter().print("Login failed");
  }
}
