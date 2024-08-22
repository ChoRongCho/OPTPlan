from dataclasses import dataclass
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
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: List[int]
    
    # Object physical properties 
    is_elastic: bool
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_rigid=True, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=True, is_rigid=True, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_rigid=False, init_pose='out_box', in_box=False)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=False, is_rigid=False, init_pose='in_box', in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_rigid=False, init_pose='box', in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'yellow_3D_cylinder', 'in_box': False},
        1: {'name': 'green_3D_cylinder', 'in_box': False},
        2: {'name': 'blue_2D_loop', 'in_box': False},
        3: {'name': 'white_2D_loop', 'in_box': True},
        4: {'name': 'white_box', 'in_box': False, 'in_bin_objects': []}
    }
    
    goal_state = {
        0: {'name': 'yellow_3D_cylinder', 'in_box': True},
        1: {'name': 'green_3D_cylinder', 'in_box': True},
        2: {'name': 'blue_2D_loop', 'in_box': True},
        3: {'name': 'white_2D_loop', 'in_box': True},
        4: {'name': 'white_box', 'in_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the blue_2D_loop (soft object) in the box first.
    # 2. Place the yellow_3D_cylinder (rigid object) in the box.
    # 3. Place the green_3D_cylinder (fragile object) in the box.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # c) Action sequence
    # Place blue_2D_loop in the box
    robot.pick(object2)
    robot.place(object2, box)
    
    # Place yellow_3D_cylinder in the box
    robot.pick(object0)
    robot.place(object0, box)
    
    # Place green_3D_cylinder in the box
    robot.pick(object1)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The blue_2D_loop is a soft object and should be placed in the box first.
    # 2. The yellow_3D_cylinder is a rigid object and can be placed after the soft object.
    # 3. The green_3D_cylinder is a fragile object and can be placed after the soft object.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
