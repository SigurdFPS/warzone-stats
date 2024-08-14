from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

COD_API_BASE_URL = "https://api.tracker.gg/api/v2/warzone/standard"

def get_warzone_stats(username, platform, password):
    url = f"{COD_API_BASE_URL}/profile/{platform}/{username}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {password}"  # Use the password as a Bearer token for authentication
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve data: {response.status_code}"}

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    platform = request.form['platform']
    password = request.form['password']  # Capture the password

    # Save user information in session
    session['username'] = username
    session['platform'] = platform
    session['password'] = password  # Save password in session for later API calls
    session['logged_in'] = True

    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('platform', None)
    session.pop('password', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    
    username = session.get('username')
    platform = session.get('platform')
    password = session.get('password')
    stats = get_warzone_stats(username, platform, password)

    return render_template('profile.html', stats=stats, username=username)

if __name__ == '__main__':
    app.run(debug=True)
