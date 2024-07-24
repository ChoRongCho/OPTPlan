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

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = True


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
        if obj.is_out_box and self.robot_handempty:
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
        if self.robot_handempty and obj.is_soft and not obj.is_rigid:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
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
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_out_box=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, is_out_box=True)
object2 = Object(index=2, name='yellow_2D_flat_rectangle', color='yellow', shape='2D_flat_rectangle', object_type='obj', is_rigid=True, is_elastic=True, is_in_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

if __name__ == '__main__':
    # Initialize the robot
    robot = Robot()

    # Final state of each object according to the goal table
    # object0 (red_3D_polyhedron) should be in the box
    # object1 (transparent_3D_cylinder) should be in the box
    # object2 (yellow_2D_flat_rectangle) is already in the box
    # object3 (white_box) is already in the box

    # Action sequence to achieve the goal state

    # Step 1: Push the red_3D_polyhedron (soft object) into the box
    robot.push(object0, object3)

    # Step 2: Fold the transparent_3D_cylinder (elastic object) into the box
    robot.fold(object1, object3)

    # The yellow_2D_flat_rectangle is already in the box, no action needed for it

    # The white_box is already in the box, no action needed for it

    # Check if the goal state is satisfying the goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True

    print("All objects are in the box as per the goal state.")
