from flask import render_template, request, session, flash, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
from blog.forms import LoginForm
import functools

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route("/")
def homepage():
    all_posts = Entry.query.all()
    return render_template("homepage.html", all_posts=all_posts)
@login_required
def create_or_edit_entry(entry_id=None):
    errors = None

    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    else:
        entry = Entry()
        form = EntryForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('homepage'))
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return create_or_edit_entry()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return create_or_edit_entry(entry_id)



@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash('Entry deleted successfully.', 'success')
    else:
        flash('Entry not found.', 'error')
        
    return redirect(url_for('homepage'))
