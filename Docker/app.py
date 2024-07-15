from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    save_to_db(name, email)
    return 'Data saved to database!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # You can add your authentication logic here
        if username == 'admin' and password == 'netcon':  # Simplified example
            return redirect(url_for('welcome', username=username))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

def save_to_db(name, email):
    conn = mysql.connector.connect(
        host='mysql-service',  # Kubernetes service name
        user='netcon',
        password='netcon',  # Make sure it matches the secret
        database='userdb'
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
