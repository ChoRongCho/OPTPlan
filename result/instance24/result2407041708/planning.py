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
    is_foldable: bool

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_packable: bool


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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and not obj.is_rigid and not obj.is_foldable:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
            self.state_handempty()

    def dummy(self):
        pass


# Create objects based on the initial state
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_foldable=False, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_rigid=False, is_foldable=True, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_foldable=False, is_in_box=True, is_packable=False)

# Create the bin (box)
bin = object2  # The white_box is the bin

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cylinder) -> in_box
    # object1 (yellow_2D_rectangle) -> in_box
    # object2 (white_box) -> box (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box), this is an example. 
    bin = object2  # The white_box is the bin

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Don't pick and place a box called bin
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object. When pushing an object, neither fragile nor rigid objects are permitted.

    # Action sequence:
    # 1. Fold the yellow_2D_rectangle (soft object)
    robot.fold(object1, bin)
    
    # 2. Place the yellow_2D_rectangle in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)
    
    # 3. Pick the yellow_3D_cylinder (rigid object)
    robot.pick(object0, bin)
    
    # 4. Place the yellow_3D_cylinder in the bin
    robot.place(object0, bin)

    # Fourth, check if the goal state is satisfying goal state table. These are examples.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True  # The box itself is always in the box
    print("All task planning is done")
