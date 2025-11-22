from flask import Blueprint,request,jsonify
from web.models import ToDo
from app import db

api_bp=Blueprint("api",__name__)

@api_bp.route("/tasks",methods=["GET"])
def get_tasks():
    tasks=ToDo.query.all()
    results=[
        {"id":t.sno,"title":t.title,"desc":t.desc}
        for t in tasks
    ]
    return jsonify(results),200

@api_bp.route("/tasks",methods=["POST"])
def create_task():
    data =request.get_json()

    if not data or "title" not in data or "desc" not in data:
        return jsonify({"error":"Task field required"})
    
    new_task=ToDo(title=data["title"],desc=data["desc"])
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"id":new_task.sno}),201