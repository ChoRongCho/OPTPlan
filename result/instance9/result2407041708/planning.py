from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates
    is_elastic: bool = False
    is_fragile: bool = False
    is_foldable: bool = False
    is_soft: bool = False
    is_rigid: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = True


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
        if self.robot_handempty and obj.is_out_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft and o.is_in_box for o in bin):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
                return
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and obj.is_out_box:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_elastic=True, is_soft=True, is_out_box=True, is_in_box=False)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_out_box=True, is_in_box=False)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (white_3D_cylinder) -> in_box
    # object1 (green_3D_cylinder) -> in_box
    # object2 (yellow_2D_rectangle) -> in_box
    # object3 (white_box) -> box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules

    # Rule 4: When a rigid object is in the bin at the initial state, out of the rigid object and replace it into the bin
    # object2 is foldable and in the bin, so we need to pick it out first
    robot.pick_out(object2, bin)

    # Rule 3: If there is a foldable object, fold the object not in the bin but on the platform
    robot.fold(object2, bin)

    # Place the folded object back into the bin
    robot.place(object2, bin)

    # Rule 2: When placing a rigid object in the bin, the soft object must be in the bin before
    # Pick the soft object (object0) and place it in the bin first
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Now pick the rigid object (object1) and place it in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == False  # The box itself is not in another box
    print("All task planning is done")
