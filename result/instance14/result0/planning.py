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
    is_elastic: bool

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
        if obj.object_type != 'box' and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
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
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_elastic and self.robot_handempty:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_rigid=False, is_soft=True, is_elastic=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_soft=False, is_elastic=False, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_rigid=False, is_soft=False, is_elastic=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_rigid=False, is_soft=False, is_elastic=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_soft=False, is_elastic=False, is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Define the bin (box)
    bin = object4

    # Plan actions to achieve the goal state
    # Step 1: Push the white_3D_cylinder to make space in the bin
    robot.push(object0, bin)
    
    # Step 2: Pick the white_3D_cylinder and place it in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)
    
    # Step 3: Pick the black_3D_cylinder and place it in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)
    
    # Step 4: Ensure the white_1D_ring and blue_1D_ring are already in the bin
    # No action needed as they are already in the bin

    # Final state of each object
    print(f"Final state of {object0.name}: is_in_box={object0.is_in_box}, is_out_box={object0.is_out_box}")
    print(f"Final state of {object1.name}: is_in_box={object1.is_in_box}, is_out_box={object1.is_out_box}")
    print(f"Final state of {object2.name}: is_in_box={object2.is_in_box}, is_out_box={object2.is_out_box}")
    print(f"Final state of {object3.name}: is_in_box={object3.is_in_box}, is_out_box={object3.is_out_box}")
    print(f"Final state of {object4.name}: is_in_box={object4.is_in_box}, is_out_box={object4.is_out_box}")

    # Check if the goal state is satisfying the goal state table
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == True and object2.is_out_box == False
    assert object3.is_in_box == True and object3.is_out_box == False
    assert object4.is_in_box == False and object4.is_out_box == False

    print("Goal state achieved successfully!")
