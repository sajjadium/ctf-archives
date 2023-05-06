package com.linectf.safeNote.configuration;

import com.linectf.safeNote.configuration.LineAuthenticationEntryPoint;
import com.linectf.safeNote.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    private final UserService userService;

    @Value("${jwt.secret-key}")
    private String secretKey;

    @Override
    protected void configure(
            HttpSecurity http
    ) throws Exception {
        http
            .csrf()
                .disable()
            .authorizeRequests()
            .antMatchers("/api/user/register","/api/user/login").permitAll()
            .antMatchers("/api/user/**", "/api/note/**").authenticated()
            .regexMatchers("/api/admin/.*").authenticated()
            .antMatchers("/api/admin/.*").hasRole("ADMIN")
            .anyRequest().permitAll();

        http
            .sessionManagement()
            .sessionCreationPolicy(
                SessionCreationPolicy.STATELESS
            );

        http
            .exceptionHandling()
            .authenticationEntryPoint(new LineAuthenticationEntryPoint());

        http.addFilterBefore(
            new TokenFilter(
                    userService,
                    secretKey
                ),
            UsernamePasswordAuthenticationFilter.class
        );
    }
}

