import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user, current_user
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'
app.config["MONGO_URI"] = "mongodb://mongodb:27017/anya"
mongo = PyMongo(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.urandom(16).hex()

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({'login': username})
    return User(username=user['login'], password=user['password'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if mongo.db.users.find_one({'login': username, 'password': password}):
            user = User(username=username, password=password)
            login_user(user)
            return redirect('/cabinet')
        else:
            return redirect('/invalid')
    return render_template('login.html')


# Add registration function to append new users on http://localhost:5000/register/
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if mongo.db.users.find_one({'login': username}):
            return "Login is taken"
        else:
            mongo.db.users.insert({'login': username, 'password': password})
    return render_template('register.html')


#Add image upload function in cabinet http://localhost:5000/cabinet/
@app.route('/cabinet', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file extension', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Successfully saved', 'success')
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template('cabinet.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/invalid')
def invalid():
    return render_template('invalid.html')


# Return static images and files on http://localhost:5000/static/<image_name>
@app.route('/static/<path:filename>')
def show_files_files(filename):
    return send_from_directory('static', filename)

#http://localhost:5000/upload/<image_name>.png
@app.route('/upload/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
