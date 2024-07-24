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
        if obj.object_type == "box":
            raise ValueError("Cannot pick up an object named box")
        if obj.is_in_box:
            raise ValueError("Object is already in the bin")
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        self.state_holding(obj)
        obj.is_in_box = False
        print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_handempty:
            raise ValueError("Robot hand is empty")
        if obj.object_type == "box":
            raise ValueError("Cannot place an object named box")
        if obj.shape == "1D" and not any(o.is_soft and o.is_in_box for o in bin):
            raise ValueError("A soft object must be in the bin before placing a 1D object")
        
        # Effects
        self.state_handempty()
        obj.is_in_box = True
        print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        if obj.is_in_box:
            raise ValueError("Object is already in the bin")
        if obj.is_elastic:
            raise ValueError("Elastic objects should not be pushed into the bin")
        
        # Effects
        obj.is_in_box = True
        print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if not obj.is_in_box:
            raise ValueError("Object is not in the bin")
        if not self.robot_handempty:
            raise ValueError("Robot hand is not empty")
        
        # Effects
        self.state_holding(obj)
        obj.is_in_box = False
        self.state_handempty()
        print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=False, is_fragile=False, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_soft=False, is_elastic=True, is_fragile=False, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_soft=False, is_elastic=True, is_fragile=False, is_in_box=True, is_packable=True)
object3 = Object(index=3, name='white_1D_linear', color='white', shape='1D_linear', object_type='obj', is_soft=False, is_elastic=False, is_fragile=True, is_in_box=True, is_packable=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_soft=False, is_elastic=False, is_fragile=False, is_in_box=False, is_packable=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # object0 (brown_3D_cuboid) should be in the box
    # object1 (blue_1D_ring) should be on the platform
    # object2 (transparent_3D_cylinder) should be in the box (already in the box)
    # object3 (white_1D_linear) should be in the box (already in the box)
    # object4 (white_box) should remain as it is (no action needed)

    # Initialize the robot
    robot = Robot()

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step 1: Pick and place the brown_3D_cuboid into the box
    robot.pick(object0, object4)
    robot.place(object0, object4)

    # Step 2: Push the blue_1D_ring onto the platform
    robot.push(object1, object4)

    # after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box (followed)
    # Rule 2: When placing a 1D object in the bin, the soft object must be in the bin before (followed, but not needed as we are pushing the 1D object to the platform)
    # Rule 3: If there is an elastic object, push the object not in the bin, but on the platform (followed, blue_1D_ring is elastic and pushed to the platform)

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == False

    print("All objects are in their goal states.")
