from flask import Flask

app = Flask(__name__)

@app.route("/")
def ciao_mondo():
    return '<h1>Ciao, Mondo!</h1>'

app.run(debug=True)

from flask import Flask, render_template

@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Il tuo risultato o codice Python da mostrare
    risultato = "Ciao, questo è il riscontro del codice Python!"
    return render_template('index.html', output_python=risultato)

if __name__ == '__main__':
    app.run(debug=True)


