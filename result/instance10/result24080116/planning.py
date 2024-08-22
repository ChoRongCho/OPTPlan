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
    is_soft: bool
    is_rigid: bool
    is_elastic: bool
    is_fragile: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
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
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.out_box:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
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
object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, is_fragile=False, in_box=False, out_box=True)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, is_fragile=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, is_fragile=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, is_fragile=False, in_box=False, out_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=False, is_fragile=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain based on the given input images.
# Each object is initialized with its properties and predicates.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'in_box' and 'out_box' predicates are set according to the 'init_pose' from the input.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, is_fragile=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, is_fragile=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, is_fragile=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, is_fragile=False, in_box=False, out_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=False, is_fragile=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        object0: {'in_box': True, 'out_box': False},
        object1: {'in_box': True, 'out_box': False},
        object2: {'in_box': True, 'out_box': False},
        object3: {'in_box': True, 'out_box': False},
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object3) first.
    # 2. Pick and place the remaining objects (object0, object1, object2).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object3, box)
    robot.place(object3, box)
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (object3) first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # 2. Placed the remaining objects (object0, object1, object2) after the soft object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    print("All task planning is done")