package cscg.user;

public class User {
	private int id;
	private String username;
	private String password;
	private Boolean isAdmin;

	public User() {
		
	}

	public User(int id, String username, String password, boolean isAdmin) {
		this.id = id;
		this.username = username;
		this.password = password;
		this.isAdmin = isAdmin;
	}

	public Boolean getIsAdmin() {
		return isAdmin;
	}

	public void setIsAdmin(Boolean isAdmin) {
		this.isAdmin = isAdmin;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}


	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	
	
}
