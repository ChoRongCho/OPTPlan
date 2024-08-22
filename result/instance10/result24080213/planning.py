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
    is_fragile: bool = False
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
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_elastic=True, 
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
        "object0": {"in_box": False, "out_box": True},
        "object1": {"in_box": False, "out_box": True},
        "object2": {"in_box": False, "out_box": True},
        "object3": {"in_box": True, "out_box": False}
    }
    
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place a soft object before placing a fragile or rigid object.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Place the soft object first
    robot.pick(object2)
    robot.place(object2, box)
    
    # Place the fragile and rigid object next
    robot.pick(object0)
    robot.place(object0, box)
    
    # Place the elastic object last
    robot.pick(object1)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object2) first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # 2. Placed the fragile and rigid object (object0) next.
    # 3. Placed the elastic object (object1) last.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    
    print("All task planning is done")
