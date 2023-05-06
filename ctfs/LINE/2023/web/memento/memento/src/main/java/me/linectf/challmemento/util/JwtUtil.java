package me.linectf.challmemento.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;

import java.util.UUID;

public class JwtUtil {
    private static String secret = UUID.randomUUID().toString();
    private static Algorithm algorithm = Algorithm.HMAC256(secret);

    public static String sign(String subject) {
        String jwt = JWT.create().withSubject(subject).sign(algorithm);
        return jwt;
    }

    public static String verify(String token) {
        JWTVerifier jwtVerifier = JWT.require(algorithm).build();
        DecodedJWT jwt = jwtVerifier.verify(token);
        return jwt.getSubject();
    }
}
