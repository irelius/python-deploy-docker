from app.models import db, MTM_Parent_Child, environment, SCHEMA

def seed_mtm_parent_child():
    how_many_parents = 3
    how_many_children = 3

    for parent in range(0, how_many_parents):
        for child in range(parent, how_many_children):
            template = MTM_Parent_Child(mtm_parent_join_id=parent+1, mtm_child_join_id=child+1, mtm_extra_data=f"join table extra data for {parent+1}:{child+1}")
            
            # # seed command if "secondary" option was used. Refer to MODEL_README.md for more information
            # template = MTM_Parent_Child(mtm_parent_join_id=parent+1, mtm_child_join_id=child+1)
            
            db.session.add(template)
            
    db.session.commit()
            


def undo_mtm_parent_child():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.mtm_parent_children RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM mtm_parent_children")

    db.session.commit()