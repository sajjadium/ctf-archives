package com.linectf.safeNote.utils;

import com.linectf.safeNote.exception.LineCtfException;
import com.linectf.safeNote.model.Enum.ErrorCode;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Date;

public class VariousUtils {
    public static <T> T cast(Object o, Class<T> clazz) {
        return clazz != null && clazz.isInstance(o) ? clazz.cast(o) : null;
    }
    public static String decode(String value) throws LineCtfException {
        String result = null;
        try{
            result = URLDecoder.decode(value, StandardCharsets.UTF_8.toString());
        }catch (Exception e){
            throw new LineCtfException(ErrorCode.INVALID_TOKEN);
        }
        return result;
    }

    public static Boolean validate(
            String token,
            String userName,
            String key
    ) {
        String usernameByToken = getUsername(token, key);
        return usernameByToken.equals(userName) && !isTokenExpired(token, key);
    }

    public static Claims extractAllClaims(
            String token,
            String key
    ) {
        return Jwts.parserBuilder()
                .setSigningKey(getSigningKey(key))
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    public static String getUsername(
            String token,
            String key
    ) {
        return extractAllClaims(token, key).get("username", String.class);
    }

    private static Key getSigningKey(
            String secretKey
    ) {
        byte[] keyBytes = secretKey.getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public static Boolean isTokenExpired(
            String token,
            String key
    ) {
        Date expiration = extractAllClaims(token, key).getExpiration();
        return expiration.before(new Date());
    }

    public static String generateAccessToken(
            String username,
            String key,
            long expiredTimeMs
    ) {
        return generateToken(username, expiredTimeMs, key);
    }

    private static String generateToken(
            String username,
            long expireTime,
            String key
    ) {

        Claims claims = Jwts.claims();
        claims.put("username", username);

        return Jwts.builder()
                .setClaims(claims)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + expireTime))
                .signWith(getSigningKey(key), SignatureAlgorithm.HS256)
                .compact();
    }
}
