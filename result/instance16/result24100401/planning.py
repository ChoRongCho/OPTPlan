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
    is_plastic: bool
    is_compressible: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning
    is_out_box: bool
    is_placed: bool

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
            obj.is_placed = True
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
        # Preconditions: Object is foldable, robot hand is empty
        if obj.is_foldable and self.robot_handempty:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: Object is in the bin
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
object0 = Object(index=0, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_bendable=False, is_plastic=True, is_compressible=False, is_rigid=False, is_out_box=True, is_placed=False)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_bendable=False, is_plastic=False, is_compressible=False, is_rigid=True, is_out_box=True, is_placed=False)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_bendable=False, is_plastic=False, is_compressible=False, is_rigid=False, is_out_box=True, is_placed=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_bendable=False, is_plastic=False, is_compressible=True, is_rigid=False, is_out_box=True, is_placed=False)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_bendable=True, is_plastic=False, is_compressible=False, is_rigid=False, is_out_box=True, is_placed=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_loop) before placing it in the bin.
    # 2. Place the compressible object (brown_3D_cylinder) first in the bin.
    # 3. Place the rigid object (yellow_3D_cylinder) after the compressible object.
    # 4. Place the bendable object (black_1D_line) in the bin.
    # 5. Place the plastic object (green_1D_line) in the bin.
    # 6. Push the compressible object after placing all items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the foldable object
    robot.fold(object2, box)
    
    # Place the compressible object first
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Place the rigid object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Place the bendable object
    robot.pick(object4, box)
    robot.place(object4, box)
    
    # Place the plastic object
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Place the foldable object after folding
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Push the compressible object
    robot.push(object3, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. The foldable object (white_2D_loop) was folded before placing it in the bin.
    # 2. The compressible object (brown_3D_cylinder) was placed first in the bin.
    # 3. The rigid object (yellow_3D_cylinder) was placed after the compressible object.
    # 4. The bendable object (black_1D_line) was placed in the bin.
    # 5. The plastic object (green_1D_line) was placed in the bin without being pushed or folded.
    # 6. The compressible object (brown_3D_cylinder) was pushed after all items were placed in the bin.

    # Finally, add this code    
    print("All task planning is done")
