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

@api_bp.route("/tasks/<int:sno>",methods=["PUT"])
def update_task(sno):
    data =request.get_json()

    task=ToDo.query.get(sno)
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404
    task.title=data["title"]
    task.desc=data["desc"]

    try:
        db.session.commit()
        return jsonify({
            "success": True,
            "data": {
                "id": task.sno,
                "title": task.title,
                "desc": task.desc
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasks/<int:sno>",methods=["DELETE"])
def delete_task(sno):
    data =request.get_json()
    todo = ToDo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"sno":"Deleted"}),200
    