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
object0 = Object(index=0, name='blue_3D_polyhedron', color='blue', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=True, is_rigid=False, is_heavy=False, is_fragile=False)
object1 = Object(index=1, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_plastic=False, is_rigid=False, is_heavy=False, is_fragile=False)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=False, is_rigid=True, is_heavy=False, is_fragile=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the brown_3D_cylinder since it is compressible.
    # 2. Place the folded brown_3D_cylinder in the box.
    # 3. Place the yellow_3D_cylinder in the box since it is rigid and a compressible object is already in the box.
    # 4. Place the blue_3D_polyhedron in the box since it is plastic and does not require any preconditions.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # c) Action sequence
    # Fold the brown_3D_cylinder
    robot.fold(object1, box)
    
    # Pick and place the brown_3D_cylinder in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Pick and place the yellow_3D_cylinder in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Pick and place the blue_3D_polyhedron in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: The brown_3D_cylinder is compressible and is placed first in the box.
    # Rule 2: The blue_3D_polyhedron is plastic and is placed without folding or pushing.
    # Rule 3: The brown_3D_cylinder is foldable and is folded before placing.
    # Rule 4: No pushing is required as all objects are placed correctly.

    # Finally, add this code    
    print("All task planning is done")
