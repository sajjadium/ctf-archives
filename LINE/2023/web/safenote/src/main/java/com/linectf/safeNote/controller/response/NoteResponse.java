package com.linectf.safeNote.controller.response;

import com.linectf.safeNote.model.Note;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.sql.Timestamp;

@Getter
@AllArgsConstructor
public class NoteResponse {

    private Integer id;
    private String note;
    private String username;
    private Timestamp createdAt;

    public static NoteResponse fromNote(Note note) {
        return new NoteResponse(
                note.getId(),
                note.getNote(),
                note.getUsername(),
                note.getCreatedAt()
        );
    }
}
