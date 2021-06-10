#! /bin/python
from flask import Flask,render_template,request
import uuid
import os
import lorun
import multiprocessing
app = Flask(__name__)


RESULT_STR = [
    'Accepted',
    'Presentation Error',
    'Time Limit Exceeded',
    'Memory Limit Exceeded',
    'Wrong Answer',
    'Runtime Error',
    'Output Limit Exceeded',
    'Compile Error',
    'System Error'
]

def compile_binary(random_prefix):
    os.system('gcc %s.c -o %s_prog'%(random_prefix,random_prefix))

@app.route("/judge",methods=['POST'])
def judge():
        try:
            random_prefix = uuid.uuid1().hex
            random_src = random_prefix + '.c'
            random_prog = random_prefix + '_prog'
            random_output = random_prefix + '.out'
            if 'code' not in request.form:
                return 'code not exists!'
            #write into file
            with open(random_src,'w') as f:
                f.write(request.form['code'])
    
            #compile
            process = multiprocessing.Process(target=compile_binary,args=(random_prefix,))
            process.start()
            process.join(1)
            if process.is_alive():
                process.terminate()
                return 'compile error!'

            if not os.path.exists(random_prefix+'_prog'):
                os.remove(random_src)
                return 'compile error!'
            
            fin = open('a+b.in','r')
            ftemp = open(random_output, 'w')
            runcfg = {
                'args':['./'+random_prog],
                'fd_in':fin.fileno(),
                'fd_out':ftemp.fileno(),
                'timelimit':1000,
                'memorylimit':200000,
                'trace':True,
                'calls':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 21, 25, 56, 63, 78, 79, 87, 89, 97, 102, 158, 186, 202, 218, 219, 231, 234, 273],
                'files':{
                  "/etc/ld.so.cache":524288,
                  "/lib/x86_64-linux-gnu/libc.so.6":524288,
                  "/lib/x86_64-linux-gnu/libm.so.6":524288,
                  "/usr/lib/x86_64-linux-gnu/libstdc++.so.6":524288,
                  "/lib/x86_64-linux-gnu/libgcc_s.so.1":524288,
                  "/lib/x86_64-linux-gnu/libpthread.so.0":524288,
                  "/etc/localtime":524288
                 }      
            }
            
            rst = lorun.run(runcfg)
            fin.close()
            ftemp.close()
            
            os.remove(random_prog)
            os.remove(random_src)

            if rst['result'] == 0:
                ftemp = open(random_output,'r')
                fout = open('a+b.out','r')
                crst = lorun.check(fout.fileno() , ftemp.fileno())
                fout.seek(0)
                ftemp.seek(0)
                standard_output = fout.read()
                test_output = ftemp.read()
                fout.close()
                ftemp.close()
                if crst != 0:
                    msg = RESULT_STR[crst] +'<br/>'
                    msg += 'standard output:<br/>'
                    msg += standard_output +'<br/>'
                    msg += 'your output:<br/>'
                    msg += test_output
                    os.remove(random_output)
                    return msg
            os.remove(random_output)
            return RESULT_STR[rst['result']]
        except Exception as e:
            if os.path.exists(random_prog):
                os.remove(random_prog)
        
            if os.path.exists(random_src):
                os.remove(random_src)

            return 'ERROR! '+str(e)
        return 'ERROR!'

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=11111)
