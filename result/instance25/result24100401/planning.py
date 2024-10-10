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
    is_bendable: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_packable: bool
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
        # Preconditions: Object is not in the bin, robot hand is empty
        if not obj.in_bin and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_bin = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        # Preconditions: Object is in the bin, robot hand is empty
        if obj.in_bin and self.robot_handempty:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        # Preconditions: Object is bendable, robot hand is empty
        if obj.is_bendable and self.robot_handempty:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: Object is in the bin
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
object0 = Object(index=0, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_bendable=True, is_rigid=False, is_packable=False, is_stable=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_bendable=False, is_rigid=True, is_packable=False, is_stable=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_bendable=False, is_rigid=False, is_packable=False, is_stable=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (black_1D_line) before placing it in the box.
    # 2. Place the compressible object (red_3D_polyhedron) in the box first.
    # 3. Place the rigid object (black_3D_cylinder) in the box after the compressible object.
    # 4. Place the foldable object (black_1D_line) in the box after folding it.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # 1. Fold the black_1D_line
    robot.fold(object0, box)
    
    # 2. Pick and place the red_3D_polyhedron in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # 3. Pick and place the black_3D_cylinder in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 4. Pick and place the black_1D_line in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Third, after making all actions, fill your reasons according to the rules
    # - Rule 1: The red_3D_polyhedron is compressible and is placed first in the box.
    # - Rule 2: No plastic objects are involved, so no push or fold restrictions apply.
    # - Rule 3: The black_1D_line is foldable and is folded before being placed in the box.
    # - Rule 4: The red_3D_polyhedron is compressible and is placed before any pushing actions, but no push is needed here.

    # Finally, add this code    
    print("All task planning is done")
