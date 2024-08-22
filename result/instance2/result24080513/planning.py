from dataclasses import dataclass

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
    in_bin_objects: list
    
    # Object physical properties 
    is_foldable: bool
    is_rigid: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_2D_loop', 
    color='white', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=True, 
    is_elastic=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=True, 
    is_rigid=False, 
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
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_elastic=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": object0,  # white_2D_loop, out_box
        "object1": object1,  # black_3D_cylinder, out_box
        "object2": object2,  # black_2D_loop, in_box
        "object3": object3   # white_box, box
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": False, "out_box": False}  # box itself, no change needed
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the white_2D_loop (soft object) in the box.
    # 2. Place the black_3D_cylinder (rigid object) in the box.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Place white_2D_loop in the box
    robot.pick(object0)
    robot.place(object0, box)
    
    # Place black_3D_cylinder in the box
    robot.pick(object1)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The white_2D_loop is a soft object and should be placed in the box before placing the rigid object.
    # 2. The black_3D_cylinder is a rigid object and can be placed after the soft object is in the box.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == False  # The box itself should not be in another box
    
    print("All task planning is done")
