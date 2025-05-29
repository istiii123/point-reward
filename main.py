from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'secret'

users = {
    'andi': {'password': '123', 'name': 'Andi', 'brand': 'Osha Snack', 'coins': 120, 'history': []},
    'budi': {'password': 'abc', 'name': 'Budi', 'brand': 'Anaconda', 'coins': 200, 'history': []},
    'cici': {'password': 'xyz', 'name': 'Cici', 'brand': 'Viscofe', 'coins': 150, 'history': []},
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Login gagal"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user = users[username]
    return render_template('dashboard.html', user=user)

@app.route('/redeem', methods=['GET', 'POST'])
def redeem():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user = users[username]
    if request.method == 'POST':
        amount = int(request.form['amount'])
        if amount <= user['coins']:
            user['coins'] -= amount
            user['history'].append(f"Tukar {amount} koin")
            return redirect(url_for('dashboard'))
    return render_template('redeem.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

app.run(host='0.0.0.0', port=81)
