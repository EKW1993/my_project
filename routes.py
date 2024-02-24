from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def homepage():
    all_posts = Entry.query.all()
    return render_template("homepage.html", all_posts=all_posts)

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
