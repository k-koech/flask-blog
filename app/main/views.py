import secrets, os
from . import main
from app.models import Comments, Post, User
from app import db
from flask import url_for, render_template, flash, redirect, request, abort
from .forms import PostForm, UpdateAccountForm, CommentForm
from flask_login import  current_user, login_required
from PIL import Image
import json
from ..requests import get_quotes
from ..email import mail_message

@main.route("/home")
@main.route("/")
def home():
    raw_quotes = get_quotes()
    quotes = json.loads(raw_quotes)
    posts = Post.query.all()
    return render_template("home.html", posts=posts, quotes=quotes)

"""SUBSCRIBE VIEW"""
@main.route("/subscribe/<user_id>",methods=['GET','POST'])
@login_required
def subscibe(user_id):
    if current_user.subscribe==True:
        current_user.subscribe=False
        db.session.commit()
        flash("Unsubscribed successfully! You will no longer receive our updates!", "success")
    else:
        current_user.subscribe=True
        db.session.commit()
        flash("You have subscribed to our email! You will be receieving updates!", "success")
    return redirect(url_for('main.home'))


def save_picture(form_pic):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('/home/moringa/Desktop/CORE/flask/blogs/app/static/profile_images',picture_fn)
    form_pic.save(picture_path)
    output_size=(125,125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


"""PROFILE VIEW"""
@main.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
                picture_file=save_picture(form.picture.data)
                current_user.image_file=picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for('main.profile'))
    elif request.method=="GET":
        raw_quotes = get_quotes()
        quotes = json.loads(raw_quotes)
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_url=url_for('static',filename='profile_images/'+current_user.image_file)
    return render_template("profile.html", title="Account", image_file=image_url, form=form, quotes=quotes)


"""NEW POST VIEW"""
@main.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
   form = PostForm()
   raw_quotes = get_quotes()
   quotes = json.loads(raw_quotes)
   if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        flash("Your post has been published", "success")
        db.session.add(post)
        db.session.commit()

        users = User.query.filter_by(subscribe=True).all()
        print(users)
        for user in users:
            mail_message("KK Blog New Article","email/welcome_user",user.email,user=user)
    

        return redirect(url_for('main.home'))
   return render_template("create_post.html",form=form, title="New Post",quotes=quotes,legend="New Post",blog_title=form.title.data)

"""INDIVIDUAL POST VIEW"""
@main.route("/post/<id>", methods=['GET','POST'])
@login_required
def post(id):
    form = CommentForm()

    raw_quotes = get_quotes()
    quotes = json.loads(raw_quotes)

    comments = Comments.query.filter_by(post_id=id).all()
    post = Post.query.get_or_404(id)
    return render_template("post.html", title=post.title,post=post, quotes=quotes, form=form, comments=comments)

"""UPDATE POST VIEW"""
@main.route("/post/update/<id>", methods=['GET','POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    raw_quotes = get_quotes()
    quotes = json.loads(raw_quotes)
    if post.author ==current_user:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Changes saved successfully", "success")
            return redirect(url_for('main.post', id=post.id))
        elif request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        title = "Update Post"
        return render_template("create_post.html", title=title,form=form, legend="Update Post", quotes=quotes)
    else:
        abort(403)

"""DELETE POST VIEW"""
@main.route("/post/delete/<id>", methods=['POST'])
@login_required
def post_delete(id):
    post = Post.query.get_or_404(id)
    if post.author ==current_user:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted successfully!", "success")
        return redirect(url_for('main.home'))
    else:
        abort(403)

"""DELETE COMMENT"""
@main.route("/post/<postid>/comment/<id>", methods=['POST',"GET"])
@login_required
def delete_comment(postid=None,id=None):
    comment = Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted", "success")
    return redirect("/post/"+postid)

    
"""ADD COMMENT"""
@main.route("/post/<post_id>/comment", methods=['GET','POST'])
@login_required
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comments(post_id=post_id, comment=form.comment.data, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment Submitted", "success")
        
    return redirect("/post/"+post_id)



