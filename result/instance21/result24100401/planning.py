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
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj in bin.in_bin_objects:
            self.state_handempty()
            obj.in_bin = False
            bin.in_bin_objects.remove(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_fragile=False, is_plastic=False, is_rigid=True, is_heavy=False, is_large=False)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_fragile=False, is_plastic=False, is_rigid=False, is_heavy=False, is_large=False)
object2 = Object(index=2, name='blue_3D_polyhedron', color='blue', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_fragile=False, is_plastic=True, is_rigid=False, is_heavy=False, is_large=False)
object3 = Object(index=3, name='green_3D_cuboid', color='green', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_fragile=True, is_plastic=False, is_rigid=True, is_heavy=False, is_large=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_circle) before placing it in the box.
    # 2. Place the foldable object (white_2D_circle) in the box.
    # 3. Place the plastic object (blue_3D_polyhedron) in the box.
    # 4. Place the rigid object (yellow_3D_cylinder) in the box.
    # 5. Place the fragile and rigid object (green_3D_cuboid) in the box.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # 1. Fold the foldable object
    robot.fold(object1, box)
    
    # 2. Place the foldable object in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 3. Place the plastic object in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # 4. Place the rigid object in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 5. Place the fragile and rigid object in the box
    robot.pick(object3, box)
    robot.place(object3, box)

    # Third, after making all actions, fill your reasons according to the rules
    # - Rule 1: The foldable object (white_2D_circle) is folded and placed first.
    # - Rule 2: The plastic object (blue_3D_polyhedron) is placed without being pushed or folded.
    # - Rule 3: The foldable object (white_2D_circle) is folded before being placed.
    # - Rule 4: No compressible objects are pushed as per the rules.

    # Finally, add this code    
    print("All task planning is done")
