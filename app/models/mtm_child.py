from .db import db, environment, SCHEMA, add_prefix_for_prod

class MTM_Child(db.Model):
    __tablename__ = 'mtm_children'
    
    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    mtm_child_col = db.Column(db.String(100), nullable=False)
    
    mtm_parent_relationship = db.relationship("MTM_Parent_Child", back_populates="mtm_child_join")

    def to_dict(self):
        return {
            'id': self.id,
            "mtm_child_col": self.mtm_child_col,
            "mtm_parents": {parent.mtm_parent_join_id: parent.to_dict() for parent in self.mtm_parent_relationship}
        }


# -------------------------------------------------------------------------


# # class with 'secondary' option
# class MTM_Child(db.Model):
#     __tablename__ = 'mtm_children'

#     id = db.Column(db.Integer, primary_key=True)
#     mtm_child_col = db.Column(db.String(100), nullable=False)
    
#     mtm_parent_relationship = db.relationship("MTM_Parent", secondary = "mtm_parent_children", back_populates = "mtm_children_relationship")

#     def to_dict(self):
#         return {
#             'id': self.id,
#             "mtm_child_col": self.mtm_child_col
#         }
