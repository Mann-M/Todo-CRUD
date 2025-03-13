from flask import Flask , render_template, request, url_for,flash, redirect, session,g
from flask_migrate import Migrate
from models import db, Todo , User
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__ , template_folder="templates")

    # db configuration
    database_url = os.environ.get("DATABASE_URL")
    print("DATABASE_URL:", database_url)  # For debugging in logs
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set")

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    if 'localhost' not in database_url and "sslmode" not in database_url:
        database_url += "?sslmode=require"

    #configuration

    app.config["SQLALCHEMY_DATABASE_URI"]=database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["SECRET_KEY"]=os.environ.get('SECRET_KEY')  # Change in production!


    # initialize db
    db.init_app(app)
    Migrate(app,db)

    # Security headers for production
    if app.config.get('FLASK_ENV') == 'production':
        app.config.update(
            SESSION_COOKIE_SECURE=True,
            REMEMBER_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='Lax'
        )

    @app.before_request
    def load_logged_in_user():
        # load the user from session before each request and store in 'g'
        g.is_authenticated= 'user_id' in session
        g.name = None
        if g.is_authenticated:
            user=User.query.filter_by(user_id = session['user_id']).first()
            g.name = user.name if user else 'Guest'

    # ---------------authentication-routes------------------
    @app.route('/login', methods = ['GET','POST'])
    def login():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            password = request.form.get('password')
            user = User.query.filter_by(user_id = user_id).first()
            if user and user.check_password(password):
                session['user_id'] = user.user_id
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else :
                flash('Invalid credentials', 'danger')
        return render_template('login.html')

    @app.route('/signup', methods = ['GET','POST'])
    def signup():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            password = request.form.get('password')
            name = request.form.get('name')
            email_id = request.form.get('email_id')
            dob_str = request.form.get('dob') # expected format "yyyy-mm-dd"

            dob=None
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d')
                except ValueError:
                    flash('Date of birth be in the format YYYY-MM-DD.', 'danger' )
                    return render_template('signup.html')

            existing_user = User.query.filter_by(user_id=user_id).first()
            existing_email = User.query.filter_by(email_id=email_id).first()
            if existing_user or existing_email:
                flash('User or email-id already exist. Please choose a different one', 'danger')
                return render_template('signup.html')

            new_user = User(user_id=user_id, name = name , dob = dob, email_id = email_id)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html')


    @app.route('/index')
    @app.route('/')
    def index():
        if 'user_id' in session:
            todos_count = Todo.query.filter_by(user_id = session['user_id']).count()
            todos = Todo.query.filter_by(user_id = session['user_id']).all()
            complete_todo = Todo.query.filter_by(user_id = session['user_id'] ,action=True).count()
            not_completed_todo = Todo.query.filter_by(user_id = session['user_id'],action=False).count()
            return render_template('index.html',todos = todos, not_completed_todo=not_completed_todo, complete_todo=complete_todo, todos_count = todos_count)
        return render_template('index.html')

    # --------CRUD Routes------------
    # CREATE : Form to add new Todo
    @app.route('/todo/new', methods = ['GET', 'POST'])
    def create_todo():
        if 'user_id' not in session:
            flash('Please log in to create a Todo.', 'danger')
            return redirect(url_for('login'))

        if request.method == 'POST' :
            title = request.form.get('title')
            description = request.form.get('description')
            priority = request.form.get('priority')
            new_todo = Todo(title = title, description = description , priority = priority, user_id = session['user_id'])
            db.session.add(new_todo)
            db.session.commit()

            flash('Todo created successfully', 'success')
            return redirect(url_for('index'))

        return render_template('create_todo.html')

    # UPDATE : Edit existing todo
    @app.route('/todo/edit/<int:todo_id>', methods = ['GET', 'POST'])
    def edit_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        if request.method == 'POST':
            todo.title = request.form.get('title')
            todo.description = request.form.get('description')
            todo.priority = request.form.get('priority')
            db.session.commit()
            flash('Todo updated successfully', 'success')
            return redirect(url_for('index'))
        return render_template('edit_todo.html', todo = todo)

    # Complete todo toggle : completion stage
    @app.route('/todo/complete/<int:todo_id>', methods = ['POST'])
    def complete_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        if not todo.action:
            todo.action = True
            todo.completed_at = datetime.now(timezone.utc)
        else :
            todo.action = False
            todo.completed_at = None
        db.session.commit()
        flash("Todo status updated", 'success')
        return redirect(url_for('index'))

    # # DELETE : delete a todo if it is completed for atleat a week or deleted manually
    # @app.route('/todo/delete/<int:todo_id>', methods=['POST'])
    # def delete_todo(todo_id):
    #     todo = Todo.query.get_or_404(todo_id)
    #     if todo.action and todo.completed_at :
    #         if datetime.now(timezone.utc) - todo.completed_at >= timedelta(days=7):
    #             db.session.delete(todo)
    #             db.session.commit()
    #     return

    @app.route('/todo/force-delete/<int:todo_id>', methods=['POST'])
    def delete(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted successfully", 'success')
        return redirect(url_for('index'))

    @app.route('/profile')
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect if not logged in
        user = User.query.get_or_404(session['user_id'])
        return render_template('profile.html', user=user)

    # ----------logout endpoint-----------
    @app.route('/logout')
    def logout():
        session.pop('user_id',None)
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))

    @app.route('/change_password', methods = ['GET','POST'])
    def change_password():
        if request.method == 'POST':
            if 'user_id' in session:
                user = User.query.filter_by(user_id = session['user_id']).first()
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')

                if user.check_password(old_password):
                    user.set_password(new_password)
                    db.session.commit()
                    flash('New password set - Successful!', 'success')
                    return redirect(url_for('profile'))
                flash("Wrong password!", 'danger')
                return redirect(url_for('change_password'))
        return render_template('change_password.html')

    return app


flask_app = create_app()

if __name__ == '__main__':
    # Never run with debug=True in production!
    flask_app.run(port=int(os.environ.get('PORT', 2300)),
                debug=os.environ.get('DEBUG_MODE', 'false').lower() == 'true')