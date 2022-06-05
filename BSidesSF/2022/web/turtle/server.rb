require 'sinatra'
require 'encrypted_cookie'
require 'tempfile'
require 'pp'
require 'fileutils'
require 'digest'
require 'json'
require 'set'

configure do
  set :bind, ENV['HOST'] || '0.0.0.0'
  set :port, ENV['PORT'] || '7999'
  set :public_folder, 'public'

  #enable :sessions
  use Rack::Session::EncryptedCookie, :secret => '07299e9170349e93da5c1106e92265b2'
end

SECRET = File.read('secret.txt').force_encoding('ASCII-8BIT')
DATE_FORMAT = '%m/%d/%y'
NEEDED_SOLVES = 30 # ~1 month

def get_path(date)
  seed = Digest::MD5.new()
    .update(SECRET)
    .update(date.strftime(DATE_FORMAT))
    .digest

  result = seed.unpack('v*').map do |v|
    {
      'angle'    => (v & 0b111111111) % 360,
      'distance' => v >> 9,
    }
  end

  return result
end

get "/" do
  send_file File.join(settings.public_folder, 'index.html')
end

post "/submit" do
  content_type 'application/json'

  begin
    # Make sure this exists
    session[:completed] = session[:completed] || Set::new()

    body = JSON.parse(request.body.read)
    date = Date.iso8601(body['date'])

    if date < Date.today
      raise "Date cannot be in the past!"
    end

    path = body['path']
    if path.length != 8
        return 400, 'body.path must be an array of 8 elements'
    end

    expected = get_path(date)

    wrongness = 0
    results = expected.each_with_index.map do |e, i|
      angle_off    = (e['angle'] - path[i]['angle']).abs
      distance_off = (e['distance'] - path[i]['distance']).abs

      wrongness = wrongness + angle_off + distance_off

      {
        'angle_off' => angle_off,
        'distance_off' => distance_off
      }
    end

    out = {
      'success' => true,
      'wrongness' => wrongness,
      'results' => results
    }

    if wrongness == 0
      session[:completed].add(date.to_s)
    end

    out[:completed] = session[:completed].length()
    if session[:completed].length() > NEEDED_SOLVES
      out[:flag] = File.read('flag.txt')
    end

    return {
      'success' => true,
      'wrongness' => wrongness,
      'results' => out
    }.to_json
  rescue StandardError => e
    $stderr.puts(e)
    $stderr.puts(e.backtrace.join("\n"))
    return {
      success: false,
      error: e.to_s(),
    }.to_json
  end
end

get "/past/:daysago" do
  content_type 'application/json'

  date = Date.today - params[:daysago].to_i.abs
  return get_path(date).to_json()
end
