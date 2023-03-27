package com.linectf.safeNote.service;

import com.linectf.safeNote.model.Enum.ErrorCode;
import com.linectf.safeNote.exception.LineCtfException;
import com.linectf.safeNote.model.Entity.NoteEntity;
import com.linectf.safeNote.model.Entity.UserEntity;
import com.linectf.safeNote.model.Note;
import com.linectf.safeNote.repository.NoteRepository;
import com.linectf.safeNote.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;
import java.util.stream.Collectors;



@Service
@RequiredArgsConstructor
public class NoteService {
    private final UserRepository userRepository;
    private final NoteRepository noteRepository;

    @Transactional
    public Note create(String userName, String title) {
        UserEntity userEntity = userRepository.findByUserName(userName)
                .orElseThrow(() -> new LineCtfException(ErrorCode.USER_NOT_FOUND, String.format("userName is %s", userName)));
        NoteEntity noteEntity = NoteEntity.of(title, userEntity);
        return Note.fromEntity(noteRepository.save(noteEntity));
    }

    public List<Note> mynote(Integer id) {
        return noteRepository
                .findAllByUserId(id)
                .stream()
                .map(Note::fromEntity)
                .collect(Collectors.toList());
    }
}
