from flask import render_template_string

def __openTemplate(template):
    with open('./templates/'+template, "r") as f:
        return f.read()

def render_template(template, **kwargs):
    temp = __openTemplate(template).format(**kwargs)
    return render_template_string(temp, **kwargs)