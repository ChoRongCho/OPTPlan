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
    is_rigid: bool = False
    is_elastic: bool = False
    is_soft: bool = False
    is_fragile: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = False


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
        if obj.name != "box" and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = True
            print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_elastic and not obj.is_in_box:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft:
            # Effects
            obj.is_rigid = True  # Assuming folding makes it rigid
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


# Creating objects based on the initial state
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) -> is_in_box: True
    # object1 (blue_1D_ring) -> is_in_box: False
    # object2 (transparent_3D_cylinder) -> is_in_box: True
    # object3 (white_2D_circle) -> is_in_box: True
    # object4 (white_box) -> is_in_box: True (already in the box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Fold the brown_3D_cuboid (soft object) to make it rigid
    robot.fold(object0, bin)
    
    # 2. Pick the brown_3D_cuboid and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)
    
    # 3. Push the blue_1D_ring (elastic object) to the platform (not in the box)
    robot.push(object1, bin)
    
    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    print("All task planning is done")
