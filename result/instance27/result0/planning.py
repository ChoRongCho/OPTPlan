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
    is_soft: bool
    is_elastic: bool

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_fragile: bool


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
        if obj.object_type == 'box':
            raise ValueError("Cannot pick a box")
        if obj.is_in_box:
            raise ValueError("Object is already in the bin")
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        self.state_holding(obj)
        obj.is_in_box = False
        print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type == 'box':
            raise ValueError("Cannot place a box")
        if not self.robot_now_holding == obj:
            raise ValueError("Robot is not holding the correct object")
        if obj.is_fragile and not any(o.is_elastic for o in bin if o.is_in_box):
            raise ValueError("Cannot place a fragile object without an elastic object in the bin")
        if not obj.is_soft and not any(o.is_soft for o in bin if o.is_in_box):
            raise ValueError("Cannot place a rigid object without a soft object in the bin")
        
        # Effects
        self.state_handempty()
        obj.is_in_box = True
        print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        if obj.is_fragile or not obj.is_soft:
            raise ValueError("Only soft objects can be pushed")
        
        # Effects
        obj.is_in_box = True
        print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.object_type == 'box':
            raise ValueError("Cannot pick out a box")
        if not obj.is_in_box:
            raise ValueError("Object is not in the bin")
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        self.state_holding(obj)
        obj.is_in_box = False
        print(f"Pick_Out {obj.name} from {bin.name}")
        self.state_handempty()
        print(f"Place {obj.name} on not_bin")

    def dummy(self):
        pass


object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_soft=True, 
    is_elastic=True, 
    is_in_box=False, 
    is_fragile=False
)

object1 = Object(
    index=1, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_soft=False, 
    is_elastic=True, 
    is_in_box=False, 
    is_fragile=False
)

object2 = Object(
    index=2, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_soft=True, 
    is_elastic=False, 
    is_in_box=True, 
    is_fragile=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    is_soft=False, 
    is_elastic=False, 
    is_in_box=True, 
    is_fragile=False
)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Define the bin (box)
    bin = object3

    # Plan actions to achieve the goal state
    # Goal: All objects should be in the box

    # Step 1: Pick and place the white_3D_cylinder (soft and elastic)
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 2: Pick and place the transparent_3D_cylinder (rigid and elastic)
    # Since there is already a soft object in the bin, we can place the rigid object
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # The brown_3D_cuboid is already in the bin, so no action is needed for it

    # Final state check
    assert object0.is_in_box == True, "white_3D_cylinder should be in the box"
    assert object1.is_in_box == True, "transparent_3D_cylinder should be in the box"
    assert object2.is_in_box == True, "brown_3D_cuboid should be in the box"
    assert object3.is_in_box == True, "white_box should be in the box"

    print("All objects are correctly placed in the box.")
