# Flag is in the root as /flag (see attached Dockerfile)

require 'sinatra'
require 'securerandom'

set :environment, :production

def err(s)
  erb :index, :locals => {:links => [], :error => s}
end

def ok(l)
  erb :index, :locals => {:links => l, :error => nil}
end

get '/' do
  return ok []
end

post '/' do
  unless params[:tarfile] && (tempfile = params[:tarfile][:tempfile])
    return err "File not sent"
  end
  unless tempfile.size <= 10240
    return err "File too big"
  end 
  
  path = SecureRandom.hex 16
  unless Dir.mkdir "uploads/#{path}", 0755
    return err "Error creating directory"
  end
  unless system "tar -xvf #{tempfile.path} -C uploads/#{path}"
    return err "Error extracting tar file"
  end

  links = Dir.glob("uploads/#{path}/**/*", File::FNM_DOTMATCH).select do |f|
    # Don't show . or ..
    if [".", ".."].include? File.basename f
      false
    # Don't show symlinks. Additionally delete them, they may be unsafe
    elsif File.symlink? f
      File.unlink f
      false
    # Don't show directories (but show files under them)
    elsif File.directory? f
      false
    # Show everything else
    else
      true
    end
  end

  return ok links
end

get '/uploads/*' do
  filepath = "uploads/#{::Rack::Utils.clean_path_info params['splat'].first}"
  halt 404 unless File.file? filepath
  send_file filepath 
end

not_found do
  status 404
  '404'
end

error 500 do
  status 500
  '500'
end
