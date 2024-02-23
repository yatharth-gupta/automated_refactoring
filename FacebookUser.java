// Social media user base class
abstract class SocialMediaUser {
    protected String id;
    protected String email;
    protected String fullName;
    protected String accessToken;

    public SocialMediaUser(String id, String email, String fullName, String accessToken) {
        this.id = id;
        this.email = email;
        this.fullName = fullName;
        this.accessToken = accessToken;
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

// Facebook user class
public class FacebookUser extends SocialMediaUser {

    public FacebookUser(String id, String email, String fullName, String accessToken) {
        super(id, email, fullName, accessToken);
    }

    // Additional Facebook-specific methods or properties can be added here
}

// Usage example
public class Main {

    public static void main(String[] args) {
        // Create a Facebook user object
        FacebookUser user = new FacebookUser("123456789", "johndoe@example.com", "John Doe", "ABCDEFGHIJK");

        // Access the user's information
        String id = user.getId();
        String email = user.getEmail();
        String fullName = user.getFullName();
        String accessToken = user.getAccessToken();

        // Do something with the user's information...
    }
}
