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
    is_foldable: bool
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
        if self.robot_handempty and obj.object_type != 'bin' and obj.is_out_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_out_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if not self.robot_handempty and obj.object_type != 'bin':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            obj.is_in_box = True
            obj.is_out_box = False
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and not obj.is_rigid and not obj.is_foldable:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin and not self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=False, 
    is_foldable=False, 
    is_soft=True, 
    is_in_box=False, 
    is_out_box=True
)

object1 = Object(
    index=1, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=False, 
    is_foldable=True, 
    is_soft=False, 
    is_in_box=False, 
    is_out_box=True
)

object2 = Object(
    index=2, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_rigid=True, 
    is_foldable=False, 
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
    is_rigid=False, 
    is_foldable=False, 
    is_soft=False, 
    is_in_box=False, 
    is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: is_out_box = True
    # object1: is_in_box = True, folded = True
    # object2: is_in_box = True
    # object3: in_bin = [object1, object2]

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Step 1: Pick out the rigid object (black_3D_cylinder) from the bin
    robot.pick_out(object2, bin)

    # Step 2: Fold the foldable object (yellow_2D_rectangle)
    robot.fold(object1, bin)

    # Step 3: Place the folded object (yellow_2D_rectangle) into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 4: Place the rigid object (black_3D_cylinder) back into the bin
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == False
    assert object1.is_in_box == True
    assert object1.folded == True
    assert object2.is_in_box == True
    assert object3.in_bin == [object1, object2]
    print("All task planning is done")
