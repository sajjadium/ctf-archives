require 'net/http'

class Server
    def call(env)
        req = Rack::Request.new(env)

        path = req.path
        
        if path == '/'
            return [200, {"Content-Type" => "text/html"}, [
                "<html><body>" +
                "There are <span id='count'></span> flags for you to capture here. Have fun!" +
                "<script>fetch('/api/flag-count').then(resp => resp.text()).then(data => document.getElementById('count').innerText = data)</script>" +
                "</body></html>"
            ]]

        elsif path == '/admin'
            params = req.params
            flagApi = params.fetch("backend", false) ? params.fetch("backend") : "http://backend/flag-plz"
            target = "https://bit.ly/3jzERNa"

            uri = URI(flagApi)
            req = Net::HTTP::Post.new(uri)
                req['Admin-Key'] = ENV.fetch("ADMIN_KEY")
                req['First-Flag'] = ENV.fetch("FIRST_FLAG")
                req.set_form_data('target' => target)

                res = Net::HTTP.start(uri.hostname, uri.port) {|http|
                http.request(req)
            }

            resp = res.body

            return [200, {"Content-Type" => "text/html"}, [resp]]

        elsif path == '/forbidden'
            return [403, {"Content-Type" => "text/html"}, ["You're not allowed in here."]]

        else
            return [404, {"Content-Type" => "text/html"}, ["Not Found"]]
        end
    end
end