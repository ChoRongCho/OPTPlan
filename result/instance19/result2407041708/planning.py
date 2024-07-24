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
    is_fragile: bool = False
    is_elastic: bool = False
    is_rigid: bool = False
    is_soft: bool = False
    is_foldable: bool = False

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
        if obj.object_type == 'box':
            raise ValueError("Cannot pick a box")
        if obj.is_in_box:
            raise ValueError("Object is already in the bin")
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        self.state_holding(obj)
        obj.is_out_box = True
        obj.is_in_box = False
        print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type == 'box':
            raise ValueError("Cannot place a box")
        if self.robot_handempty:
            raise ValueError("Robot hand is empty")
        if obj.is_rigid and not any(o.is_soft and o.is_in_box for o in bin):
            raise ValueError("Soft objects must be in the bin before placing a rigid object")
        
        # Effects
        self.state_handempty()
        obj.is_in_box = True
        obj.is_out_box = False
        print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        if not obj.is_soft:
            raise ValueError("Can only push soft objects")
        if any(o.is_rigid and o.is_in_box for o in bin):
            raise ValueError("Cannot push if there are rigid objects in the bin")
        
        # Effects
        print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        if not obj.is_foldable:
            raise ValueError("Object is not foldable")
        
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
        obj.is_out_box = True
        self.state_handempty()
        print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Initialize objects
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_fragile=True, is_rigid=True, is_in_box=False, is_out_box=True)
object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_elastic=True, is_foldable=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

# Initialize robot
robot = Robot()

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: is_in_box = True, is_out_box = False
    # object1: is_in_box = True, is_out_box = False
    # object2: is_in_box = True, is_out_box = False
    # object3: is_in_box = False, is_out_box = True
    # object4: is_in_box = True, is_out_box = False (box, no action needed)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Push the soft object (brown_3D_cuboid) into the bin
    robot.push(object0, bin)
    object0.is_in_box = True
    object0.is_out_box = False

    # 2. Place the rigid object (yellow_3D_cylinder) into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)
    object1.is_in_box = True
    object1.is_out_box = False

    # 3. Place the fragile and rigid object (green_3D_cylinder) into the bin
    robot.pick(object2, bin)
    robot.place(object2, bin)
    object2.is_in_box = True
    object2.is_out_box = False

    # 4. Pick out the foldable object (black_2D_circle) from the bin
    robot.pick_out(object3, bin)
    object3.is_in_box = False
    object3.is_out_box = True

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == False
    assert object4.is_in_box == True
    print("All task planning is done")
