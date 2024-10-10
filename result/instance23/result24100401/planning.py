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
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_heavy: bool
    is_large: bool

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
        if self.robot_handempty and not obj.in_bin:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_bin = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.in_bin:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable and not obj.folded:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_plastic=False, is_fragile=False, is_rigid=False, is_heavy=False, is_large=False)
object1 = Object(index=1, name='green_3D_cuboid', color='green', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=False, is_fragile=True, is_rigid=True, is_heavy=False, is_large=False)
object2 = Object(index=2, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=True, is_fragile=False, is_rigid=False, is_heavy=False, is_large=False)
object3 = Object(index=3, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_plastic=False, is_fragile=False, is_rigid=False, is_heavy=False, is_large=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold all foldable objects before placing them in the bin.
    # 2. Place compressible objects first if available.
    # 3. Place fragile or rigid objects after compressible objects.
    # 4. Do not push or fold plastic objects.
    # 5. Push compressible objects after placing all items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold foldable objects
    robot.fold(object0, box)  # Fold yellow_2D_rectangle
    robot.fold(object3, box)  # Fold blue_2D_loop

    # Place compressible objects first
    robot.pick(object0, box)
    robot.place(object0, box)

    robot.pick(object3, box)
    robot.place(object3, box)

    # Place fragile or rigid objects
    robot.pick(object1, box)
    robot.place(object1, box)

    # Place plastic objects
    robot.pick(object2, box)
    robot.place(object2, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded yellow_2D_rectangle and blue_2D_loop before placing them in the bin as they are foldable.
    # 2. Placed yellow_2D_rectangle and blue_2D_loop first as they are compressible.
    # 3. Placed green_3D_cuboid after compressible objects as it is fragile and rigid.
    # 4. Placed green_1D_line as it is plastic and not foldable or pushable.
    # 5. Did not push any objects as per the rules.

    # Finally, add this code    
    print("All task planning is done")
