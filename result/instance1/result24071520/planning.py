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
    is_soft: bool
    is_elastic: bool
    is_rigid: bool
    
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
            if obj.is_rigid and any(o.is_soft for o in bin.in_bin):
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
            elif not obj.is_rigid:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
            else:
                print(f"Cannot Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj in bin.in_bin:
            if not any(o.is_fragile for o in bin.in_bin if o != obj):
                print(f"Push {obj.name}")
                obj.pushed = True
            else:
                print(f"Cannot Push {obj.name} because a fragile object is on it")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj not in bin.in_bin:
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
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_elastic=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_heavy=False
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_fragile=False, 
    is_heavy=False
)

object2 = Object(
    index=2, 
    name='blue_1D_ring', 
    color='blue', 
    shape='1D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_elastic=True, 
    is_rigid=False, 
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
    is_soft=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> in_box, pushed=True
    # object1 (black_3D_cylinder) -> in_box
    # object2 (blue_1D_ring) -> out_box
    # object3 (white_box) -> box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Pick and place the yellow_3D_cuboid (soft object) into the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Push the yellow_3D_cuboid to make more space in the bin
    robot.push(object0, bin)

    # 3. Pick and place the black_3D_cylinder (rigid object) into the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin and object0.pushed == True
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    assert object3.object_type == 'box'
    print("All task planning is done")
