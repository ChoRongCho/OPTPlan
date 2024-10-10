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
    is_plastic: bool
    is_rigid: bool
    
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
        # Preconditions: Object is not in the bin, robot hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Effects: Robot is holding the object, object is not in the bin
            self.state_holding(obj)
            obj.in_bin = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Effects: Object is in the bin, robot hand is empty
            bin.in_bin_objects.append(obj)
            obj.in_bin = True
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
        # Preconditions: Object is not in the bin, robot hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object is in the bin
        if obj in bin.in_bin_objects:
            # Effects: Object is removed from the bin, robot hand is empty
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_plastic=True, is_rigid=False, is_heavy=False, is_fragile=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False, is_fragile=False)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False, is_fragile=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold any foldable objects before placing them in the box.
    # 2. Place the compressible object first if available.
    # 3. Place rigid objects after compressible objects.
    # 4. Do not push or fold plastic objects.
    # 5. Push compressible objects after placing all items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # 1. Fold the green_1D_line (if it were foldable, but it's not in this case)
    # 2. Place the green_1D_line (compressible object) in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # 3. Place the black_3D_cylinder (rigid object) in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # 4. Place the yellow_3D_cylinder (rigid object) in the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # Third, after making all actions, fill your reasons according to the rules
    # - Rule 1: The green_1D_line is a compressible object and is placed first.
    # - Rule 2: No plastic objects are pushed or folded.
    # - Rule 3: No foldable objects are present.
    # - Rule 4: No compressible objects are pushed after placing items in the bin.

    # Finally, add this code    
    print("All task planning is done")
