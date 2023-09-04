package com.sekai.app.waf;

import lombok.val;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.nio.file.AccessDeniedException;
import java.util.Optional;

@Configuration
@Order(Integer.MIN_VALUE)
public class FrogWaf implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object obj) throws Exception {
        // Uri
        val query = request.getQueryString();
        if (query != null) {
            val v = getViolationByString(query);
            if (v.isPresent()) {
                throw new AccessDeniedException(String.format("Malicious input found: %s", v));
            }
        }
        return true;
    }

    public static Optional<WafViolation> getViolationByString(String userInput) {
        for (val c : AttackTypes.values()) {
            for (val m : c.getAttackStrings()) {
                if (userInput.contains(m)) {
                    return Optional.of(new WafViolation(c, m));
                }
            }
        }
        return Optional.empty();
    }

}