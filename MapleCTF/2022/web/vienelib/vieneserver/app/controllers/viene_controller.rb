class VieneController < ApplicationController
    protect_from_forgery with: :null_session
    def index
        if request.local?
            if request.put?
                request_body = request.body.read
                if ['?', '{', '}', '~', '[', ']', ';'].include?(request_body)
                    render json: {"ERROR": "BAD HACKER"}
                end
                viene = open(request_body)
                render json: {"chosen_viene": viene}
                
            elsif request.post?
                if not ['1.txt', '2.txt', '3.txt'].include?(request.body.read)
                    render json: {"chosen_viene": "Error", "chosen_viene_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
                else 
                    fullname = File.join("app","assets", "#{rand(1..3)}.txt")
                    viene = File.read(fullname)
                    #memes
                    viene_poem = viene.split('>')[1].strip
                    viene_url = viene.split('>')[0].strip
                    render json: {"chosen_viene": viene_poem, "chosen_viene_link": viene_url}
                end
            else
                render json: {"ERROR": "I didn't understand the request..."}
            end
        else 
            render json: {"ERROR": "Ur not local..."}
        end
    end
end