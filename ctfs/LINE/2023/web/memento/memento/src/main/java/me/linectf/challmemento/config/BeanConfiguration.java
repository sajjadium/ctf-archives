package me.linectf.challmemento.config;

import me.linectf.challmemento.context.AuthContext;
import me.linectf.challmemento.interceptor.AuthInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BeanConfiguration {

    @Bean
    public AuthInterceptor authInterceptor() {
        return new AuthInterceptor();
    }

    @Bean
    public AuthContext authContext() {
        return new AuthContext();
    }
}
