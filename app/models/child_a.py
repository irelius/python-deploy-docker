from .db import db, environment, SCHEMA, add_prefix_for_prod

# One-to-Many from Parent_A to Child_A. One direction
class Child_A(db.Model):
    __tablename__ = 'child_a'
    
    if environment == "production":
        print('production conditional child_a', SCHEMA)
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    child_a = db.Column(db.String(100), nullable=False)
    
    # parent_a_id is foreign key column. References table "parent_a" column "id"
    parent_a_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("parent_a.id")))
    
    def to_dict(self):
        return {
            'id': self.id,
            'child_a': self.child_a,
            'parent_a_id': self.parent_a_id
        }