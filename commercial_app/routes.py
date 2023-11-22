from flask import request, redirect, url_for, flash, render_template, abort, jsonify
from commercial_app import app, db
from commercial_app.forms import UserLoginForm, UserRegistrationForm, \
    AdminRegistrationForm, AdminLoginForm, UpdateAccountForm, PostForm
from commercial_app.models import User, Post, Admin
from flask_login import login_user, current_user, logout_user, login_required
from commercial_app import bcrypt
import secrets
import os
from PIL import Image
from flask_jwt_extended import get_jwt_identity,create_access_token, jwt_required, JWTManager

@app.route("/")
def homePage():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('layout.html', posts=posts)
#sample

def save_profile_picture(form_picture, picture_type):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, f'static/{picture_type}', picture_fname)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fname

def save_product_picture(form_picture, picture_type):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, f'static/{picture_type}', picture_fname)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fname

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data, 'profile_pic')
            current_user.image_file = picture_file
        if form.username.data == current_user.username and not form.picture.data and form.email.data == current_user.email:
            pass
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your Account has been updated successfully', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, user=current_user)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_product_picture(form.picture.data, 'product_image')
            post = Post(title=form.title.data, content=form.content.data, 
                        price=form.price.data,author=current_user,tags=[i for i in form.tags.data])
            post.product_image = picture_file
            db.session.add(post)
            db.session.commit()
            flash(f'Your post has been uploaded successfully', 'success')
            return redirect(url_for('homePage'))
        elif request.method == 'GET':
            pass
    return render_template('create_post.html',
                           title='New Design Post',
                           form=form, legend='New Post')


@app.route("/login", methods=['GET', 'POST'])
def userLogin():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('homePage'))
        elif user is None:
            flash(f'User not registered. Please create an account', 'warning')
        else:
            flash(f'Logging In Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('homePage'))
        elif admin is None:
            flash(f'Admin not registered. Please create an account', 'warning')
        else:
            flash(f'Logging In Unsuccessful. Please check email and password', 'danger')
    return render_template('admin_login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Accounted created successfully. You can log In', 'success')
        return redirect(url_for('userLogin'))
    return render_template('register.html', form=form)

@app.route("/admin/register", methods=['GET', 'POST'])
def adminRegister():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = Admin(username=form.username.data,
                    email=form.email.data, password=hashed_pwd, \
                        client_secret=form.client_secret.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Accounted created successfully. You can log In', 'success')
        return redirect(url_for('adminLogin'))
    return render_template('adminRegister.html', form=form)


@app.route("/account/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    flash(f'Your account has been deleted successfully', 'success')
    return redirect(url_for('homePage'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homePage'))



