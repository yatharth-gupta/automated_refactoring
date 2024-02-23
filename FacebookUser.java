// FacebookUser.java
public class FacebookUser {

    private String id;
    private String email;
    private String fullName;
    private String accessToken;

    public FacebookUser(String id, String email, String fullName, String accessToken) {
        this.id = id;
        this.email = email;
        this.fullName = fullName;
        this.accessToken = accessToken;
    }

    // Getters and setters with proper access control
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getAccessToken() {
        return accessToken;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }
}

// FacebookUserService.java
public class FacebookUserService {

    public FacebookUser createUser(String id, String email, String fullName, String accessToken) {
        // Validation logic can be added here

        FacebookUser user = new FacebookUser(id, email, fullName, accessToken);

        // Save the user to the database or perform other necessary actions

        return user;
    }

    public FacebookUser getUserById(String id) {
        // Retrieve the user from the database or other data source

        return null; // Replace with actual implementation
    }

    // Other methods for managing Facebook users
}
