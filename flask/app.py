from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!'
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/map')
def map(): 
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='5000')
