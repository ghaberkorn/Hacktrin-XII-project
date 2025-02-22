from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploadedfiles/'
ALLOWED_EXTENSIONS = {'py', 'html', 'css', 'js', 'png', 'jpeg', 'jpg', 'gif', 'pdf', 'docx', 'pptx', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'jhguidsfhvuidsfbgisdbvsdbvudfgfusdbvhusdbfgdsbvhdsfbf'

loggedIn = False

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    # Check if user is logged in
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
    # Serve the uploaded file
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    global loggedIn
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # For simplicity, assume login is always successful
        # Replace this with real authentication (database check, etc.)
        if username == 'admin' and password == 'password':  # Example login check
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

@app.route('/register/')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(24)  # Ensure you have a secret key for sessions
    app.run(debug=True)
