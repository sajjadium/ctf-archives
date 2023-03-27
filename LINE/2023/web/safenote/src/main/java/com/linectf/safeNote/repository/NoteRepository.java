package com.linectf.safeNote.repository;

import com.linectf.safeNote.model.Entity.NoteEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NoteRepository extends JpaRepository<NoteEntity, Integer> {
    List<NoteEntity> findAll();
    List<NoteEntity> findByNote(String note);
    List<NoteEntity> findAllByUserId(Integer id);

}
