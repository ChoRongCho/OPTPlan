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
    is_elastic: bool
    is_fragile: bool

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
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj == self.robot_now_holding:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable and not obj.is_fragile:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_elastic=False, is_fragile=True, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_elastic=False, is_fragile=False, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_rigid=False, is_elastic=True, is_fragile=False, is_in_box=False, is_packable=True)
object3 = Object(index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_rigid=False, is_elastic=True, is_fragile=False, is_in_box=True, is_packable=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_elastic=False, is_fragile=False, is_in_box=True, is_packable=False)

if __name__ == '__main__':
    # Initialize the robot
    robot = Robot()

    # Define the bin (white_box)
    bin = object4

    # Plan to achieve the goal state
    # 1. Pick the green_3D_cylinder and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick the blue_1D_ring and place it in the box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Final state of each object
    # green_3D_cylinder: is_in_box = True
    # yellow_3D_cylinder: is_in_box = False
    # blue_1D_ring: is_in_box = True
    # white_1D_ring: is_in_box = True
    # white_box: is_in_box = True

    # Check if the goal state is satisfying goal state table
    assert object0.is_in_box == True, "green_3D_cylinder should be in the box"
    assert object1.is_in_box == False, "yellow_3D_cylinder should not be in the box"
    assert object2.is_in_box == True, "blue_1D_ring should be in the box"
    assert object3.is_in_box == True, "white_1D_ring should be in the box"
    assert object4.is_in_box == True, "white_box should be in the box"

    print("All objects are in their correct final states.")
