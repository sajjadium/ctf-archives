package com.linectf.safeNote.configuration;

import com.linectf.safeNote.controller.response.Response;
import com.linectf.safeNote.exception.LineCtfException;
import com.linectf.safeNote.model.Enum.ErrorCode;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class ControllerAdvice {

    @ExceptionHandler(LineCtfException.class)
    public ResponseEntity<?> errorHandler(
        LineCtfException e
    ) {
        log.error("Error occurs {}", e.toString());
        return ResponseEntity.status(e.getErrorCode().getStatus())
                .body(Response.error(e.getErrorCode().name()));
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<?> databaseErrorHandler(
            IllegalArgumentException e
    ) {
        log.error("Error occurs {}", e.toString());
        return ResponseEntity.status(ErrorCode.DATABASE_ERROR.getStatus())
                .body(Response.error(ErrorCode.DATABASE_ERROR.name()));
    }

}