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
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=True, 
    is_rigid=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=False, 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        'object0': {
            'in_box': False,
            'out_box': True,
            'is_fragile': False,
            'is_rigid': True
        },
        'object1': {
            'in_box': False,
            'out_box': True,
            'is_fragile': True,
            'is_rigid': False
        },
        'object2': {
            'in_box': True,
            'out_box': False,
            'in_bin_objects': []
        }
    }

    goal_state = {
        'object0': {
            'in_box': True,
            'out_box': False
        },
        'object1': {
            'in_box': True,
            'out_box': False
        },
        'object2': {
            'in_box': True,
            'out_box': False,
            'in_bin_objects': [0, 1]
        }
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the rigid object (object0) in the box.
    # 2. Place the fragile object (object1) in the box.
    # 3. Ensure that object2 (the box) contains both object0 and object1.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # Action sequence
    # 1. Place the rigid object (object0) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # 2. Place the fragile object (object1) in the box
    robot.pick(object1)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The rigid object (object0) is placed first as there are no soft objects to place before it.
    # - The fragile object (object1) is placed after the rigid object (object0) as per the rules.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [0, 1]

    print("All task planning is done")
