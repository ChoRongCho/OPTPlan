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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
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
    name='white_3D_cuboid', 
    color='white', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_foldable=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='yellow_2D_triangle', 
    color='yellow', 
    shape='2D_triangle', 
    object_type='obj', 
    is_foldable=True, 
    is_soft=True, 
    in_box=True, 
    out_box=False
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box_objects=[]
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'green_3D_cylinder', 'in_box': False, 'out_box': True, 'is_rigid': True, 'is_fragile': True},
        1: {'name': 'white_3D_cuboid', 'in_box': False, 'out_box': True, 'is_foldable': True},
        2: {'name': 'white_3D_cylinder', 'in_box': False, 'out_box': True, 'is_soft': True, 'is_elastic': True},
        3: {'name': 'yellow_2D_triangle', 'in_box': True, 'out_box': False, 'is_foldable': True, 'is_soft': True},
        4: {'name': 'white_box', 'in_box_objects': []}
    }

    goal_state = {
        0: {'name': 'green_3D_cylinder', 'in_box': True, 'out_box': False},
        1: {'name': 'white_3D_cuboid', 'in_box': True, 'out_box': False},
        2: {'name': 'white_3D_cylinder', 'in_box': True, 'out_box': False},
        3: {'name': 'yellow_2D_triangle', 'in_box': True, 'out_box': False},
        4: {'name': 'white_box', 'in_box_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (white_3D_cylinder) in the box first.
    # 2. Fold the foldable object (white_3D_cuboid) if necessary.
    # 3. Place the foldable object (white_3D_cuboid) in the box.
    # 4. Place the rigid and fragile object (green_3D_cylinder) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place the soft object (white_3D_cylinder) in the box
    robot.pick(object2)
    robot.place(object2, box)
    
    # 2. Fold the foldable object (white_3D_cuboid)
    robot.fold(object1)
    
    # 3. Place the foldable object (white_3D_cuboid) in the box
    robot.pick(object1)
    robot.place(object1, box)
    
    # 4. Place the rigid and fragile object (green_3D_cylinder) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The soft object (white_3D_cylinder) is placed first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # - The foldable object (white_3D_cuboid) is folded before placing it in the box.
    # - The rigid and fragile object (green_3D_cylinder) is placed last to ensure the soft object is already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True  # Already in the box initially
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
