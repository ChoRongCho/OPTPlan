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
    is_out_box: bool
    is_ready_for_packing: bool

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
        if self.robot_handempty and not obj.in_bin and obj.is_out_box:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_bin = True
            obj.is_ready_for_packing = True
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
            obj.in_bin = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='blue_3D_polyhedron', color='blue', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=True, is_bendable=False, is_out_box=True, is_ready_for_packing=False)
object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=True, is_plastic=False, is_bendable=False, is_out_box=True, is_ready_for_packing=False)
object2 = Object(index=2, name='transparent_3D_cuboid', color='transparent', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_bendable=False, is_out_box=True, is_ready_for_packing=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=False, is_bendable=True, is_out_box=True, is_ready_for_packing=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_loop) before placing it in the box.
    # 2. Place the compressible object (transparent_3D_cuboid) first in the box.
    # 3. Place the folded object (white_2D_loop) in the box.
    # 4. Place the remaining objects (blue_3D_polyhedron) in the box.
    # 5. Do not push or fold the plastic object (blue_3D_polyhedron).
    # 6. Do not place the bendable object (black_1D_line) in the box as per the goal state.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the foldable object
    robot.fold(object1, box)  # Fold white_2D_loop

    # Place the compressible object first
    robot.pick(object2, box)  # Pick transparent_3D_cuboid
    robot.place(object2, box)  # Place transparent_3D_cuboid in bin

    # Place the folded object
    robot.pick(object1, box)  # Pick white_2D_loop
    robot.place(object1, box)  # Place white_2D_loop in bin

    # Place the remaining object
    robot.pick(object0, box)  # Pick blue_3D_polyhedron
    robot.place(object0, box)  # Place blue_3D_polyhedron in bin

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Folded the white_2D_loop before placing it in the box as it is foldable (Rule 3).
    # 2. Placed the transparent_3D_cuboid first as it is compressible (Rule 1).
    # 3. Placed the blue_3D_polyhedron without folding or pushing as it is plastic (Rule 2).
    # 4. Did not place the black_1D_line in the box as per the goal state.

    # Finally, add this code    
    print("All task planning is done")
