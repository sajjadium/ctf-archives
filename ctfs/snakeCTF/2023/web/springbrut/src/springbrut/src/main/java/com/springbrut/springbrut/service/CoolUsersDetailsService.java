package com.springbrut.springbrut.service;

import com.springbrut.springbrut.domain.entity.User;
import com.springbrut.springbrut.domain.repository.UserRepository;
import com.springbrut.springbrut.session.MyUserPrincipal;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class CoolUsersDetailsService implements UserDetailsService {
  @Autowired private UserRepository userRepository;

  public void saveUser(User u) { userRepository.save(u); }

  public Optional<User> getUser(String username) {
    return userRepository.findByUsername(username);
  }

  public List<User> listUsers() { return (List<User>)userRepository.findAll(); }

  @Override
  public UserDetails loadUserByUsername(String username) {
    Optional<User> user = userRepository.findByUsername(username);
    if (!user.isPresent()) {
      throw new UsernameNotFoundException(username);
    }
    return new MyUserPrincipal(user.get());
  }
}
