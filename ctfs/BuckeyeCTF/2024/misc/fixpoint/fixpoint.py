import base64

standard_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# alphabet = standard_alphabet
# fixed_point = "Vm0wd2QyUXlVWGxWV0d4V1YwZDRWMVl3WkRSV01WbDNXa1JTVjAxV2JETlhhMUpUVmpBeFYySkVUbGhoTVVwVVZtcEJlRll5U2tWVWJHaG9UVlZ3VlZadGNFSmxSbGw1VTJ0V1ZXSkhhRzlVVmxaM1ZsWmFkR05GU214U2JHdzFWVEowVjFaWFNraGhSemxWVm14YU0xWnNXbUZrUjA1R1UyMTRVMkpIZHpGV1ZFb3dWakZhV0ZOcmFHaFNlbXhXVm0xNFlVMHhXbk5YYlVaclVqQTFSMVV5TVRSVk1rcElaSHBHVjFaRmIzZFdha1poVjBaT2NtRkhhRk5sYlhoWFZtMHhORmxWTUhoWGJrNVlZbFZhY2xWcVFURlNNVlY1VFZSU1ZrMXJjRWxhU0hCSFZqRmFSbUl6WkZkaGExcG9WakJhVDJOdFJraGhSazVzWWxob1dGWnRNSGhPUm14V1RVaG9XR0pyTlZsWmJGWmhZMnhXY1ZGVVJsTk5WbFkxVkZaU1UxWnJNWEpqUld4aFUwaENTRlpxUm1GU2JVbDZXa1prYUdFeGNHOVdha0poVkRKT2RGSnJhR2hTYXpWeldXeG9iMWRHV25STlNHaFBVbTE0VjFSVmFHOVhSMHB5VGxac1dtSkdXbWhaTW5oWFkxWkdWVkpzVGs1V2JGa3hWa1phVTFVeFduSk5XRXBxVWxkNGFGVXdhRU5UUmxweFVtMUdVMkpWYkRaWGExcHJZVWRGZUdOSE9WZGhhMHBvVmtSS1QyUkdTbkpoUjJoVFlYcFdlbGRYZUc5aU1XUkhWMjVTVGxOSGFGQlZiVEUwVmpGU1ZtRkhPVmhTTUhCNVZHeGFjMWR0U2tkWGJXaGFUVzVvV0ZreFdrZFdWa3B6VkdzMVYySkdhM2hXYTFwaFZURlZlRmR1U2s1WFJYQnhWV3hrTkdGR1ZYZGhSVTVVVW14d2VGVnRNVWRWTWtwV1lrUmFXR0V4Y0hKWlZX"

alphabet = "bctf{?????????????????????????FiXed???????????????????????p01nT}"
fixed_point = "NslSBwm6YNHHNreCNsmojw8zY9nGVzep9NoJ5LHpH3b8NKnQlB2Ca{XzIxeUyR85Y{COjRD09P4mFEAAFACZlAo0jwnGBrj7UAbwYBHDjBDEjBlMY{DWkE46YrVtaKh6ABDdVLoty{5Gjr5DMrmSNAo05DVu5NjR93m9VEDqMfHcjr5rAr2WVPo0lBVGaxA{N3mvBw8cYzbL5DHLlB8GBxrzYNo95B52N9HCIR4Ol3mcaxm3AocWkE2tArVeF{D0NxlvVrm6UElHFKmklB5CNE2tU{VtFPmp9B8WUNAtlNmUUBefyACwNR7zY9leFEwzj9nxARvDks5caoHo5sv{k{8ZYPH9aKwRABASy{HqY9vSjxAfNrBOVDA0As5EBEL7UBCZALAUj35SNKLAABmoHsocj6VUBxVp9NoSHBHDV64GU98ZjAmR5Evzl9leYweWl3lRFRv0UD4HB{X8IBv6BrDtjAl8Fwe29NoRBR4Zj9HUarmgAr5ck{DzlBAt5B76ABmf9rDkjAAGkzANNrvkjBDtY9nCaRnxMxH9ABmZAsb8NKnNy{mC5DIRl{VAUNeMMrDvBxADVs4SU92o93VoAR7zYDmEBsI7ABjwy{m09femjsIRjsm{VE4cYfeEVRBOUB8WBrmylD4GUBeAI3mvHwDOl9luFw5pY{mcVfAtlzHcjKLKU3m{MR4cjBVuFrDUNsmRMR4t5P5HU98fIAmJF{LZyfocjKLMj3ldU{8qYr88FRLflB5mBK20ArDANKAlN3m{VrmZjB59az5NANrOYzrzAKncBxVp9B5v5BmzyNVcjK46F3vvkfoKH9LGawoyMslvFLHDlElHHKADAomtNLAtUDVtaKL8Y{jw5LAtHBDmkRLRyPV{NR78YPAEVzA793vvILHKj35SFrexMrvkyLBzY3vlBx5xMrm9VBHO5DAUaRLyNACwVfAjlBeAUNeKyBDvyrH0ND48HKnxMrvkN9hzYE5AFze293CZU{Hy"

translation_table = str.maketrans(standard_alphabet, alphabet)
def encode(s):
    """Base64 encode the string using our custom alphabet"""
    return base64.b64encode(s.encode()).decode().replace('=', '').translate(translation_table)


starting_string = input("String to encode? ")
current = starting_string

print(f"{0} {starting_string}")
for i in range(100):
    old = current
    current = encode(current)
    print(f"{i+1} {current[0:1000] + (current[1000:] and '...')}")

    if current[0:1000] == old[0:1000]:
        if current.startswith(fixed_point):
            print("Found the fixed point, and it is what I expected!")
        else:
            print("Found a fixed point, but it's not what I expected!!!")
        break
else:
    print("Failed to find a fixed point")
    
