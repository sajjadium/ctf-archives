require 'json'
require 'securerandom'
require 'sinatra'

FLAG = ENV['FLAG'] || 'nek0pts{FAKE_FLAG}'
ALLOWED_ORIGIN = (ENV['ALLOWED_ORIGIN'] || '').split(',')
ADMIN_KEY = ENV['ADMIN_KEY'] || SecureRandom.uuid

SAMPLE_IDS = '41071402-ea46-414b-899a-aaf4b2fc4b3b,a7a74a78-3a82-4c77-a042-f997398af586,1252b5db-7d35-4563-8e1e-4658a8c90daa'.split(',')
MAX_LIKES = 5000

posts = {}
SAMPLE_IDS.each_with_index do |id, i|
    posts[id] = {
        'id' => id,
        'title' => "test #{i + 1}",
        'content' => 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'like' => Random.rand(1000..10000),
        'permission' => {
            'flag' => false,
            'like' => false
        }
    }
end

set :raise_errors, false
set :show_exceptions, false

before do
    content_type :json

    if !request.env.key?('HTTP_ORIGIN')
        return
    end

    origin = request.env['HTTP_ORIGIN']
    if ALLOWED_ORIGIN.include?(origin)
        requested_headers = (request.env['HTTP_ACCESS_CONTROL_REQUEST_HEADERS'] || '').gsub(/\s/, '').split(',')
        # enumerate requested headers for Access-Control-Allow-Headers
        requested_headers.filter! do |h|
            h.downcase() == 'authorization' || \
            h.downcase().start_with?('x-') # if it starts with X-, then it's safe, I think
        end

        # admin uses Authorization header
        if !requested_headers.include?('authorization')
            requested_headers.push('authorization')
        end

        headers \
            'Access-Control-Allow-Origin' => origin,
            'Access-Control-Allow-Headers' => requested_headers.join(', '),
            'Access-Control-Allow-Methods' => 'GET, POST, OPTIONS' # ToDo: add PUT method after implementing `PUT /api/post/:id` properly
    end
end

post '/api/post' do
    if !params['title']
        return { 'error' => 'no title specified' }.to_json
    end

    if !params['content']
        return { 'error' => 'no content specified' }.to_json
    end

    id = SecureRandom.uuid
    posts[id] = {
        'id' => id,
        'title' => params['title'],
        'content' => params['content'],
        'like' => 0,
        'permission' => {
            'flag' => false,
            'like' => true
        }
    }

    return { 'post' => posts[id] }.to_json
end

get '/api/post/:id' do
    id = params['id']
    if !posts.key?(id)
        return { 'error' => 'no such post' }.to_json
    end

    return { 'post' => posts[id] }.to_json
end

# the post has over 1,000,000,000,000 likes, so we give you the flag
get '/api/post/:id/has_enough_permission_to_get_the_flag' do
    id = params['id']
    if !posts.key?(id)
        return { 'error' => 'no such post' }.to_json
    end

    permission = posts[id]['permission']
    if !permission || !permission['flag']
        return { 'flag' => 'nope' }.to_json
    end

    return { 'flag' => FLAG }.to_json
end

post '/api/post/:id/like' do
    id = params['id']
    if !posts.key?(id)
        return { 'error' => 'no such post' }.to_json
    end

    permission = posts[id]['permission']
    if !permission || !permission['like']
        return { 'error' => 'like is restricted' }.to_json
    end

    token = request.env['HTTP_AUTHORIZATION']
    is_admin = token == ADMIN_KEY

    likes = (params['likes'] || 1).to_i
    if !is_admin && likes != 1
        return { 'error' => 'you can add only one like at one time' }.to_json
    end

    if (posts[id]['like'] + likes) > MAX_LIKES
        return { 'error' => 'too much likes' }.to_json
    end
    posts[id]['like'] += likes

    # get 1,000,000,000,000 likes to capture the flag!
    if posts[id]['like'] >= 1_000_000_000_000
        posts[id]['permission']['flag'] = true
    end
    
    return { 'post' => posts[id] }.to_json
end

put '/api/post/:id' do
    token = request.env['HTTP_AUTHORIZATION']
    is_admin = token == ADMIN_KEY

    id = params['id']
    if !posts.key?(id)
        return { 'error' => 'no such post' }.to_json
    end

    id = params['id']
    if SAMPLE_IDS.include?(id)
        return { 'error' => 'sample post should not be updated' }.to_json
    end

    if !is_admin && params['permission']
        return { 'error' => 'only admin can change the parameter' }.to_json
    end

    if !(params['title'] || params['content'])
        return { 'error' => 'no title and content specified' }.to_json
    end

    posts[id].merge!(params)
    return posts[id].to_json
end

# always returns 200 just for CORS
options '/*' do
    return {}.to_json
end

error do
    return 500, { "error": "something went wrong" }.to_json
end

not_found do
    return 404, { "error": "not found" }.to_json
end
