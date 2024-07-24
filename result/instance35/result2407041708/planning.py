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
    is_elastic: bool = False
    is_rigid: bool = False

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
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = True
            obj.is_in_box = False
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
        if obj.is_soft and self.robot_handempty:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_elastic and self.robot_handempty:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
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


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box')

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> is_in_box: True
    # object1 (red_3D_polyhedron) -> is_in_box: True
    # object2 (black_3D_cylinder) -> is_in_box: True
    # object3 (white_1D_ring) -> is_in_box: False
    # object4 (white_box) -> is_in_box: False (box itself should not be in another box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Push yellow_3D_cuboid (soft object) into the box
    robot.push(object0, bin)
    
    # 2. Push red_3D_polyhedron (soft object) into the box
    robot.push(object1, bin)
    
    # 3. Pick out white_1D_ring (elastic object) from the box
    robot.pick_out(object3, bin)
    
    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == False
    assert object4.is_in_box == False
    print("All task planning is done")
