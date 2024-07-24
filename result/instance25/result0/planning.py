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

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_fragile: bool = False


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
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.is_elastic:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot pick out {obj.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, is_in_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Final state of each object according to the goal table
    # object0 (yellow_3D_cuboid) should be out of the box
    # object1 (transparent_3D_cylinder) should be in the box
    # object2 (white_box) should remain as it is

    # Plan:
    # 1. Pick the transparent_3D_cylinder
    # 2. Place the transparent_3D_cylinder in the white_box

    # Step 1: Pick the transparent_3D_cylinder
    robot.pick(object1, object2)

    # Step 2: Place the transparent_3D_cylinder in the white_box
    robot.place(object1, object2)

    # Check if the goal state is satisfying the goal state table
    assert object0.is_in_box == False, "yellow_3D_cuboid should be out of the box"
    assert object1.is_in_box == True, "transparent_3D_cylinder should be in the box"
    assert object2.is_in_box == True, "white_box should remain as it is"

    print("Goal state achieved successfully!")
