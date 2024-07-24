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
    is_rigid: bool
    is_soft: bool
    is_elastic: bool
    is_fragile: bool

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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if obj.object_type != 'box' and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_out_box and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=False, 
    is_soft=True, 
    is_elastic=True, 
    is_fragile=False, 
    is_in_box=False, 
    is_out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=True, 
    is_in_box=False, 
    is_out_box=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    is_rigid=False, 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_in_box=True, 
    is_out_box=False
)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal state:
    # white_3D_cylinder: is_in_box = True, is_out_box = False
    # green_3D_cylinder: is_in_box = True, is_out_box = False
    # white_box: is_in_box = True, is_out_box = False

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step 1: Fold the white_3D_cylinder (soft object) on the platform
    robot.fold(object0, object2)

    # Step 2: Pick the white_3D_cylinder and place it in the white_box
    robot.pick(object0, object2)
    robot.place(object0, object2)

    # Step 3: Pick the green_3D_cylinder and place it in the white_box
    robot.pick(object1, object2)
    robot.place(object1, object2)

    # after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box
    # - Followed: No actions involve picking up or setting down the white_box.

    # Rule 2: When placing a rigid object in the bin, the soft object must be in the bin before
    # - Followed: The white_3D_cylinder (soft) is placed in the white_box before the green_3D_cylinder (rigid).

    # Rule 3: If there is a foldable object, fold the object not in the bin but on the platform
    # - Followed: The white_3D_cylinder (soft) is folded on the platform before being placed in the white_box.

    # Rule 4: When a rigid object is in the bin at the initial state, take out the rigid object and replace it into the bin
    # - Not applicable: No rigid objects are initially in the bin.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == True and object2.is_out_box == False

    print("All objects are in the correct final state.")
