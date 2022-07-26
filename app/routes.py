from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, UserForm, ItemForm, DateSearchForm
from app.models import User, Item
from datetime import date


@app.route('/')
@app.route('/index')
def index():
    markdown_items = Item.query.filter_by(markdown=date.today()).all()
    expired_items = Item.query.filter_by(expiration=date.today()).all()
    return render_template('index.html', title='Fridge Manager', markdown_items=markdown_items, expired_items=expired_items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/view_users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('users.html', title='Users', users=users)


@app.route('/user_dashboard/<user_id>')
@login_required
def user_dashboard(user_id):
    user = User.query.get(int(user_id))
    return render_template('user.html', title='User Dashboard', user=user)


@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(int(user_id))
    form = UserForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_dashboard', user_id=user_id))
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    return render_template('edit_user.html', title='Edit User', form=form)


@app.route('/view_inventory')
@login_required
def view_inventory():
    items = Item.query.all()
    return render_template('view_inventory.html', title='View Inventory', items=items)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(upc=form.upc.data, name=form.name.data, markdown=form.markdown.data,
                    expiration=form.expiration.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('view_inventory'))
    return render_template('add_item.html', title='Add Item', form=form)


@app.route('/edit_item/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get(int(item_id))
    form = ItemForm()
    if form.validate_on_submit():
        item.upc = form.upc.data
        item.name = form.name.data
        item.markdown = form.markdown.data
        item.expiration = form.expiration.data
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', title='Edit Item', form=form)


def delete_item(item_id):
    item = Item.query.get(int(item_id))
    db.session.delete(item)
    db.session.commit()
    
    
@app.route('/delete_item_index/<item_id>')
@login_required
def delete_item_index(item_id):
    delete_item(item_id=item_id)
    return redirect(url_for('index'))


@app.route('/delete_item_inventory/<item_id>')
@login_required
def delete_item_inventory(item_id):
    delete_item(item_id=item_id)
    return redirect(url_for('view_inventory'))


@app.route('/delete_item_markdown/<markdown_date>/<item_id>')
@login_required
def delete_item_markdown(markdown_date, item_id):
    delete_item(item_id=item_id)
    return redirect(url_for('view_markdown_items', markdown_date=markdown_date))


@app.route('/delete_item_expired/<expiration_date>/<item_id>')
@login_required
def delete_item_expired(expiration_date, item_id):
    delete_item(item_id=item_id)
    return redirect(url_for('view_expired_items', expiration_date=expiration_date))


@app.route('/view_markdown_items/<markdown_date>')
@login_required
def view_markdown_items(markdown_date):
    items = Item.query.filter_by(markdown=markdown_date).all()
    return render_template('view_markdown_items.html', title='View Markdown Items', items=items,
                           markdown_date=markdown_date)


@app.route('/search_markdown_date', methods=['GET', 'POST'])
@login_required
def search_markdown_date():
    form = DateSearchForm()
    if form.validate_on_submit():
        return redirect(url_for('view_markdown_items', markdown_date=form.date.data))
    return render_template('search_markdown_date.html', title='Search Markdown Date', form=form)


@app.route('/view_expired_items/<expiration_date>')
@login_required
def view_expired_items(expiration_date):
    items = Item.query.filter_by(expiration=expiration_date).all()
    return render_template('view_expired_items.html', title='View Expired Items', items=items,
                           expiration_date=expiration_date)


@app.route('/search_expiration_date', methods=['GET', 'POST'])
@login_required
def search_expiration_date():
    form = DateSearchForm()
    if form.validate_on_submit():
        return redirect(url_for('view_expired_items', expiration_date=form.date.data))
    return render_template('search_expiration_date.html', title='Search Expiration Date', form=form)
