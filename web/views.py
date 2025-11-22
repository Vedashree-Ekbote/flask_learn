from flask import Blueprint, render_template, request, redirect
from extensions import db
from web.models import ToDo

web_bp = Blueprint("web", __name__, template_folder="templates")

@web_bp.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        todo = ToDo(title=request.form['title'], desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    return render_template("index.html", allTodo=ToDo.query.all())

@web_bp.route("/delete/<int:sno>")
def delete(sno):
    todo = ToDo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@web_bp.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = ToDo.query.get_or_404(sno)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)
