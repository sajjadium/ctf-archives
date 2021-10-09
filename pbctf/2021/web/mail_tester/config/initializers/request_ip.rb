module Rack
    class Request
      module Helpers
        def real_ip  
          forwarded_for&.[](-2) || ip
        end
      end
    end
  end
