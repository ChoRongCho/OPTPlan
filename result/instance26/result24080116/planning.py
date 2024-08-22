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
    is_foldable: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True


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
            obj.in_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if obj.in_box and not self.robot_handempty:
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.append(obj.index)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        if obj.index in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj.index)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='white_3D_cuboid', 
    color='white', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_rigid=True, 
    is_fragile=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    is_foldable=True, 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {"in_box": False, "out_box": True, "is_soft": True},
        "object1": {"in_box": False, "out_box": True, "is_rigid": True, "is_fragile": True},
        "object2": {"in_box": False, "out_box": True, "is_elastic": True},
        "object3": {"in_box": False, "out_box": True, "is_foldable": True, "is_rigid": True},
        "object4": {"in_box": True, "out_box": False}  # This is the box
    }

    # Goal state
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the foldable object (object3) after folding it.
    # 3. Pick and place the elastic object (object2).
    # 4. Pick and place the rigid and fragile object (object1).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Pick and place the soft object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)

    # 2. Fold and place the foldable object (object3)
    robot.fold(object3, box)
    robot.pick(object3, box)
    robot.place(object3, box)

    # 3. Pick and place the elastic object (object2)
    robot.pick(object2, box)
    robot.place(object2, box)

    # 4. Pick and place the rigid and fragile object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # - Placed the soft object (object0) first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # - Folded the foldable object (object3) before placing it in the box.
    # - Placed the elastic object (object2) without any special conditions.
    # - Placed the rigid and fragile object (object1) last to ensure the soft object was already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    # Don't include a box in the goal state. Only express objects.

    print("All task planning is done")
