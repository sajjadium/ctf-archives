package com.linectf.safeNote.service;

import com.linectf.safeNote.model.Enum.ErrorCode;
import com.linectf.safeNote.exception.LineCtfException;
import com.linectf.safeNote.model.Entity.UserEntity;
import com.linectf.safeNote.model.Enum.UserRole;
import com.linectf.safeNote.model.User;
import com.linectf.safeNote.repository.UserRepository;
import com.linectf.safeNote.utils.VariousUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder encoded;

    @Value("${jwt.secret-key}")
    private String secretKey;

    @Value("${jwt.token.expired-time-ms}")
    private Long expiredTimeMs;


    public User loadUserByUsername(String userName) throws UsernameNotFoundException {
        return userRepository.findByUserName(userName).map(User::fromEntity).orElseThrow(
                        () -> new LineCtfException(ErrorCode.USER_NOT_FOUND, String.format("userName is %s", userName))
        );
    }

    public String login(
            String userName,
            String password
    ) {
        User savedUser = loadUserByUsername(userName);
        if (!encoded.matches(password, savedUser.getPassword())) {
            throw new LineCtfException(ErrorCode.INVALID_PASSWORD);
        }
        return VariousUtils.generateAccessToken(userName, secretKey, expiredTimeMs);
    }

    @Transactional
    public User register(
            String userName,
            String password
    ) {

        userRepository.findByUserName(userName).ifPresent(it -> {
            throw new LineCtfException(ErrorCode.DUPLICATED_USERNAME, String.format("userName is %s", userName));
        });

        UserEntity savedUser = userRepository.save(
                UserEntity.of(
                        userName,
                        encoded.encode(password),
                        UserRole.USER
                )
        );
        return User.fromEntity(savedUser);
    }
}
