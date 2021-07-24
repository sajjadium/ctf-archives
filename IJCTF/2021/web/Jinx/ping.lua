
local hex_to_char = function(x)
  return string.char(tonumber(x, 16))
end

local unescape = function(url)
  return url:gsub("%%(%x%x)", hex_to_char)
end

local ping = function(ip)
  local cmd = "ping -c1 "..ip
  local p = io.popen(cmd, 'r')
  local s = assert(p:read('*a'))
  p:close()
  return s
end

local ip =  unescape(ngx.var.arg_ip)

ngx.say(ping(ip))
