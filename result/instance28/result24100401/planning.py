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
    is_plastic: bool
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_heavy: bool
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
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=False, is_fragile=True, is_rigid=True, is_heavy=False, is_stable=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=False, is_fragile=False, is_rigid=True, is_heavy=False, is_stable=False)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=False, is_fragile=False, is_rigid=True, is_heavy=False, is_stable=False)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=True, is_plastic=False, is_fragile=False, is_rigid=False, is_heavy=False, is_stable=False)
object4 = Object(index=4, name='blue_3D_polyhedron', color='blue', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_foldable=False, is_plastic=True, is_fragile=False, is_rigid=False, is_heavy=False, is_stable=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (transparent_2D_circle) before placing it in the box.
    # 2. Place the foldable object (transparent_2D_circle) in the box.
    # 3. Place the plastic object (blue_3D_polyhedron) in the box.
    # 4. Place the fragile object (green_3D_cylinder) in the box.
    # 5. Place the remaining rigid objects (black_3D_cylinder and yellow_3D_cylinder) in the box.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=5, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the foldable object
    robot.fold(object3, box)
    
    # Place the foldable object in the box
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Place the plastic object in the box
    robot.pick(object4, box)
    robot.place(object4, box)
    
    # Place the fragile object in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Place the remaining rigid objects in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded the transparent_2D_circle because it is foldable (Rule 3).
    # 2. Placed the transparent_2D_circle first because it is foldable and should be folded before placing (Rule 3).
    # 3. Placed the blue_3D_polyhedron next because it is plastic and should not be pushed or folded (Rule 2).
    # 4. Placed the green_3D_cylinder after the foldable object because it is fragile (Rule 1).
    # 5. Placed the black_3D_cylinder and yellow_3D_cylinder last as they are rigid and not fragile (Rule 1).

    # Finally, add this code    
    print("All task planning is done")
