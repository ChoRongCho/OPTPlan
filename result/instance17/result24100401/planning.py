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
    is_rigid: bool
    is_foldable: bool
    is_compressible: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_in_box: bool
    is_out_box: bool

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
        if not self.robot_handempty and self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_bin = True
            obj.is_in_box = True
            obj.is_out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.in_bin:
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
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_rigid=True, is_foldable=False, is_compressible=False, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_rigid=False, is_foldable=True, is_compressible=False, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=False, is_rigid=False, is_foldable=False, is_compressible=True, is_in_box=False, is_out_box=True)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (white_2D_circle) before placing it in the box.
    # 2. Place the compressible object (red_3D_polyhedron) in the box first.
    # 3. Place the foldable object (white_2D_circle) in the box after folding.
    # 4. Do not place the rigid object (beige_1D_line) in the box as per the goal state.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # Action sequence
    # Step 1: Fold the white_2D_circle
    robot.fold(object1, box)
    
    # Step 2: Pick and place the red_3D_polyhedron in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Step 3: Pick and place the white_2D_circle in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: The red_3D_polyhedron is compressible and is placed in the box first.
    # Rule 2: The white_2D_circle is foldable and is folded before placing it in the box.
    # Rule 3: The beige_1D_line is rigid and not placed in the box as per the goal state.
    # Rule 4: No pushing action is required as per the goal state.

    # Finally, add this code    
    print("All task planning is done")
