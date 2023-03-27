package com.linectf.safeNote.controller.rest;

import com.linectf.safeNote.controller.request.NoteCreateRequest;
import com.linectf.safeNote.controller.response.NoteCreateResponse;
import com.linectf.safeNote.controller.response.NoteResponse;
import com.linectf.safeNote.controller.response.Response;
import com.linectf.safeNote.model.User;;
import com.linectf.safeNote.service.NoteService;
import com.linectf.safeNote.utils.VariousUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@RestController
@RequestMapping("/api/note")
@RequiredArgsConstructor
public class NoteRestController {

    private final NoteService noteService;

    @GetMapping
    public Response<List<NoteResponse>> note(Authentication authentication) {
        User user = VariousUtils.cast(authentication.getPrincipal(), User.class);
        return Response.success(
                noteService.mynote(
                        user.getId()
                ).stream().map(NoteResponse::fromNote).collect(Collectors.toList())
        );
    }

    @PostMapping("/create")
    public Response<NoteCreateResponse> create(@RequestBody NoteCreateRequest request, Authentication authentication) {
        return Response.success(
                NoteCreateResponse.fromNote(
                        noteService.create(
                                authentication.getName(),
                                request.getNote()
                        )
                )
        );
    }
}
