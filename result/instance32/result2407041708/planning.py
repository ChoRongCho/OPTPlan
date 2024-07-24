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
    is_rigid: bool = False
    is_fragile: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_packable: bool = True


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
        if self.robot_handempty and not obj.is_in_box and obj.is_packable:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic and not obj.is_fragile:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot pick out {obj.name}")

    def dummy(self):
        pass


# Create objects
object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=False)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False)
object3 = Object(index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_packable=False)

# Create robot
robot = Robot()

# Initial state
robot.state_base()

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (green_3D_cylinder) -> in_box
    # object1 (yellow_3D_cylinder) -> out_box
    # object2 (blue_1D_ring) -> in_box
    # object3 (white_1D_ring) -> in_box
    # object4 (white_box) -> box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # c) Make the action sequence
    # Pick and place green_3D_cylinder into the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Pick and place blue_1D_ring into the box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The green_3D_cylinder is rigid and fragile, and it needs to be placed in the box.
    # 2. The blue_1D_ring is elastic and needs to be placed in the box.
    # 3. The white_1D_ring is already in the box, so no action is needed for it.
    # 4. The yellow_3D_cylinder should remain out of the box, so no action is needed for it.
    # 5. The white_box is the bin, and it should not be picked or placed.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == False  # The box itself should not be in another box
    print("All task planning is done")
