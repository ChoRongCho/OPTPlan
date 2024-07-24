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
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box and obj.is_soft:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Create objects
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_rigid=False, is_soft=True, is_fragile=False, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_soft=False, is_fragile=False, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_soft=False, is_fragile=True, is_in_box=False, is_out_box=True)
object3 = Object(index=3, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_rigid=True, is_soft=False, is_fragile=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_soft=False, is_fragile=False, is_in_box=True, is_out_box=False)

# Create robot
robot = Robot()

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # brown_3D_cuboid: is_in_box = True, is_out_box = False
    # yellow_3D_cylinder: is_in_box = True, is_out_box = False
    # green_3D_cylinder: is_in_box = True, is_out_box = False
    # black_1D_ring: is_in_box = False, is_out_box = True
    # white_box: is_in_box = True, is_out_box = False

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step 1: Pick and place the soft object first
    robot.pick(object0, object4)  # Pick brown_3D_cuboid
    robot.place(object0, object4)  # Place brown_3D_cuboid in white_box

    # Step 2: Push the soft object to make more space
    robot.push(object0, object4)  # Push brown_3D_cuboid

    # Step 3: Pick and place the rigid objects
    robot.pick(object1, object4)  # Pick yellow_3D_cylinder
    robot.place(object1, object4)  # Place yellow_3D_cylinder in white_box

    robot.pick(object2, object4)  # Pick green_3D_cylinder
    robot.place(object2, object4)  # Place green_3D_cylinder in white_box

    # Step 4: Pick out the black_1D_ring from the box
    robot.pick_out(object3, object4)  # Pick_Out black_1D_ring from white_box

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (brown_3D_cuboid) is placed first to ensure it is in the bin before any rigid objects.
    # 2. The soft object is pushed to make more space in the bin.
    # 3. The rigid objects (yellow_3D_cylinder and green_3D_cylinder) are placed after the soft object.
    # 4. The black_1D_ring is picked out from the box to match the goal state.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == True and object2.is_out_box == False
    assert object3.is_in_box == False and object3.is_out_box == True
    assert object4.is_in_box == True and object4.is_out_box == False

    print("Goal state achieved successfully!")
