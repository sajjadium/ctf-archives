package com.sekai.app.controller.contact;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

@Getter
@Setter
@Entity
public class Contact {

    @Id
    @GeneratedValue
    private Long id;

    @NotNull
    @Pattern(regexp = "^[A-Z][a-z]{2,}$")
    private String firstName;

    @NotNull
    @Pattern(regexp = "^[A-Z][a-z]{2,}$")
    private String lastName;

    @NotNull
    @Pattern(regexp = "^[A-Z][a-z]{2,}$")
    private String description;

    @NotNull
    @CheckCountry
    private String country;

}
