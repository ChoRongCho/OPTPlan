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
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


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
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            bin.in_bin.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj in bin.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and obj.object_type == 'obj' and obj not in bin.in_bin:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            bin.in_bin.remove(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=True, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

object1 = Object(
    index=1, 
    name='white_1D_ring', 
    color='white', 
    shape='1D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False
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
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_2D_rectangle) -> in white_box
    # object1 (white_1D_ring) -> in white_box
    # object2 (transparent_2D_circle) -> out of any box
    # object3 (white_box) -> contains object0 and object1

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Avoid handling and moving any box
    # Rule 2: If there is a foldable object, fold the object at the platform not in the bin
    # Rule 3: When fold a foldable object, the elastic object must be in the bin
    # Rule 4: When place a fragile objects, the soft objects must be in the bin

    # Step-by-step action sequence:
    # 1. Place elastic objects in the bin first
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 2. Fold the foldable object (yellow_2D_rectangle) at the platform
    robot.fold(object0, bin)

    # 3. Place the folded object in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Fourth, check if the goal state is satisfying goal state table.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    assert object3.in_bin == [object1, object0]  # Order might differ but should contain both objects

    print("All task planning is done")
