from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, RegistrationForm, ChangePasswordForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.config import posts_pagination


# Register index route
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=posts_pagination, page=page)
    return render_template('pages/index.html', posts=posts)

# Register registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, display_name=form.displayName.data,
            password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You may now log in', 'success')
        return redirect(url_for('login'))
    return render_template('pages/register.html', title='Register', form=form)

# Register login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, display_name=form.displayName.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.rememberMe.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('index'))
        else:
            flash('Username and password combination incorrect', 'danger')
    return render_template('pages/login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashedPassword
        db.session.commit()
        flash(f'Your password has been updated', 'success')
        return redirect(url_for('account'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=posts_pagination)
    return render_template('pages/account.html', title='My Account', form=form, posts=posts)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('account'))
    return render_template('pages/create_post.html', title='Create Post', form=form)

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('pages/view_post.html', post=post)


@app.route('/user/<string:user_display_name>')
def user(user_display_name):
    if current_user.is_authenticated and current_user.display_name == user_display_name:
        return redirect(url_for('account'))
    user = User.query.filter_by(display_name=user_display_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=posts_pagination)
    return render_template('pages/user.html', user=user, posts=posts)

