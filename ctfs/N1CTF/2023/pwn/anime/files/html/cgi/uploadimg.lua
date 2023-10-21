local fname=cgi.querystr()..".jpg"
if #fname>5 and #fname<32 then
print(cgi.saveto(fname))
end
