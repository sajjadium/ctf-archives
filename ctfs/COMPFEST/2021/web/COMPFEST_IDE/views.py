from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .utils import CODE_DIR, BLACKLIST, run_code, get_output, generate_id

@require_http_methods(['GET', 'POST'])
def create_handler(req):
    illegal = False
    if req.method == 'POST':
        code = req.POST.get('code', None)
        if code_checker(code):
            codeid = save_code(code)
            if codeid:
                return redirect(f'/{codeid}')
        else: illegal = True
    return render(req, 'createcode.html', {'illegal': illegal})

@require_http_methods(['GET', 'POST'])
def codeview_handler(req, id):
    illegal = False
    if req.method == 'POST':
        newcode = req.POST.get('code', None)
        if code_checker(newcode):
            update_code(id, newcode)
        else: illegal = True

    code = get_code(id)
    if code == None: return redirect('/')
    stt, out, err = get_output(id)
    return render(req, 'viewcode.html', {'id': id, 'code': code, 'stt':stt, 'out': out, 'err': err, 'illegal': illegal})

def code_checker(code):
    if not code: return False
    for elm in BLACKLIST:
        if elm in code: return False
    return True

def save_code(code):
    if code == None or len(code) <= 0: return None

    ID = generate_id(10)
    f = open(f'{CODE_DIR}/{ID}', 'w+')
    f.write(code)
    f.close()
    run_code(ID)
    return ID

def update_code(id, code):
    try:
        f = open(f'{CODE_DIR}/{id}', "a+")
        f.seek(0)
        if len(f.read()) > 0: f.truncate(0)
        if code: f.write(code)
        f.close()
        run_code(id)
    except Exception as e:
        print(e)

def get_code(id):
    try:
        f = open(f'{CODE_DIR}/{id}')
        code = f.read()
        f.close()
        return code
    except FileNotFoundError:
        return None