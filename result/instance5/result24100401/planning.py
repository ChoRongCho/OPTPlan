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
    is_fragile: bool
    is_plastic: bool
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
        # Preconditions: Robot hand must be empty, object must be compressible
        if self.robot_handempty and obj.is_compressible:
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
object0 = Object(index=0, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_fragile=False, is_plastic=True, is_rigid=False, is_heavy=False, is_large=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_fragile=False, is_plastic=False, is_rigid=True, is_heavy=False, is_large=False)
object2 = Object(index=2, name='green_3D_cuboid', color='green', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_fragile=True, is_plastic=False, is_rigid=True, is_heavy=False, is_large=False)
object3 = Object(index=3, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_fragile=False, is_plastic=False, is_rigid=False, is_heavy=False, is_large=False)
object4 = Object(index=4, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_fragile=False, is_plastic=False, is_rigid=True, is_heavy=False, is_large=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the compressible object (white_3D_cylinder) before placing it in the bin.
    # 2. Place the folded compressible object (white_3D_cylinder) in the bin.
    # 3. Place the fragile object (green_3D_cuboid) in the bin after the compressible object.
    # 4. Place the rigid object (black_3D_cylinder) in the bin.
    # 5. Place the rigid object (yellow_3D_cylinder) in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the compressible object
    robot.fold(object3, box)
    
    # Place the folded compressible object in the bin
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Place the fragile object in the bin
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Place the rigid object (black_3D_cylinder) in the bin
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Place the rigid object (yellow_3D_cylinder) in the bin
    robot.pick(object4, box)
    robot.place(object4, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. The white_3D_cylinder is compressible, so it was folded before placing it in the bin.
    # 2. The green_3D_cuboid is fragile, so it was placed after the compressible object.
    # 3. The black_3D_cylinder and yellow_3D_cylinder are rigid, so they were placed after the compressible object.
    # 4. The green_1D_line is plastic, so it was not pushed or folded.

    # Finally, add this code    
    print("All task planning is done")
