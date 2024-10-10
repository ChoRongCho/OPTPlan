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
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_2D: bool
    is_3D: bool

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
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_bin = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.in_bin and not obj.pushed:
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
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=True, is_plastic=False, is_rigid=False, is_2D=True, is_3D=False)
object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_rigid=False, is_2D=False, is_3D=True)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=False, is_rigid=True, is_2D=False, is_3D=True)
object3 = Object(index=3, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=True, is_rigid=False, is_2D=False, is_3D=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_circle) before placing it in the box.
    # 2. Place the compressible object (brown_3D_cuboid) in the box first.
    # 3. Place the rigid object (yellow_3D_cylinder) after the compressible object.
    # 4. Place the plastic object (green_1D_line) in the box without pushing or folding.
    
    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the foldable object
    robot.fold(object0, box)
    
    # Pick and place the compressible object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Pick and place the foldable object
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the rigid object
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Pick and place the plastic object
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Third, after making all actions, fill your reasons according to the rules
    # 1. The white_2D_circle was folded before placing it in the box as per rule 3.
    # 2. The brown_3D_cuboid, being compressible, was placed first in the box as per rule 1.
    # 3. The yellow_3D_cylinder, being rigid, was placed after the compressible object as per rule 1.
    # 4. The green_1D_line, being plastic, was placed without pushing or folding as per rule 2.
    
    # Finally, add this code    
    print("All task planning is done")
