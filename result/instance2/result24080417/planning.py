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
    is_elastic: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='blue_2D_loop', 
    color='blue', 
    shape='2D_loop', 
    object_type='obj', 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='white_2D_loop', 
    color='white', 
    shape='2D_loop', 
    object_type='obj', 
    is_elastic=True, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box_objects=[2], 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'black_3D_cylinder', 'shape': '3D_cylinder', 'color': 'black', 'predicates': ['is_rigid'], 'init_pose': 'out_box'},
        1: {'name': 'blue_2D_loop', 'shape': '2D_loop', 'color': 'blue', 'predicates': [], 'init_pose': 'out_box'},
        2: {'name': 'white_2D_loop', 'shape': '2D_loop', 'color': 'white', 'predicates': ['is_elastic'], 'init_pose': 'in_box'},
        3: {'name': 'white_box', 'shape': 'box', 'color': 'white', 'predicates': [], 'init_pose': 'box'}
    }

    goal_state = {
        0: {'name': 'black_3D_cylinder', 'shape': '3D_cylinder', 'color': 'black', 'predicates': ['is_rigid'], 'goal_pose': 'in_box'},
        1: {'name': 'blue_2D_loop', 'shape': '2D_loop', 'color': 'blue', 'predicates': [], 'goal_pose': 'in_box'},
        2: {'name': 'white_2D_loop', 'shape': '2D_loop', 'color': 'white', 'predicates': ['is_elastic'], 'goal_pose': 'in_box'},
        3: {'name': 'white_box', 'shape': 'box', 'color': 'white', 'predicates': [], 'goal_pose': 'box'}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Ensure the soft object (white_2D_loop) is already in the box.
    # 2. Place the blue_2D_loop in the box.
    # 3. Place the black_3D_cylinder in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place blue_2D_loop in the box
    robot.pick(object1)
    robot.place(object1, box)

    # Place black_3D_cylinder in the box
    robot.pick(object0)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The white_2D_loop (soft object) is already in the box, satisfying the rule for placing rigid objects.
    # 2. The blue_2D_loop is placed in the box first, followed by the black_3D_cylinder, ensuring the order of operations is correct.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True

    print("All task planning is done")
