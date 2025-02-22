from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploadedfiles/'
ALLOWED_EXTENSIONS = {'py', 'html', 'css', 'js', 'png', 'jpeg', 'jpg', 'gif', 'pdf', 'docx', 'pptx', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'jhguidsfhvuidsfbgisdbvsdbvudfgfusdbvhusdbfgdsbvhdsfbf'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/",methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save()
            return redirect(url_for('download_file', name=filename))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)