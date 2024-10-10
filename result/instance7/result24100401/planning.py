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
    is_bendable: bool
    is_compressible: bool
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
        # Preconditions: Object is bendable, robot hand is empty
        if obj.is_bendable and self.robot_handempty:
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
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_bendable=True, is_compressible=False, is_plastic=False, is_fragile=False, is_rigid=False, is_heavy=False, is_large=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_bendable=False, is_compressible=True, is_plastic=False, is_fragile=False, is_rigid=False, is_heavy=False, is_large=False)
object2 = Object(index=2, name='blue_2D_triangle', color='blue', shape='2D_triangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_bendable=False, is_compressible=False, is_plastic=True, is_fragile=False, is_rigid=False, is_heavy=False, is_large=False)
object3 = Object(index=3, name='green_3D_cuboid', color='green', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_bendable=False, is_compressible=False, is_plastic=False, is_fragile=True, is_rigid=True, is_heavy=False, is_large=False)
object4 = Object(index=4, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_bendable=False, is_compressible=False, is_plastic=False, is_fragile=False, is_rigid=True, is_heavy=False, is_large=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the bendable object (black_1D_line) before placing it in the box.
    # 2. Place the compressible object (yellow_3D_cuboid) in the box first.
    # 3. Place the plastic object (blue_2D_triangle) in the box.
    # 4. Place the fragile and rigid objects (green_3D_cuboid and yellow_3D_cylinder) in the box.
    # 5. Push the compressible object (yellow_3D_cuboid) after placing all items in the box.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the bendable object
    robot.fold(object0, box)
    
    # Pick and place the compressible object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Pick and place the plastic object
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Pick and place the fragile and rigid objects
    robot.pick(object3, box)
    robot.place(object3, box)
    
    robot.pick(object4, box)
    robot.place(object4, box)
    
    # Push the compressible object
    robot.push(object1, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded the bendable object (black_1D_line) before placing it in the box as per rule 3.
    # 2. Placed the compressible object (yellow_3D_cuboid) first to satisfy rule 1.
    # 3. Placed the plastic object (blue_2D_triangle) without folding or pushing as per rule 2.
    # 4. Placed the fragile and rigid objects (green_3D_cuboid and yellow_3D_cylinder) after the compressible object.
    # 5. Pushed the compressible object (yellow_3D_cuboid) after placing all items in the box as per rule 4.

    # Finally, add this code    
    print("All task planning is done")
