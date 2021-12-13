from flask import Flask, render_template_string, request

app = Flask(__name__)
blacklist = [ 
    'request',
    'config',
    'self',
    'class',
    'flag',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '"',
    '\'',
    '.',
    '\\',
    '`',
    '%',
    '#',
    ]

error_page = '''
        {% extends "layout.html" %}
        {% block body %}
        <center>
           <section class="section">
              <div class="container">
                 <h1 class="title">Error :(</h1>
                 <p>Your request was blocked. Please try again!</p>
              </div>
           </section>
        </center>
        {% endblock %}
        '''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form['q']:
            return render_template_string(error_page)

        if len(request.form) > 1:
            return render_template_string(error_page)

        query = request.form['q'].lower()
        if '{' in query and any([bad in query for bad in blacklist]):
            return render_template_string(error_page)

        if len(query) > 256:
            return render_template_string(error_page)

        page = \
            '''
        {{% extends "layout.html" %}}
        {{% block body %}}
        <center>
           <section class="section">
              <div class="container">
                 <h1 class="title">You have entered the raffle!</h1>
                 <ul class=flashes>
                    <label>Hey {}! We have received your entry! Good luck!</label>
                 </ul>
                 </br>
              </div>
           </section>
        </center>
        {{% endblock %}}
        '''.format(query)

    elif request.method == 'GET':
        page = \
            '''
        {% extends "layout.html" %}
        {% block body %}
        <center>
            <section class="section">
              <div class="container">
                 <h1 class="title">Welcome to the idekCTF raffle!</h1>
                 <p>Enter your name below for a chance to win!</p>
                 <form action='/' method='POST' align='center'>
                    <p><input name='q' style='text-align: center;' type='text' placeholder='your name' /></p>
                    <p><input value='Submit' style='text-align: center;' type='submit' /></p>
                 </form>
              </div>
           </section>
        </center>
        {% endblock %}
        '''
    return render_template_string(page)


app.run('0.0.0.0', 1337)

