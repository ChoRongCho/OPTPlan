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
        if self.robot_handempty and not obj.in_bin:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.in_bin = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_bin:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.in_bin:
            # Effects
            obj.in_bin = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot pick out {obj.name}")

    def dummy(self):
        pass


object0 = Object(
    index=0, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False
)

object1 = Object(
    index=1, 
    name='beige_1D_ring', 
    color='beige', 
    shape='1D_ring', 
    object_type='obj', 
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    object0.in_bin = False  # transparent_3D_cylinder starts out of the box
    object1.in_bin = False  # beige_1D_ring starts out of the box
    object2.in_bin = True   # white_box is already the box

    # Initialize the robot
    robot = Robot()

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Plan:
    # 1. Pick transparent_3D_cylinder and place it in the white_box
    # 2. Pick beige_1D_ring and place it in the white_box

    # Step 1: Pick transparent_3D_cylinder and place it in the white_box
    robot.pick(object0, object2)
    robot.place(object0, object2)

    # Step 2: Pick beige_1D_ring and place it in the white_box
    robot.pick(object1, object2)
    robot.place(object1, object2)

    # after making all actions, fill your reasons according to the rules
    # Rule 1: It is prohibited to lift and relocate a container.
    # - We did not lift or relocate the white_box.
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before.
    # - We did not place any rigid objects, so this rule does not apply.
    # Rule 3: When placing a fragile object, the soft objects must be in the bin.
    # - We did not place any fragile objects, so this rule does not apply.

    # check if the goal state is satisfying goal state table
    assert object0.in_bin == True, "transparent_3D_cylinder should be in the box"
    assert object1.in_bin == True, "beige_1D_ring should be in the box"
    assert object2.in_bin == True, "white_box should be in the box"

    print("All objects are in the correct final state.")
