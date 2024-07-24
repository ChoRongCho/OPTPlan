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
    is_elastic: bool
    is_soft: bool
    
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
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
    
    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin):
        if self.robot_handempty and obj.object_type == 'obj':
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=True, is_soft=False,
    is_fragile=False, is_heavy=False
)

object1 = Object(
    index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=True, is_soft=False,
    is_fragile=False, is_heavy=False
)

object2 = Object(
    index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=False, is_soft=True,
    is_fragile=False, is_heavy=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin=[object2], is_elastic=False, is_soft=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (blue_1D_ring) -> in white_box
    # object1 (white_1D_ring) -> in white_box
    # object2 (yellow_3D_cuboid) -> out of white_box
    # object3 (white_box) -> contains object0 and object1

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Pick out yellow_3D_cuboid from white_box
    robot.pick_out(object2, bin)

    # 2. Pick blue_1D_ring and place it in white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick white_1D_ring and place it in white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    assert object3.in_bin == [object0, object1]
    print("All task planning is done")
