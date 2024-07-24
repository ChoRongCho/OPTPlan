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
    is_soft: bool = False
    is_rigid: bool = False
    is_foldable: bool = False

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
        if obj.object_type != 'box' and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_foldable and self.robot_handempty:
            # Effects
            obj.is_foldable = False  # Assuming folding makes it non-foldable
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='white_3D_cone', color='white', shape='3D_cone', object_type='obj', is_foldable=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (black_3D_cylinder) -> is_in_box: True, is_out_box: False
    # object1 (white_3D_cone) -> is_in_box: True, is_out_box: False
    # object2 (brown_3D_cuboid) -> is_in_box: True, is_out_box: False
    # object3 (white_box) -> is_in_box: True, is_out_box: False

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Don't pick and place a box called bin
    # Rule 2: When fold a foldable object, the fragile object must be in the bin
    # Rule 3: Do not place a fragile object if there is no elastic object in the bin
    # Rule 4: When push an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted

    # Step-by-step action sequence
    # 1. Fold the white_3D_cone (object1) since it is foldable
    robot.fold(object1, bin)

    # 2. Pick the black_3D_cylinder (object0) and place it in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick the white_3D_cone (object1) and place it in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 4. The brown_3D_cuboid (object2) is already in the bin, no action needed

    # Fourth, check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    print("All task planning is done")
