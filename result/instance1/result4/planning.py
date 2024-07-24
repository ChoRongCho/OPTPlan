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
        if obj.object_type != 'box' and obj not in bin.in_bin and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_rigid and any(o.is_soft for o in bin.in_bin):
                bin.in_bin.append(obj)
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
            elif not obj.is_fragile or any(o.is_elastic for o in bin.in_bin):
                bin.in_bin.append(obj)
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj in bin.in_bin:
            if not any(o.is_fragile for o in bin.in_bin if o != obj):
                obj.pushed = True
                print(f"Push {obj.name}")
            else:
                print(f"Cannot Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.object_type != 'box':
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def pick_out(self, obj, bin):
        if obj in bin.in_bin and self.robot_handempty:
            bin.in_bin.remove(obj)
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
# Initialize objects
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True, 
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
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
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
    is_rigid=False, 
    is_elastic=True, 
    is_soft=False, 
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
    is_elastic=False, 
    is_soft=False, 
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) -> in white_box, pushed=True
    # object1 (black_3D_cylinder) -> in white_box
    # object2 (blue_1D_ring) -> out of white_box
    # object3 (white_box) -> remains as is

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Step 1: Pick and place the soft object (brown_3D_cuboid) first
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 2: Push the soft object to make more space
    robot.push(object0, bin)

    # Step 3: Pick and place the rigid object (black_3D_cylinder)
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin and object0.pushed == True
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    assert object3.object_type == 'box'
    print("All task planning is done")
