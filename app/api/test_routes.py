from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User, Parent_A, Parent_B, Child_A, Child_B, MTM_Child, MTM_Parent, MTM_Parent_Child


test_routes = Blueprint('test', __name__)

@test_routes.route('/parent_a')
def get_all_parent_a():
    parents = Parent_A.query.all()
    return {'parent_a': [parent_a.to_dict() for parent_a in parents]}


@test_routes.route('/parent_b')
def get_all_parent_b():
    parents = Parent_B.query.all()
    return {'parent_b': [parent_b.to_dict() for parent_b in parents]}

@test_routes.route('/child_a')
def get_all_child_a():
    parents = Child_A.query.all()
    return {'child_a': [child_a.to_dict() for child_a in parents]}


@test_routes.route('/child_b')
def get_all_child_b():
    parents = Child_B.query.all()
    return {'child_b': [child_b.to_dict() for child_b in parents]}
