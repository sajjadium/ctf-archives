require 'sinatra/base'
require_relative '../helper/scanner_helper'

class ScanController < Sinatra::Base

  configure do
    set :views, "app/views"
    set :public_dir, "public"
  end

  get '/' do
    erb :'index'
  end

  post '/' do
    input_service = escape_shell_input(params[:service])
    hostname, port = input_service.split ':', 2
    begin
      if valid_ip? hostname and valid_port? port
        # Service up?
        s = TCPSocket.new(hostname, port.to_i)
        s.close
        # Assuming valid ip and port, this should be fine
        @scan_result = IO.popen("nmap -p #{port} #{hostname}").read
      else
        @scan_result = "Invalid input detected, aborting scan!"
      end
    rescue Errno::ECONNREFUSED
      @scan_result = "Connection refused on #{hostname}:#{port}"
    rescue => e
      @scan_result = e.message
    end

    erb :'index'
  end

end
