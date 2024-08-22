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
    is_rigid: bool
    is_soft: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_soft=False, is_elastic=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_soft=True, is_elastic=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_soft=True, is_elastic=True,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_soft=False, is_elastic=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': False, 'out_box': True},
        3: {'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }
    
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before rigid objects if there are any soft objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Place soft objects first
    robot.pick(object1)
    robot.place(object1, box)
    
    robot.pick(object2)
    robot.place(object2, box)
    
    # Place rigid object
    robot.pick(object0)
    robot.place(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed soft objects (object1 and object2) before the rigid object (object0) as per the rule.
    # 2. No foldable objects, so no folding action required.
    # 3. No push action required as per the goal state.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
