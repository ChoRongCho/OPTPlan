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
    is_foldable: bool
    is_elastic: bool
    is_rigid: bool
    is_fragile: bool
    is_soft: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_out_box: bool


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if self.robot_handempty and obj.object_type != 'box' and not obj.is_in_box:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
                return
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            bin.in_bin.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable and not obj.is_in_box:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj.is_in_box and obj in bin.in_bin:
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            bin.in_bin.remove(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_rigid=False, 
    is_fragile=False, 
    is_soft=True, 
    is_in_box=False, 
    is_out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_fragile=True, 
    is_soft=False, 
    is_in_box=False, 
    is_out_box=True
)

object2 = Object(
    index=2, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=True, 
    is_elastic=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_soft=False, 
    is_in_box=True, 
    is_out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='bin', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_soft=False, 
    is_in_box=False, 
    is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (white_3D_cylinder) -> in_box, pushed
    # object1 (green_3D_cylinder) -> in_box
    # object2 (yellow_2D_rectangle) -> in_box, folded
    # object3 (white_box) -> bin

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules

    # Rule 3: Fold the foldable object not in the bin but on the platform
    robot.pick_out(object2, bin)
    robot.fold(object2, bin)
    robot.place(object2, bin)

    # Rule 5: Pick, place and push soft objects into the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)
    robot.push(object0, bin)

    # Rule 2: When placing a rigid object in the bin, the soft object must be in the bin before
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.is_in_box == True
    assert object0.pushed == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object2.folded == True
    assert object3.is_in_box == False
    print("All task planning is done")
