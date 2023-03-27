package me.linectf.challmemento.interceptor;

import me.linectf.challmemento.context.AuthContext;
import me.linectf.challmemento.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.util.WebUtils;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.UUID;


public class AuthInterceptor implements HandlerInterceptor {

    @Autowired
    private AuthContext authContext;

    private static String COOKIE_NAME = "MEMENTO_TOKEN";

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        Cookie cookie = WebUtils.getCookie(request, COOKIE_NAME);
        if (cookie != null && !cookie.getValue().isEmpty()) {
            try {
                String token = cookie.getValue();
                String userid = JwtUtil.verify(token);
                authContext.userid.set(userid);
                return true;
            } catch (Exception e) {
                // Failed to verify jwt
            }
        }
        String userId = UUID.randomUUID().toString();
        cookie = new Cookie(COOKIE_NAME, JwtUtil.sign(userId));
        cookie.setPath("/");
        response.addCookie(cookie);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        authContext.userid.remove();
    }
}
