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
            # Effects: Robot is holding the object, object is not in the bin
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Effects: Object is placed in the bin, robot hand is empty
            obj.in_bin = True
            self.state_handempty()
            bin.in_bin_objects.append(obj)
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
        # Preconditions: Object is foldable, robot hand is empty
        if obj.is_foldable and self.robot_handempty:
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
object0 = Object(index=0, name='transparent_3D_cuboid', color='transparent', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_rigid=False, is_placed=False, is_stable=False)
object1 = Object(index=1, name='blue_2D_triangle', color='blue', shape='2D_triangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=True, is_rigid=False, is_placed=False, is_stable=False)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=False, is_plastic=False, is_rigid=True, is_placed=False, is_stable=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_foldable=True, is_plastic=False, is_rigid=False, is_placed=False, is_stable=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the compressible object (transparent_3D_cuboid) first.
    # 2. Fold the foldable object (white_2D_circle) before placing it.
    # 3. Place the rigid object (yellow_3D_cylinder) after the compressible object is in the bin.
    # 4. Do not push or fold the plastic object (blue_2D_triangle).
    # 5. Place the blue_2D_triangle after folding it.
    
    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # 1. Pick and place the compressible object
    robot.pick(object0, box)
    robot.place(object0, box)

    # 2. Fold the foldable object
    robot.fold(object3, box)

    # 3. Pick and place the folded object
    robot.pick(object3, box)
    robot.place(object3, box)

    # 4. Pick and place the rigid object
    robot.pick(object2, box)
    robot.place(object2, box)

    # 5. Pick and place the plastic object
    robot.pick(object1, box)
    robot.place(object1, box)

    # Third, after making all actions, fill your reasons according to the rules
    # - Rule 1: The compressible object (transparent_3D_cuboid) is placed first.
    # - Rule 2: The plastic object (blue_2D_triangle) is not pushed or folded.
    # - Rule 3: The foldable object (white_2D_circle) is folded before placing.
    # - Rule 4: The compressible object is not pushed as it is not required by the goal state.

    # Finally, add this code    
    print("All task planning is done")
