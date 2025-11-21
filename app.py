from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db =SQLAlchemy(app)

class ToDo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno} -{self.title}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo =ToDo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=ToDo.query.all()
    return render_template("index.html",allTodo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = ToDo.query.get_or_404(sno)

    if request.method == "POST":
        print("Before:", todo.sno, todo.title, todo.desc)

        todo.title = request.form['title']
        todo.desc = request.form['desc']

        print("After:", todo.sno, todo.title, todo.desc)

        db.session.commit()
        return redirect("/")

    return render_template("update.html", todo=todo)



if __name__=="__main__":
    app.run(debug=True,port=8000)