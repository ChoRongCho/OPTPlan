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
    is_foldable: bool = False
    is_soft: bool = False
    is_elastic: bool = False

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
        if self.robot_handempty and not obj.is_in_box:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = True
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
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and not obj.is_in_box:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj.is_in_box:
            # Effects
            self.state_handempty()
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_2D_flat_rectangle', color='yellow', shape='2D_flat_rectangle', object_type='obj', is_foldable=True, is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='orange_2D_flat_rectangle', color='orange', shape='2D_flat_rectangle', object_type='obj', is_soft=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='green_2D_flat_rectangle', color='green', shape='2D_flat_rectangle', object_type='obj', is_foldable=True, is_rigid=True, is_in_box=True, is_out_box=False)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Define the bin
    bin = object5

    # Plan actions to achieve the goal state
    # Step 1: Fold the foldable objects that are out of the box
    robot.fold(object0, bin)  # Fold yellow_2D_flat_rectangle

    # Step 2: Place soft objects in the bin first
    robot.pick(object0, bin)  # Pick yellow_2D_flat_rectangle
    robot.place(object0, bin)  # Place yellow_2D_flat_rectangle in the bin

    robot.pick(object1, bin)  # Pick transparent_3D_cylinder
    robot.place(object1, bin)  # Place transparent_3D_cylinder in the bin

    # Step 3: Ensure all objects are in the bin
    # Note: red_3D_polyhedron, orange_2D_flat_rectangle, and green_2D_flat_rectangle are already in the bin

    # Final state of each object
    print(f"Final state of {object0.name}: is_in_box={object0.is_in_box}, is_out_box={object0.is_out_box}")
    print(f"Final state of {object1.name}: is_in_box={object1.is_in_box}, is_out_box={object1.is_out_box}")
    print(f"Final state of {object2.name}: is_in_box={object2.is_in_box}, is_out_box={object2.is_out_box}")
    print(f"Final state of {object3.name}: is_in_box={object3.is_in_box}, is_out_box={object3.is_out_box}")
    print(f"Final state of {object4.name}: is_in_box={object4.is_in_box}, is_out_box={object4.is_out_box}")
    print(f"Final state of {object5.name}: is_in_box={object5.is_in_box}, is_out_box={object5.is_out_box}")

    # Check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    assert object5.is_in_box == False

    print("Goal state achieved successfully!")
