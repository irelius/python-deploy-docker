from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import db, User, Parent_A, Parent_B, Child_A, Child_B, MTM_Child, MTM_Parent, MTM_Parent_Child

test_routes = Blueprint('test', __name__)

@test_routes.route('/')
def test_route():
    return "Test route hello"


@test_routes.route('/users')
def get_all_users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@test_routes.route('/parent_a')
def get_all_parent_a():
    parents = Parent_A.query.all()
    return {'parent_a': [parent_a.to_dict() for parent_a in parents]}


@test_routes.route('/parent_a/<int:parent_id>/children')
def get_all_parent_a_children(parent_id):
    parents = (Parent_A.query.get(parent_id)).to_dict()
    children = Child_A.query.filter(Child_A.parent_a_id == parent_id)
    parents["child_a"] = {child_a.id: child_a.to_dict() for child_a in children}
    
    return parents


@test_routes.route('/parent_b')
def get_all_parent_b():
    parents = Parent_B.query.all()
    return {'parent_b': [parent_b.to_dict() for parent_b in parents]}


@test_routes.route('/child_a')
def get_all_child_a():
    children = Child_A.query.all()
    return {'child_a': [child_a.to_dict() for child_a in children]}


@test_routes.route('/child_b')
def get_all_child_b():
    children = Child_B.query.all()
    return {'child_b': [child_b.to_dict() for child_b in children]}


@test_routes.route('/mtm_child')
def get_all_mtm_child():
    children = MTM_Child.query.filter().all()
    return {'mtm_child': [mtm_child.to_dict() for mtm_child in children]}


@test_routes.route('/mtm_child/<int:child_id>')
def get_one_mtm_child_parents(child_id):
    # mtm_child = db.get_or_404(MTM_Child, child_id) # <--- More up to date version of fetch
    mtm_child = MTM_Child.query.get(child_id) # <---- Technically deprecated
    return {"mtm_child": {child_id: mtm_child.to_dict()}}


@test_routes.route('/mtm_child/<int:child_id>/parents')
def get_all_mtm_child_parents(child_id):
    child = MTM_Child.query.get(child_id)
    data = child.to_dict()
    
    parent_child = MTM_Parent.query.join(MTM_Parent_Child).filter(MTM_Parent_Child.mtm_child_join_id == child_id).all()
    
    data['parent'] = {parent.id: parent.to_dict() for parent in parent_child}
    return data


@test_routes.route('/mtm_parent')
def get_all_mtm_parent():
    parents = MTM_Parent.query.all()
    return {'mtm_parent': [mtm_parent.to_dict() for mtm_parent in parents]}