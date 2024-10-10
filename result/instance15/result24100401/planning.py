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
    is_plastic: bool
    is_bendable: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_fragile: bool
    is_heavy: bool

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
        # Preconditions: Robot hand must be empty, object must be bendable
        if self.robot_handempty and obj.is_bendable:
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
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_plastic=False, is_bendable=False, is_fragile=False, is_heavy=False)
object1 = Object(index=1, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=True, is_bendable=False, is_fragile=False, is_heavy=False)
object2 = Object(index=2, name='blue_3D_polyhedron', color='blue', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=True, is_bendable=False, is_fragile=False, is_heavy=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=False, is_bendable=True, is_fragile=False, is_heavy=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the compressible object (brown_3D_cuboid) first as per rule 1.
    # 2. Fold the bendable object (black_1D_line) before placing it as per rule 3.
    # 3. Place the remaining objects (green_1D_line and blue_3D_polyhedron) in the bin.
    # 4. Do not push or fold plastic objects as per rule 2.
    # 5. Push the compressible object after placing all items in the bin as per rule 4.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Place the compressible object first
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fold the bendable object before placing it
    robot.fold(object3, box)
    robot.pick(object3, box)
    robot.place(object3, box)

    # Place the remaining objects
    robot.pick(object1, box)
    robot.place(object1, box)

    robot.pick(object2, box)
    robot.place(object2, box)

    # Push the compressible object after placing all items
    robot.push(object0, box)

    # Third, after making all actions, fill your reasons according to the rules
    # - Rule 1: The compressible object (brown_3D_cuboid) is placed first.
    # - Rule 2: No plastic objects (green_1D_line, blue_3D_polyhedron) are pushed or folded.
    # - Rule 3: The bendable object (black_1D_line) is folded before placing.
    # - Rule 4: The compressible object (brown_3D_cuboid) is pushed after all items are placed.

    # Finally, add this code    
    print("All task planning is done")
