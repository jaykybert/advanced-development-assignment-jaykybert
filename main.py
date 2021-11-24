from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/submitted', methods=['POST'])
def register_complete():
    name = request.form['name']
    email = request.form['email']

    return render_template('register_complete.html',
                           name=name, email=email)


# Page Not Found
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error=e)


# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error=e)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


