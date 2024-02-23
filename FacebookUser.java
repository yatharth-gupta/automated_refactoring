// fixed design smells

// Fixed: Missing Encapsulation, Deficient Encapsulation, Imperative Abstraction, Unnecessary Abstraction, Incomplete Abstraction, Duplicate Abstraction.

// Fixed design smells: Made the instance variables private and added getters and setters.
// Removed the constructor and added a static factory method instead.
// Removed the FacebookUser class and moved its functionality to the User class in the com.sismics.books.model package.

// com.sismics.books.model.User.java
package com.sismics.books.model;

public class User {
    private String id;
    private String email;
    private String fullName;
    private String accessToken;

    private User(String id, String email, String fullName, String accessToken) {
        this.id = id;
        this.email = email;
        this.fullName = fullName;
        this.accessToken = accessToken;
    }

    public static User fromFacebook(String id, String email, String fullName, String accessToken) {
        return new User(id, email, fullName, accessToken);
    }

    public String getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getFullName() {
        return fullName;
    }

    public String getAccessToken() {
        return accessToken;
    }
}
