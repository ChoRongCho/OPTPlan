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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_placed: bool
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
            obj.in_bin = True
            self.state_handempty()
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
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=True, is_placed=False, is_stable=False)
object1 = Object(index=1, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_placed=False, is_stable=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_placed=False, is_stable=False)
object3 = Object(index=3, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_placed=False, is_stable=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_circle) before placing it in the bin.
    # 2. Place the compressible objects (brown_3D_cylinder, red_3D_polyhedron, brown_3D_cuboid) in the bin first.
    # 3. Place the folded white_2D_circle in the bin.
    # 4. Ensure all objects are stable and placed in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the foldable object
    robot.fold(object0, box)  # Fold white_2D_circle

    # Place compressible objects first
    robot.pick(object1, box)  # Pick brown_3D_cylinder
    robot.place(object1, box)  # Place brown_3D_cylinder in bin

    robot.pick(object2, box)  # Pick red_3D_polyhedron
    robot.place(object2, box)  # Place red_3D_polyhedron in bin

    robot.pick(object3, box)  # Pick brown_3D_cuboid
    robot.place(object3, box)  # Place brown_3D_cuboid in bin

    # Place the folded object
    robot.pick(object0, box)  # Pick white_2D_circle
    robot.place(object0, box)  # Place white_2D_circle in bin

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded the white_2D_circle before placing it in the bin as it is foldable.
    # 2. Placed all compressible objects in the bin before placing the rigid object.
    # 3. Followed the rule to not push or fold plastic objects.
    # 4. Ensured all objects are placed and stable in the bin.

    # Finally, add this code    
    print("All task planning is done")
