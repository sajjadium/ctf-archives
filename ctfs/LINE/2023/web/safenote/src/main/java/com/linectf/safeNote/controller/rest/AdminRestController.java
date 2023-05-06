package com.linectf.safeNote.controller.rest;

import com.linectf.safeNote.controller.response.FeatureResponse;
import com.linectf.safeNote.controller.response.Response;
import com.linectf.safeNote.exception.LineCtfException;
import com.linectf.safeNote.model.Entity.NoteEntity;
import com.linectf.safeNote.model.Enum.ErrorCode;
import com.linectf.safeNote.model.Note;
import com.linectf.safeNote.model.User;
import com.linectf.safeNote.repository.NoteRepository;
import com.linectf.safeNote.repository.UserRepository;
import com.linectf.safeNote.utils.VariousUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.http.MediaType;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Slf4j
@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminRestController {

    private final NoteRepository noteRepository;
    private final SpelExpressionParser spelExpressionParser;
    private static final String ADMIN_ROLE = "admin";
    private static final String USER_ROLE = "user";


    @GetMapping("/note/list")
    public List<NoteEntity> getNotes(Authentication authentication) {
        User user = VariousUtils.cast(authentication.getPrincipal(), User.class);
        if(!Objects.equals(user.getUsername(), ADMIN_ROLE)){
            throw new LineCtfException(
                    ErrorCode.INVALID_PERMISSION,
                    String.format("You are Not Admin : %s", authentication.getName())
            );
        }

        return noteRepository.findAll();
    }

    @GetMapping("/note/{note}")
    public List<Note> getNote(@PathVariable String note, Authentication authentication){
        User user = VariousUtils.cast(authentication.getPrincipal(), User.class);
        if(!Objects.equals(user.getUsername(), ADMIN_ROLE)){
            throw new LineCtfException(
                    ErrorCode.INVALID_PERMISSION,
                    String.format("You are Not Admin : %s", authentication.getName())
            );
        }
        return noteRepository
                .findByNote(VariousUtils.decode(note))
                .stream()
                .map(Note::fromEntity)
                .collect(Collectors.toList());
    }
    
    @GetMapping("/key/{id}")
    public String getKey(
            @Value("${jwt.secret-key}") String secretKey
    ) {
        if(SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getAuthorities()
                .stream()
                .anyMatch(x -> x.getAuthority()
                        .equals("USER"))
        ){
            return "There's nothing for you.";
        }
        return secretKey;
    }

    @PostMapping(value="/feature", produces = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public Response<FeatureResponse> emulateFeature(@RequestBody String featureRequest, Authentication authentication) {

        User user = VariousUtils.cast(authentication.getPrincipal(), User.class);
        if(!Objects.equals(user.getUsername(), ADMIN_ROLE)){
            throw new LineCtfException(
                    ErrorCode.INVALID_PERMISSION,
                    String.format("You are Not Admin : %s", authentication.getName())
            );
        }
        return Response.success(
                new FeatureResponse(
                        spelExpressionParser.parseExpression(
                                VariousUtils.decode(featureRequest).split("=")[1]
                        ).getValue(String.class)
                )
        );
    }
}
