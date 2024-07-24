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
    is_foldable: bool = False

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
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and (bin.object_type == 'box' or not bin.is_in_box):
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
        if self.robot_handempty and obj.is_foldable:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, is_in_box=False)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, is_in_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> in_box
    # object1 (white_3D_cylinder) -> out_box
    # object2 (yellow_2D_rectangle) -> in_box
    # object3 (white_box) -> box (unchanged)

    # Initialize the robot
    robot = Robot()

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step 1: Pick out the rigid object (white_box) from the box
    robot.pick_out(object3, object3)  # This action is not valid as per rule 1, so we skip it

    # Step 2: Pick and place yellow_3D_cuboid into the box
    robot.pick(object0, object3)
    robot.place(object0, object3)

    # Step 3: Pick and place yellow_2D_rectangle into the box
    robot.pick(object2, object3)
    robot.place(object2, object3)

    # Step 4: No need to handle white_3D_cylinder as it should remain out of the box

    # after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. We never attempt to pick up and set down an object named box.
    # 2. We do not place a fragile object if there is no elastic object in the bin (no fragile objects in this scenario).
    # 3. We did not need to handle rigid objects as there were none initially in the box.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    assert object3.is_in_box == True

    print("All objects are in their goal states.")
