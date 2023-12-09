package com.springbrut.springbrut.session;

import com.springbrut.springbrut.domain.entity.User;
import java.util.ArrayList;
import java.util.Collection;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

public class MyUserPrincipal implements UserDetails {
  private User loggedUser;

  public MyUserPrincipal(User u) { this.loggedUser = u; }

  public String getUsername() { return loggedUser.getUsername(); }

  public String getPassword() { return loggedUser.getPassword(); }

  @Override
  public Collection<? extends GrantedAuthority> getAuthorities() {
    ArrayList<SimpleGrantedAuthority> res = new ArrayList<>();
    res.add(new SimpleGrantedAuthority("USER"));
    return res;
  }

  @Override
  public boolean isAccountNonExpired() {
    return true;
  }

  @Override
  public boolean isAccountNonLocked() {
    return true;
  }

  @Override
  public boolean isCredentialsNonExpired() {
    return true;
  }

  @Override
  public boolean isEnabled() {
    return true;
  }
}
