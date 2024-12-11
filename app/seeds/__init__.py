from app.models.db import environment

from flask.cli import AppGroup
from .users import seed_users, undo_users
from .parent_a import seed_parent_a, undo_parent_a
from .child_a import seed_child_a, undo_child_a
from .parent_b import seed_parent_b, undo_parent_b
from .child_b import seed_child_b, undo_child_b

from .mtm_parent import seed_mtm_parent, undo_mtm_parent
from .mtm_parent_child import seed_mtm_parent_child, undo_mtm_parent_child
from .mtm_child import seed_mtm_child, undo_mtm_child

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        undo_mtm_parent_child()
        undo_mtm_child()
        undo_mtm_parent()
        
        undo_child_b()
        undo_parent_b()
        undo_child_a()
        undo_parent_a()
        
        undo_users()
    seed_users()
    
    seed_parent_a()
    seed_child_a()
    seed_parent_b()
    seed_child_b()
    
    seed_mtm_parent()
    seed_mtm_child()
    seed_mtm_parent_child()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_mtm_parent_child()
    undo_mtm_child()
    undo_mtm_parent()
    
    undo_child_b()
    undo_parent_b()
    undo_child_a()
    undo_parent_a()
    
    undo_users()
    # Add other undo functions here
