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
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
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
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
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
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', is_foldable=True, is_fragile=True, in_box=True, out_box=False)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', in_box_objects=[])

### 3. Notes:
# The initial state is defined based on the input images. Each object has specific properties and initial positions (in_box or out_box).
# The white_box (index 5) is a container and does not have any predicates or initial pose other than being a box.
# The objects have been initialized with their respective properties and initial states as per the given information.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', is_foldable=True, is_fragile=True, in_box=True, out_box=False)
    object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[])

    # Goal state
    goal_state = {
        0: True,  # red_3D_polyhedron in_box
        1: True,  # yellow_3D_cylinder in_box
        2: True,  # green_2D_circle in_box
        3: True,  # white_2D_loop in_box
        4: True,  # black_1D_line in_box
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the rigid objects (object1 and object2).
    # 3. Pick and place the elastic object (object3).
    # 4. Ensure the foldable and fragile object (object4) remains in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object0) first to satisfy the rule that soft objects should be in the box before placing rigid or fragile objects.
    # - Placed the rigid objects (object1 and object2) after the soft object.
    # - Placed the elastic object (object3) last.
    # - The foldable and fragile object (object4) was already in the box and remained there.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True

    print("All task planning is done")
