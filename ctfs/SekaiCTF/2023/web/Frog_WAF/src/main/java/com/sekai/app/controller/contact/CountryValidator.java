package com.sekai.app.controller.contact;

import com.sekai.app.waf.FrogWaf;
import lombok.SneakyThrows;
import lombok.val;
import org.springframework.core.io.ClassPathResource;
import org.springframework.util.StreamUtils;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.nio.charset.Charset;
import java.nio.file.AccessDeniedException;
import java.util.Arrays;

public class CountryValidator implements ConstraintValidator<CheckCountry, String> {

    @SneakyThrows
    @Override
    public boolean isValid(final String input, final ConstraintValidatorContext constraintContext) {
        if (input == null) {
            return true;
        }

        val v = FrogWaf.getViolationByString(input);
        if (v.isPresent()) {
            val msg = String.format("Malicious input found: %s", v);
            throw new AccessDeniedException(msg);
        }

        val countries = StreamUtils.copyToString(new ClassPathResource("countries").getInputStream(), Charset.defaultCharset()).split("\n");
        val isValid = Arrays.asList(countries).contains(input);

        if (!isValid) {
            val message = String.format("%s is not a valid country", input);
            constraintContext.disableDefaultConstraintViolation();
            constraintContext.buildConstraintViolationWithTemplate(message)
                    .addConstraintViolation();
        }
        return isValid;
    }
}