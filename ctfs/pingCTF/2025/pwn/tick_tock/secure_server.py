from flask import Flask, request
import subprocess as sp
app = Flask(__name__)

@app.route('/check', methods=['get'])
def check():
    flag = request.args.get('flag')
    if not flag:
        return "No flag given"
    # if not flag.isalnum() or "{" in flag or "}" in flag:
    for c in flag:
        if not c.isalnum() and c not in "{}_":
            return "Flag should be alphanumeric except for {}_"
    if len(flag) > 60:
        return "Flag too long"
    r = sp.run(f'valgrind --tool=callgrind  --callgrind-out-file=/dev/null ./main {flag}', shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
    stderr = r.stderr.decode()
    stdout = r.stdout.decode()
    ins_num = -1
    for line in stderr.split("\n"):
        if "Collected" in line:
            ins_num = int(line.split(" ")[3])
            break
    
    ret = ""
    if "Incorrect" in stdout:
        ret += "Incorrect flag\n"
    elif "Correct" in stdout:
        ret += "Correct flag!!!\n"
    else:
        ret += "Something went wrong\n"
    print(f"Flag: {flag} Instructions: {ins_num}")
    ret = f"{stdout} <br> Time taken: {ins_num}ms"
    if ins_num == -1:
        return "Something went wrong"
    return ret

        
if __name__ == '__main__':
    app.run(port=5000)