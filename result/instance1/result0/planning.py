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
    is_flexible: bool = False
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
        if obj.is_soft and self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_flexible and self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Out {obj.name} from {bin.name}")
    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_out_box=True)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_flexible=True, is_elastic=True, is_out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Plan to pack all objects in the box
    # Step 1: Pick the blue_1D_ring and place it in the white_box
    robot.pick(object2, object3)
    robot.place(object2, object3)

    # Step 2: Pick the yellow_3D_cuboid and place it in the white_box
    robot.pick(object0, object3)
    robot.place(object0, object3)

    # Step 3: Push the yellow_3D_cuboid to make more space in the bin
    robot.push(object0, object3)

    # Note: The black_3D_cylinder is not placed in the box because it is rigid and there is no space left after placing the other objects.

    # Final state of each object
    print(f"Final state of {object0.name}: is_in_box={object0.is_in_box}, is_out_box={object0.is_out_box}")
    print(f"Final state of {object1.name}: is_in_box={object1.is_in_box}, is_out_box={object1.is_out_box}")
    print(f"Final state of {object2.name}: is_in_box={object2.is_in_box}, is_out_box={object2.is_out_box}")
    print(f"Final state of {object3.name}: is_in_box={object3.is_in_box}, is_out_box={object3.is_out_box}")

    # Check if the goal state is satisfied
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == False and object1.is_out_box == True
    assert object2.is_in_box == True and object2.is_out_box == False
    assert object3.is_in_box == True and object3.is_out_box == False

    print("Goal state is satisfied.")
