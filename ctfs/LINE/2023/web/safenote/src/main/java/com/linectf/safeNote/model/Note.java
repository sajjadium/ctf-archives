package com.linectf.safeNote.model;

import com.linectf.safeNote.model.Entity.NoteEntity;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.sql.Timestamp;

@Getter
@AllArgsConstructor
public class Note {
    private Integer id;

    private String note;

    private String username;

    private Timestamp createdAt;

    public static Note fromEntity(NoteEntity entity) {
        return new Note(
                entity.getId(),
                entity.getNote(),
                User.fromEntity(entity.getUser()).getUsername(),
                entity.getCreatedAt()
        );
    }
}
