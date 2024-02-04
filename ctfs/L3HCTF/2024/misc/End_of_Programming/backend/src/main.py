from flask import Flask,request,render_template
import hashlib
from client.Python.client import JudgeServerClient, JudgeServerClientError,cpp_lang_config
import os
import requests
import re

flag = os.environ.get('FLAG')
client = JudgeServerClient(server_base_url='http://judge_server:8080',token='2q3r4t5y6u7i8o9p0sacuhu32')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_URL = os.environ.get('OPENAI_API_URL')
ENGINE_NAME = os.environ.get('ENGINE_NAME')

RESULT_SUCCESS = 0
RESULT_WRONG_ANSWER = -1
RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
RESULT_MEMORY_LIMIT_EXCEEDED = 3
RESULT_RUNTIME_ERROR = 4
RESULT_SYSTEM_ERROR = 5

result_str_map = {
    RESULT_SUCCESS: 'Accepted',
    RESULT_WRONG_ANSWER: 'Wrong Answer',
    RESULT_CPU_TIME_LIMIT_EXCEEDED: 'CPU Time Limit Exceeded',
    RESULT_REAL_TIME_LIMIT_EXCEEDED: 'Real Time Limit Exceeded',
    RESULT_MEMORY_LIMIT_EXCEEDED: 'Memory Limit Exceeded',
    RESULT_RUNTIME_ERROR: 'Runtime Error',
    RESULT_SYSTEM_ERROR: 'System Error'
}

cpp_source = '''
#include <iostream>
using namespace std;
int main(){
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
}
'''
app = Flask(__name__)

# ChatGPT
def get_output(text):
    prompt = f"{text}"
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": ENGINE_NAME, "messages": [{"role":"user","content":prompt}], "max_tokens": 400, "temperature": 0}
    )
    try:
        print(response.json())
        cpp_code = response.json().get('choices')[0].get('message').get('content').strip()
    except:
        print(response.text)
        return None
    if cpp_code:
        return cpp_code
    return None
    
# check whether prompt containts code
def is_code_present(text):
    # 向 GPT-3.5 发送请求，询问是否包含代码或伪代码
    prompt = f"Is there any code or pseudocode in the following text? Answer with 'yes' or 'no' only.\n\n{text}"
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": ENGINE_NAME, "messages": [{"role":"user","content":prompt}], "max_tokens": 3, "temperature": 0}
    )
    try:
        reply = response.json().get('choices')[0].get('message').get('content').strip().lower()
    except Exception as e:
        print(response.text)
        raise e
    return reply == "yes"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/problem', methods=['GET'])
def problem():
    return open('templates/problem_cn.html').read()

@app.route('/problem_en', methods=['GET'])
def problem_en():
    return open('templates/problem_en.html').read()

@app.route('/submit', methods=['POST'])
def submit():
    prompt = str(request.form.get('prompt'))
    prompt = prompt[:2048]
    try:
        if is_code_present(prompt):
            return 'Invalid input: code detected.'
    except Exception as e:
        print(e.__repr__())
        return 'API Error'
    output = get_output(prompt)
    if output == None:
        return 'Code extraction or evaluation failed.'
    response = ''
    response += '-------------------------\n'
    response += 'ChatGPT Output:\n{chatgpt_output}\n'.format(chatgpt_output=output)
    response += '-------------------------\n'

    out_code = re.findall(r'```cpp([\s\S]+)```', output)
    if len(out_code) == 0:
        response += 'No code found in the output'
        return response
    out_code = out_code[0]
    print(out_code)
    judge_ret = client.judge(out_code,cpp_lang_config, max_cpu_time=1000, max_memory=1024 * 1024 * 128,test_case_id='pal',output=False)
    if judge_ret['err'] != None:
        response += 'Error: ' + judge_ret['err']
        print(judge_ret)
        return response
    
    is_good_job = all([i['result'] == RESULT_SUCCESS for i in judge_ret['data']])

    for i in judge_ret['data']:
        response += 'Test Case:{test_case}\t{result}\n'.format(test_case=i['test_case'],result=result_str_map[i['result']])
    if is_good_job:
        response += 'Flag is {flag}'.format(flag=flag)
    return response
