from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # physical state of an object
    pushed: bool
    folded: bool
    in_bin: bool
    
    # Object physical properties 
    is_compressible: bool
    is_foldable: bool
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_heavy: bool
    is_stable: bool

@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str
    
    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list


class Robot:
    def __init__(self, name: str = "OpenManipulator", goal: str = None, actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False

    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    def state_base(self):
        self.robot_base_pose = True

    def pick(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must not be in bin
        if self.robot_handempty and not obj.in_bin:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_bin = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be in bin
        if self.robot_handempty and obj.in_bin:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: Object must be in bin
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=False, 
    is_compressible=False, 
    is_foldable=False, 
    is_fragile=True, 
    is_rigid=True, 
    is_heavy=False, 
    is_stable=False
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=False, 
    is_compressible=True, 
    is_foldable=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_heavy=False, 
    is_stable=False
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=False, 
    is_compressible=False, 
    is_foldable=True, 
    is_fragile=False, 
    is_rigid=False, 
    is_heavy=False, 
    is_stable=False
)

object3 = Object(
    index=3, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=False, 
    is_compressible=False, 
    is_foldable=True, 
    is_fragile=False, 
    is_rigid=False, 
    is_heavy=False, 
    is_stable=False
)

box = Box(
    index=0, 
    name='box', 
    object_type='box', 
    in_bin_objects=[]
)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold all foldable objects before placing them in the box.
    # 2. Place the compressible object first to satisfy the rule for fragile/rigid objects.
    # 3. Place the remaining objects in the box.
    # 4. Push the compressible object after placing all items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # c) Action sequence
    # Fold the foldable objects
    robot.fold(object2, box)  # Fold transparent_2D_circle
    robot.fold(object3, box)  # Fold yellow_2D_rectangle

    # Place the compressible object first
    robot.pick(object1, box)  # Pick white_3D_cylinder
    robot.place(object1, box)  # Place white_3D_cylinder in box

    # Place the folded objects
    robot.pick(object2, box)  # Pick transparent_2D_circle
    robot.place(object2, box)  # Place transparent_2D_circle in box

    robot.pick(object3, box)  # Pick yellow_2D_rectangle
    robot.place(object3, box)  # Place yellow_2D_rectangle in box

    # Place the fragile/rigid object
    robot.pick(object0, box)  # Pick green_3D_cylinder
    robot.place(object0, box)  # Place green_3D_cylinder in box

    # Push the compressible object
    robot.push(object1, box)  # Push white_3D_cylinder

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded transparent_2D_circle and yellow_2D_rectangle before placing them in the box as they are foldable.
    # 2. Placed white_3D_cylinder first because it is compressible, satisfying the rule for placing fragile/rigid objects.
    # 3. Placed green_3D_cylinder after the compressible object was in the box.
    # 4. Pushed white_3D_cylinder after all items were placed in the bin.

    # Finally, add this code    
    print("All task planning is done")
