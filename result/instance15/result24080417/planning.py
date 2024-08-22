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
    is_soft: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_elastic=True, is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_elastic=True, is_soft=True, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', in_box=False, out_box=True)
object3 = Object(index=3, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', is_soft=True, in_box=True, out_box=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_fragile=True, is_rigid=True, in_box=True, out_box=False)
object5 = Object(index=5, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=True, out_box=False)
object6 = Object(index=6, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[3, 4, 5], in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': False, 'out_box': True},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False},
        5: {'in_box': True, 'out_box': False},
        6: {'in_box': True, 'out_box': False, 'in_bin_objects': [3, 4, 5]}
    }

    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False},
        5: {'in_box': True, 'out_box': False},
        6: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3, 4, 5]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy: Place soft objects first, then place fragile/rigid objects

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object6

    # c) Action sequence
    # Place soft objects first
    robot.pick(object0)
    robot.place(object0, box)
    robot.pick(object1)
    robot.place(object1, box)

    # Place remaining objects
    robot.pick(object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: Soft objects (object0, object1) are placed first as per the rule before placing any fragile/rigid objects.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_box == True
    assert object6.in_bin_objects == [0, 1, 2, 3, 4, 5]

    print("All task planning is done")
