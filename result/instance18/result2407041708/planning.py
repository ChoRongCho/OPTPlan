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
        if self.robot_handempty and obj.is_out_box and not obj.object_type == 'box':
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_soft and bin.is_in_box:
                # Effects
                self.state_handempty()
                obj.is_in_box = True
                obj.is_out_box = False
                print(f"Place {obj.name} in {bin.name}")
            elif obj.is_rigid and bin.is_in_box:
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
        if self.robot_handempty and obj.is_foldable:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and not self.robot_handempty:
            # Effects
            self.state_handempty()
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_rigid=True, is_foldable=True, is_in_box=True, is_out_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) should be in the box
    # object1 (black_2D_circle) should be out of the box
    # object2 (white_box) should remain in the box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object2  # white_box

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 4: when a rigid object in the bin at the initial state, out of the rigid object first
    robot.pick_out(object1, bin)  # Pick out black_2D_circle from the box

    # Rule 2: when place a soft object, the elastic object must be in the bin
    robot.pick(object0, bin)  # Pick brown_3D_cuboid
    robot.place(object0, bin)  # Place brown_3D_cuboid in the box

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    print("All task planning is done")