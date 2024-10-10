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
    is_bendable: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_in_position: bool
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
        # Preconditions: Robot hand must be empty, object must not be in bin, object must be in position
        if self.robot_handempty and not obj.in_bin and obj.is_in_position:
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
object0 = Object(index=0, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_bendable=False, is_rigid=True, is_in_position=False, is_stable=False)
object1 = Object(index=1, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_bendable=False, is_rigid=False, is_in_position=False, is_stable=False)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_bendable=False, is_rigid=False, is_in_position=False, is_stable=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_bendable=False, is_rigid=False, is_in_position=False, is_stable=False)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_bendable=True, is_rigid=False, is_in_position=False, is_stable=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold all foldable objects before placing them in the box.
    # 2. Place foldable objects in the box.
    # 3. Place the bendable object in the box.
    # 4. Place the rigid object in the box.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Fold all foldable objects
    robot.fold(object1, box)  # Fold blue_2D_loop
    robot.fold(object2, box)  # Fold white_2D_loop
    robot.fold(object3, box)  # Fold yellow_2D_rectangle

    # Place foldable objects in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    robot.pick(object2, box)
    robot.place(object2, box)

    robot.pick(object3, box)
    robot.place(object3, box)

    # Place the bendable object in the box
    robot.pick(object4, box)
    robot.place(object4, box)

    # Place the rigid object in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Foldable objects (blue_2D_loop, white_2D_loop, yellow_2D_rectangle) were folded before placing them in the box as per rule 3.
    # 2. The bendable object (black_1D_line) was placed in the box before the rigid object (gray_1D_line) as per rule 1.
    # 3. No plastic objects were pushed or folded as per rule 2.
    # 4. No compressible objects were pushed after placing items in the bin as per rule 4.

    # Finally, add this code    
    print("All task planning is done")
