package com.springbrut.springbrut.domain.repository;

import com.springbrut.springbrut.domain.entity.User;
import java.util.Optional;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends CrudRepository<User, Integer> {
  public Optional<User> findByUsername(String username);
}
