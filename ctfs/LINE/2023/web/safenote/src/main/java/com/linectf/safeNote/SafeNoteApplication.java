package com.linectf.safeNote;

import com.linectf.safeNote.model.Entity.UserEntity;
import com.linectf.safeNote.model.Enum.UserRole;
import com.linectf.safeNote.repository.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.security.SecureRandom;

@SpringBootApplication(scanBasePackages = "com.linectf")
public class SafeNoteApplication {

    public static void main(String[] args) {
        SpringApplication.run(SafeNoteApplication.class, args);
    }

    public static String genreateRandomString(int len) {
        String randomString = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_-!@#$%^&*()";
        SecureRandom rnd = new SecureRandom();
        StringBuilder sb = new StringBuilder(len);
        for (int i = 0; i < len; i++) {
            sb.append(randomString.charAt(rnd.nextInt(randomString.length())));
        }
        return sb.toString();
    }

    @Bean
    CommandLineRunner init(UserRepository userRepository, BCryptPasswordEncoder encode) {
        return args -> {
            userRepository.findByUserName("admin").ifPresentOrElse(
                    it -> {
                    }, () -> userRepository.save(UserEntity.of("admin",  encode.encode(genreateRandomString(48)), UserRole.ADMIN))
            );
        };
    }
}
