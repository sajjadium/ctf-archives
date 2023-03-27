package com.linectf.safeNote.controller.response;

import com.linectf.safeNote.model.Note;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class NoteCreateResponse {

    private String note;
    private String username;

    public static NoteCreateResponse fromNote(Note note) {
        return new NoteCreateResponse(
                note.getNote(),
                note.getUsername()
        );
    }
}
