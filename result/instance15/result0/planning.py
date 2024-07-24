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
    is_soft: bool = False
    is_elastic: bool = False
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
        if self.robot_handempty and not obj.is_in_box:
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
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, is_in_box=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False)
object3 = Object(index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=True)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', is_packable=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Define the bin (box)
    bin = object5

    # Action sequence to achieve the goal state
    # 1. Pick out the fragile object (green_3D_cylinder) from the box
    robot.pick_out(object4, bin)
    
    # 2. Place the soft object (yellow_3D_cuboid) in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)
    
    # 3. Place the soft and elastic object (white_3D_cylinder) in the box
    robot.pick(object1, bin)
    robot.place(object1, bin)
    
    # 4. Place the fragile object (green_3D_cylinder) back into the box
    robot.pick(object4, bin)
    robot.place(object4, bin)

    # Final state of each object
    print(f"{object0.name} is in box: {object0.is_in_box}")
    print(f"{object1.name} is in box: {object1.is_in_box}")
    print(f"{object2.name} is in box: {object2.is_in_box}")
    print(f"{object3.name} is in box: {object3.is_in_box}")
    print(f"{object4.name} is in box: {object4.is_in_box}")
    print(f"{object5.name} is in box: {object5.is_in_box}")

    # Check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    assert object5.is_in_box == False

    print("Goal state achieved successfully!")
