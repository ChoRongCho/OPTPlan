from dataclasses import dataclass, field
from typing import List

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: List[int] = field(default_factory=list)
    
    # Object physical properties
    is_fragile: bool = False
    is_rigid: bool = False
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    is_fragile=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='white_3D_cuboid', 
    color='white', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_fragile=True, 
    is_foldable=True, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object4 = Object(
    index=4, 
    name='translucent_2D_circle', 
    color='translucent', 
    shape='2D_circle', 
    object_type='obj', 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object5 = Object(
    index=5, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'green_3D_cylinder', 'in_box': False, 'out_box': True},
        1: {'name': 'black_3D_cylinder', 'in_box': False, 'out_box': True},
        2: {'name': 'white_3D_cuboid', 'in_box': False, 'out_box': True},
        3: {'name': 'white_3D_cylinder', 'in_box': False, 'out_box': True},
        4: {'name': 'translucent_2D_circle', 'in_box': False, 'out_box': True},
        5: {'name': 'white_box', 'in_box': True, 'out_box': False}
    }

    goal_state = {
        0: {'name': 'green_3D_cylinder', 'in_box': True, 'out_box': False},
        1: {'name': 'black_3D_cylinder', 'in_box': True, 'out_box': False},
        2: {'name': 'white_3D_cuboid', 'in_box': True, 'out_box': False},
        3: {'name': 'white_3D_cylinder', 'in_box': True, 'out_box': False},
        4: {'name': 'translucent_2D_circle', 'in_box': True, 'out_box': False},
        5: {'name': 'white_box', 'in_box': True, 'out_box': False}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place soft objects first (object3 and object4)
    # 2. Place rigid and fragile objects (object0, object1, object2)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # c) Action sequence
    # Place soft objects first
    robot.place(object3, box)
    robot.place(object4, box)

    # Place rigid and fragile objects
    robot.place(object0, box)
    robot.place(object1, box)
    robot.fold(object2)  # Fold the foldable object before placing
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed soft objects (object3 and object4) first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # 2. Folded the foldable object (object2) before placing it in the box.
    # 3. Placed all other objects in the box following the rules.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
