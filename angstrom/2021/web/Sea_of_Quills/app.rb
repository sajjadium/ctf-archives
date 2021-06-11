require 'sinatra'
require 'sqlite3'

set :bind, "0.0.0.0"
set :port, 4567

get '/' do
	db = SQLite3::Database.new "quills.db"
	@row = db.execute( "select * from quills" )
	

	erb :index
end

get '/quills' do
	erb :quills	

end


post '/quills' do
	db = SQLite3::Database.new "quills.db"
	cols = params[:cols]
	lim = params[:limit]
	off = params[:offset]
	
	blacklist = ["-", "/", ";", "'", "\""]
	
	blacklist.each { |word|
		if cols.include? word
			return "beep boop sqli detected!"
		end
	}

	
	if !/^[0-9]+$/.match?(lim) || !/^[0-9]+$/.match?(off)
		return "bad, no quills for you!"
	end

	@row = db.execute("select %s from quills limit %s offset %s" % [cols, lim, off])

	p @row

	erb :specific
end
