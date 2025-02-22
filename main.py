from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
import os, sqlite3

UPLOAD_FOLDER = 'uploadedfiles/'
ALLOWED_EXTENSIONS = {'html', 'css', 'py', 'java'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'jhguidsfhvuidsfbgisdbvsdbvudfgfusdbvhusdbfgdsbvhdsfbf'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to search through uploaded files
def search_in_uploaded_files(query):
    result_files = []
    
    # Loop through all files in the uploaded_files directory
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if os.path.isfile(file_path) and allowed_file(filename):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check if the query is in the file content
                if query.lower() in content.lower():
                    result_files.append(filename)
    
    return result_files

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session or not session['logged_in']:
        flash('You need to be logged in to upload files')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again')

    return render_template('login.html')

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Registration successful, please log in')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists, please choose another')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/mission/')
def mission():
    return render_template('mission.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get('query', '')
    results = []

    if query:
        results = search_in_uploaded_files(query)
    
    return render_template("search.html", results=results, query=query)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
