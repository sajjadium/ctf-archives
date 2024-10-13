-- Author: aimardcr
local env = _G

function run(untrusted_code)
    env['string']['char'] = function() end  
    env['string']['format'] = function() end
    env['string']['gsub'] = function() end
    env['string']['sub'] = function() end
    local res, err = load(untrusted_code, nil, 't', env)
    if not res then 
        print('Error: ' .. err)
        return nil, err 
    end
    return pcall(res)
end

print('Welcome to Landbox! (LUA Sandbox)')
print('Feel free to type your lua code below, type \'-- END\' once you are done ;)')
print('-- BEGIN')

local code = ''
while true
do
    local input = io.read()
    if input == '-- END' then
        break
    end
    code = code .. input .. '\n'
end

-- Check 1
blacklist = {'os.execute', 'execute', 'io.popen', 'popen', 'package.loadlib', 'loadlib'}
for line in code:gmatch("[^\n]+") do
    for i = 1, #blacklist do
        if string.find(line, blacklist[i]) then
            print('No! bad code!')
            return 
        end
    end
end

-- Check 2
sanitized = string.gsub(code, '%W', '')
sanitized = string.gsub(sanitized, '%d', '')
for i = 1, #blacklist do
    if string.find(sanitized, blacklist[i]) then
        print('No! bad code!')
        return
    end

    local parts = {}
    for part in sanitized:gmatch("0x%x?%x") do
        table.insert(parts, part)
    end
    
    local result = ''
    for j = 1, #parts do
        result = result .. string.char(tonumber(parts[j]:sub(3), 16))
    end
    
    if string.find(result, blacklist[i]) then
        print('No! bad code!')
        return
    end
end

-- Check 3
local result = {}
for match in code:gmatch("['\"](.-)['\"]") do
    table.insert(result, match)
end

local sanitized = ''
for i = 1, #result do
    sanitized = sanitized .. result[i]
end

for i = 1, #blacklist do
    if string.find(sanitized, blacklist[i]) then
        print('No! bad code!')
        return
    end

    local parts = {}
    for part in sanitized:gmatch("\\x%x%x") do
        table.insert(parts, part)
    end

    local result = ''
    for j = 1, #parts do
        result = result .. string.char(tonumber(parts[j]:sub(3), 16))
    end

    if string.find(result, blacklist[i]) then
        print('No! bad code!')
        return
    end
end

print()

print('-- OUTPUT BEGIN')
local res, err = run(code)
if not res then
    print('Error: ' .. err)
end
print('-- OUTPUT END')