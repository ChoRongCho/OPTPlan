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
    is_soft: bool = False
    is_elastic: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True, 'is_soft': True, 'is_rigid': False},
        1: {'in_box': False, 'out_box': True, 'is_soft': False, 'is_rigid': True},
        2: {'in_box': False, 'out_box': True, 'is_soft': False, 'is_rigid': False, 'is_elastic': True},
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
    # 1. Place soft objects before rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(object0, box)
    
    # 2. Place the elastic object (object2) in the box
    robot.place(object2, box)
    
    # 3. Place the rigid object (object1) in the box
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed object0 first because it is soft.
    # - Placed object2 next because it is elastic and not rigid.
    # - Placed object1 last because it is rigid.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    
    # Check if the box contains all objects
    assert set(box.in_bin_objects) == {0, 1, 2}
    
    print("All task planning is done")
