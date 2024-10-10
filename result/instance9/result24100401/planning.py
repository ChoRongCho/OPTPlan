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
    is_foldable: bool
    is_plastic: bool
    is_bendable: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_heavy: bool
    is_fragile: bool

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
        # Preconditions: Robot hand must be empty, object must not be in the bin
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
        # Preconditions: Robot hand must be empty, object must be in the bin
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
        # Preconditions: Object must be in the bin
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
object0 = Object(index=0, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_plastic=False, is_bendable=False, is_heavy=False, is_fragile=False)
object1 = Object(index=1, name='blue_3D_polyhedron', color='blue', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=True, is_bendable=False, is_heavy=False, is_fragile=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=False, is_bendable=True, is_heavy=False, is_fragile=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_plastic=False, is_bendable=False, is_heavy=False, is_fragile=False)
object4 = Object(index=4, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=True, is_bendable=False, is_heavy=False, is_fragile=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold all foldable objects before placing them in the bin.
    # 2. Place foldable objects in the bin.
    # 3. Place compressible (bendable) objects in the bin.
    # 4. Place non-compressible objects in the bin if no compressible objects are available.
    # 5. Push compressible objects after placing items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold foldable objects
    robot.fold(object0, box)  # Fold white_2D_loop
    robot.fold(object3, box)  # Fold white_2D_circle

    # Place foldable objects in the bin
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object3, box)
    robot.place(object3, box)

    # Place compressible (bendable) objects in the bin
    robot.pick(object2, box)
    robot.place(object2, box)

    # Place non-compressible objects in the bin if no compressible objects are available
    robot.pick(object4, box)
    robot.place(object4, box)

    # Push compressible objects after placing items in the bin
    robot.push(object2, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded white_2D_loop and white_2D_circle before placing them in the bin as they are foldable.
    # 2. Placed black_1D_line (compressible) in the bin before placing any non-compressible objects.
    # 3. Placed green_1D_line (non-compressible) after placing a compressible object.
    # 4. Pushed black_1D_line after placing all items in the bin.

    # Finally, add this code    
    print("All task planning is done")
