package com.springbrut.springbrut.config;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class CustomAuthenticationSuccessHandler
    implements AuthenticationSuccessHandler {

  public CustomAuthenticationSuccessHandler() { super(); }

  @Override
  public void onAuthenticationSuccess(HttpServletRequest request,
                                      HttpServletResponse response,
                                      Authentication auth) {
    log.info("onAuthenticationSuccess called");
    // Sleep to avoid side channels
    try {
      Thread.sleep(2000);
    } catch (Exception e) {
    }
    response.addHeader("Welcome", auth.getName());
    response.addHeader("Location", "/");
    response.setStatus(HttpStatus.FOUND.value());
  }
}
