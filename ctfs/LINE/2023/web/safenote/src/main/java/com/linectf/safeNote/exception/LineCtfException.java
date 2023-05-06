package com.linectf.safeNote.exception;

import com.linectf.safeNote.model.Enum.ErrorCode;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class LineCtfException extends RuntimeException{

    private ErrorCode errorCode;
    private String message;

    public LineCtfException(
            ErrorCode errorCode
    ) {
        this.errorCode = errorCode;
        this.message = null;
    }

    @Override
    public String getMessage() {
        if (message == null) {
            return errorCode.getMessage();
        } else {
            return String.format("%s. %s", errorCode.getMessage(), message);
        }
    }
}
