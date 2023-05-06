package cscg.user;

import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.*;

import javax.servlet.http.HttpServletRequest;

public class UserDAO {
	public User checkLogin(HttpServletRequest request, String username, String password_md5_sha1) {
		User user = null;

		ArrayList<User> users = (ArrayList<User>) request.getServletContext().getAttribute("users");
		if (users == null)
			return null;

		for (User u : users) {
			if (u.getUsername().equals(username)) {
				try {
					// User password in storage is only stored as md5, we should hash it again
					MessageDigest digestStorage;
					digestStorage = MessageDigest.getInstance("SHA-1");
					digestStorage.update(u.getPassword().getBytes("ascii"));

					byte[] passwordBytes = null;
					try {
						passwordBytes = Hex.decodeHex(password_md5_sha1);
					} catch (DecoderException e) {
						return null;
					}

					UserConfig userConfig = (UserConfig) request.getSession().getAttribute("config");

					if (userConfig.isDebugMode()) {
						String pw1 = new String(Hex.encodeHex(digestStorage.digest()));
						String pw2 = password_md5_sha1;

						java.util.logging.Logger.getLogger("login")
								.info(String.format("Login tried with: %s == %s", pw1, pw2));
					}

					if (Arrays.equals(passwordBytes, digestStorage.digest())) {
						if (userConfig.isDebugMode())
							java.util.logging.Logger.getLogger("login").info("Passwords were equal");
						return u;
					}
					if (userConfig.isDebugMode())
						java.util.logging.Logger.getLogger("login").info("Passwords were NOT equal");
				} catch (NoSuchAlgorithmException e) {
					return null;
				} catch (UnsupportedEncodingException e) {
					return null;
				}
			}
		}

		return null;
	}

}
