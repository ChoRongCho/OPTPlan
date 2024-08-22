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
    is_elastic: bool
    is_soft: bool
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if obj.out_box and self.robot_handempty:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj.index)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        if obj.in_box and self.robot_handempty:
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj.index)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_soft=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_soft=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_soft=True,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='yellow_3D_polyhedron', color='yellow', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=True, is_soft=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[2, 3], is_rigid=False, is_elastic=False, is_soft=False,
    in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {"in_box": False, "out_box": True},
        "object1": {"in_box": False, "out_box": True},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_bin_objects": [2, 3]}
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_bin_objects": [0, 1, 2, 3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place object1 (soft) into the box.
    # 2. Pick and place object0 (rigid) into the box.
    # 3. Pick and place object1 (soft) into the box.
    # 4. Pick and place object2 (soft) into the box.
    # 5. Pick and place object3 (rigid) into the box.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # Action sequence
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Pick and place object1 (soft) into the box to satisfy the rule that soft objects should be in the box before placing rigid objects.
    # 2. Pick and place object0 (rigid) into the box after ensuring soft objects are in the box.
    # 3. Pick and place object2 (soft) into the box to ensure all soft objects are in the box.
    # 4. Pick and place object3 (rigid) into the box after ensuring all soft objects are in the box.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
