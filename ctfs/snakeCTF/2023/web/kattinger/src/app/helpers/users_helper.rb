module UsersHelper
    require 'digest'

    def cipher(username)
        generator = Digest::SHA256::new
        generator << ENV['SECRET'] + username
        
        return generator.hexdigest()
    end

    def check(username, token)
        generator = Digest::SHA256::new
        generator << ENV['SECRET'] + username

        return generator.hexdigest() == token
    end
end
