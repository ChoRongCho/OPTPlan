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
        # Preconditions: The object is not in the bin, the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Effects: The robot is now holding the object, the object is not in the bin
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        # Preconditions: The robot is holding the object
        if self.robot_now_holding == obj:
            # Effects: The object is placed in the bin, the robot's hand is empty
            bin.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        # Preconditions: The object is in the bin, the robot's hand is empty
        if obj.in_bin and self.robot_handempty:
            # Effects: The object is pushed
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        # Preconditions: The object is compressible, the robot's hand is empty
        if obj.is_compressible and self.robot_handempty:
            # Effects: The object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        # Preconditions: The object is in the bin
        if obj in bin.in_bin_objects:
            # Effects: The object is removed from the bin, the robot's hand is empty
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_plastic=False, is_rigid=False, is_heavy=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=True, is_plastic=False, is_rigid=False, is_heavy=False, is_fragile=False)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=False, is_rigid=True, is_heavy=False, is_fragile=False)
object3 = Object(index=3, name='green_1D_line', color='green', shape='1D_line', object_type='obj', pushed=False, folded=False, in_bin=False, is_compressible=False, is_plastic=True, is_rigid=False, is_heavy=False, is_fragile=False)

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the compressible objects before placing them in the bin.
    # 2. Place the folded compressible object in the bin first.
    # 3. Place the rigid object in the bin.
    # 4. Place the plastic object in the bin.
    # 5. Push the compressible object after placing all items in the bin.

    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # Action sequence
    # Fold the brown_3D_cylinder (compressible)
    robot.fold(object0, box)
    
    # Place the folded brown_3D_cylinder in the bin
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Place the yellow_3D_cylinder (rigid) in the bin
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Place the green_1D_line (plastic) in the bin
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Push the brown_3D_cylinder (compressible) in the bin
    robot.push(object0, box)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. The brown_3D_cylinder is folded before placing it in the bin because it is compressible.
    # 2. The brown_3D_cylinder is placed first to satisfy the condition for placing rigid objects.
    # 3. The yellow_3D_cylinder is placed after the brown_3D_cylinder because it is rigid.
    # 4. The green_1D_line is placed after the yellow_3D_cylinder as it is plastic and not affected by the order.
    # 5. The brown_3D_cylinder is pushed after all items are placed in the bin.

    # Finally, add this code    
    print("All task planning is done")
