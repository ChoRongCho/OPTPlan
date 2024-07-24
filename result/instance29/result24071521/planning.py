from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic Effect Robot Action Predicates for object_type = obj
    pushed: bool
    folded: bool
    
    # Bin Predicates for object_type = bin
    in_bin: list
    
    # Object physical properties predicates
    is_rigid: bool
    is_soft: bool
    is_elastic: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


class Robot:
    def __init__(self, name: str = "UR5", goal: str = None, actions: dict = None):
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

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False

    def state_base(self):
        self.robot_base_pose = True

    def pick(self, obj, bin):
        if obj.object_type != 'box' and obj not in bin.in_bin and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj.is_elastic and any(o.is_fragile for o in bin.in_bin):
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")

    def pick_out(self, obj, bin):
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=True, 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=False, 
    is_soft=True, 
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False
)

object2 = Object(
    index=2, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=False, 
    is_soft=True, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=False, 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: out_box
    # object1: in_box
    # object2: in_box
    # object3: box (bin)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # c) Plan the actions
    # Pick and place white_3D_cylinder (object1) into the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Pick and place red_3D_polyhedron (object2) into the box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Never attempt to pick up and set down an object named box - Followed
    # 2. When fold a foldable object, the fragile object must be in the bin - Not applicable
    # 3. Do not place a fragile object if there is no elastic object in the bin - Followed (no fragile objects)
    # 4. You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object when push an object, neither fragile and rigid objects are permitted - Not applicable

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in bin.in_bin == False
    assert object1 in bin.in_bin == True
    assert object2 in bin.in_bin == True
    assert object3.in_bin == []
    print("All task planning is done")
