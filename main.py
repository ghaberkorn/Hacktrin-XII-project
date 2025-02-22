from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploadedfiles/'
ALLOWED_EXTENSIONS = {'py', 'html', 'css', 'js', 'png', 'jpeg', 'jpg', 'gif', 'pdf', 'docx', 'pptx', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'jhguidsfhvuidsfbgisdbvsdbvudfgfusdbvhusdbfgdsbvhdsfbf'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
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
    return render_template('index.html')

@app.route('/uploads/<name>')
def download_file(name):
    # Serve the uploaded file
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def login():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
