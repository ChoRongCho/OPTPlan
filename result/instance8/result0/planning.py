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
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid:
                if any(o.is_elastic for o in bin):
                    # Effects
                    obj.is_in_box = True
                    self.state_handempty()
                    print(f"Place {obj.name} in {bin.name}")
            elif obj.is_elastic:
                if any(o.color == 'blue' for o in bin):
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
        if self.robot_handempty and obj.is_elastic:
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


object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_rigid=False, is_elastic=True, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_elastic=False, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_rigid=False, is_elastic=True, is_in_box=False, is_fragile=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_elastic=False, is_in_box=True, is_fragile=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Define the bin (white_box)
    bin = object3

    # Plan to achieve the goal state
    # 1. Pick blue_1D_ring and place it in the white_box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # 2. Pick transparent_3D_cylinder and place it in the white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick black_3D_cylinder and place it in the white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Final state of each object
    print(f"Final state of {object0.name}: is_in_box = {object0.is_in_box}")
    print(f"Final state of {object1.name}: is_in_box = {object1.is_in_box}")
    print(f"Final state of {object2.name}: is_in_box = {object2.is_in_box}")
    print(f"Final state of {object3.name}: is_in_box = {object3.is_in_box}")

    # Check if the goal state is satisfying the goal state table
    assert object0.is_in_box == True, "transparent_3D_cylinder should be in the box"
    assert object1.is_in_box == True, "black_3D_cylinder should be in the box"
    assert object2.is_in_box == True, "blue_1D_ring should be in the box"
    assert object3.is_in_box == True, "white_box should be in the box"
    
    print("All objects are correctly placed in the box.")
