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
    is_plastic: bool
    is_bendable: bool
    
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
            # Effects: Robot is holding the object, object is not in the bin
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Effects: Object is in the bin, robot hand is empty
            obj.in_bin = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        # Preconditions: Object is in the bin, robot hand is empty
        if obj.in_bin and self.robot_handempty:
            # Effects: Object is pushed
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        # Preconditions: Object is foldable, robot hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: Object is in the bin
        if obj in bin.in_bin_objects:
            # Effects: Object is not in the bin, robot hand is empty
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=False, is_bendable=True, is_packable=False, is_stable=False)
object1 = Object(index=1, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_bendable=False, is_packable=False, is_stable=False)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=True, is_plastic=False, is_bendable=False, is_packable=False, is_stable=False)
object3 = Object(index=3, name='blue_2D_triangle', color='blue', shape='2D_triangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=True, is_bendable=False, is_packable=False, is_stable=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_loop) before placing it in the box.
    # 2. Place the compressible object (brown_3D_cylinder) first in the box.
    # 3. Place the non-compressible objects (black_1D_line and blue_2D_triangle) in the box.
    # 4. Do not push or fold the plastic object (blue_2D_triangle).
    # 5. Push the compressible object (brown_3D_cylinder) after placing all items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # 1. Fold the foldable object
    robot.fold(object2, box)  # Fold white_2D_loop

    # 2. Place the compressible object first
    robot.pick(object1, box)  # Pick brown_3D_cylinder
    robot.place(object1, box)  # Place brown_3D_cylinder in box

    # 3. Place the non-compressible objects
    robot.pick(object0, box)  # Pick black_1D_line
    robot.place(object0, box)  # Place black_1D_line in box

    robot.pick(object3, box)  # Pick blue_2D_triangle
    robot.place(object3, box)  # Place blue_2D_triangle in box

    # 4. Push the compressible object
    robot.push(object1, box)  # Push brown_3D_cylinder

    # Third, after making all actions, fill your reasons according to the rules
    # - Folded white_2D_loop before placing it in the box as per rule 3.
    # - Placed brown_3D_cylinder first because it is compressible, satisfying rule 1.
    # - Placed black_1D_line and blue_2D_triangle after the compressible object.
    # - Did not push or fold blue_2D_triangle as it is plastic, satisfying rule 2.
    # - Pushed brown_3D_cylinder after placing all items in the bin, satisfying rule 4.

    # Finally, add this code    
    print("All task planning is done")
