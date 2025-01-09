from .db import db, environment, SCHEMA, add_prefix_for_prod

# Join table for MTM_Parent and MTM_Child
class MTM_Parent_Child(db.Model):
    __tablename__ = 'mtm_parent_children'
    
    if environment == "prsoduction":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    mtm_extra_data = db.Column(db.String(150), nullable=False)

    mtm_parent_join_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("mtm_parents.id")))
    mtm_child_join_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("mtm_children.id")))

    mtm_parent_join = db.relationship("MTM_Parent", back_populates="mtm_children_relationship")
    mtm_child_join = db.relationship("MTM_Child", back_populates="mtm_parent_relationship")
    
    def to_dict(self):
        return {
            'id': self.id,
            "mtm_extra_data": self.mtm_extra_data,
            "mtm_parent_join_id": self.mtm_parent_join_id,
            "mtm_child_join_id": self.mtm_child_join_id
        }


# -------------------------------------------------------------------------


# # class with 'secondary' option. Makes it easier for connecting a many-to-many, but it only works for a join table without extra data.
# class MTM_Parent_Child(db.Model):
#     __tablename__ = 'mtm_parent_children'

#     id = db.Column(db.Integer, primary_key=True)
#     # mtm_extra_data would go here, but it doesn't work with "secondary"

#     mtm_parent_join_id = db.Column(db.Integer, db.ForeignKey("mtm_parents.id"))
#     mtm_child_join_id = db.Column(db.Integer, db.ForeignKey("mtm_children.id"))
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             "mtm_parent_join_id": self.mtm_parent_join_id,
#             "mtm_child_join_id": self.mtm_child_join_id
#         }
