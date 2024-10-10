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
        # Preconditions: Object is not in the bin, robot hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: Object is in the bin, robot hand is empty
        if obj.in_bin and self.robot_handempty:
            # Effects: Object is not in the bin, robot hand is empty
            obj.in_bin = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='blue_2D_triangle', color='blue', shape='2D_triangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_plastic=True, is_rigid=False, is_2D=True, is_3D=False)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_plastic=False, is_rigid=True, is_2D=False, is_3D=True)
object2 = Object(index=2, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_plastic=False, is_rigid=True, is_2D=False, is_3D=True)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the blue_2D_triangle since it is foldable (Rule 3).
    # 2. Place the yellow_3D_cylinder in the bin since there is no compressible object (Rule 1).
    # 3. Place the black_3D_cylinder in the bin since there is no compressible object (Rule 1).

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # 1. Fold the blue_2D_triangle
    robot.fold(object0, box)
    
    # 2. Pick and place the yellow_3D_cylinder
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 3. Pick and place the black_3D_cylinder
    robot.pick(object2, box)
    robot.place(object2, box)

    # Third, after making all actions, fill your reasons according to the rules
    # - The blue_2D_triangle is foldable, so it was folded first (Rule 3).
    # - The yellow_3D_cylinder and black_3D_cylinder are rigid objects, and since there is no compressible object, they were placed directly (Rule 1).
    # - No plastic objects were pushed or folded (Rule 2).
    # - No compressible objects were pushed after placing items in the bin (Rule 4).

    # Finally, add this code    
    print("All task planning is done")
