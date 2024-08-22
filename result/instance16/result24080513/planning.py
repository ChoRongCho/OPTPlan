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
    is_fragile: bool
    is_soft: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=True,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=True,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=True,
    in_box=False, out_box=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': False, 'out_box': True},
        3: {'in_box': False, 'out_box': True},
        4: {'in_box': True, 'out_box': False}
    }
    
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # Action sequence
    # 1. Place the soft object (object1) in the box first
    robot.place(object1, box)
    
    # 2. Place the fragile object (object0) in the box
    robot.place(object0, box)
    
    # 3. Place the rigid object (object2) in the box
    robot.place(object2, box)
    
    # 4. Place the remaining object (object3) in the box
    robot.place(object3, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - object1 (soft) is placed first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # - object0 (fragile) is placed next.
    # - object2 (rigid) is placed after the fragile object.
    # - object3 is placed last as it does not have any specific constraints.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    
    print("All task planning is done")
