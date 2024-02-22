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

    public void createUser(FacebookUser user) {
        // Code to create a Facebook user in the database
    }

    public FacebookUser getUserById(String id) {
        // Code to get a Facebook user from the database by their ID
        return null;
    }

    public void updateUser(FacebookUser user) {
        // Code to update a Facebook user in the database
    }

    public void deleteUser(String id) {
        // Code to delete a Facebook user from the database
    }
}
