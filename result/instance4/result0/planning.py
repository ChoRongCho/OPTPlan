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
    is_elastic: bool
    is_foldable: bool

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_packable: bool


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
        if self.robot_handempty and obj.is_foldable:
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


object0 = Object(index=0, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_foldable=False, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_foldable=False, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_elastic=False, is_foldable=True, is_in_box=True, is_packable=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_elastic=False, is_foldable=False, is_in_box=True, is_packable=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal state:
    # blue_1D_ring: is_in_box = True
    # white_1D_ring: is_in_box = True
    # yellow_2D_rectangle: is_in_box = True
    # white_box: is_in_box = True (already in box, no action needed)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Plan:
    # 1. Pick blue_1D_ring
    # 2. Place blue_1D_ring in white_box
    # 3. Pick white_1D_ring
    # 4. Place white_1D_ring in white_box

    # Execute the plan
    robot.pick(object0, object3)  # Pick blue_1D_ring
    robot.place(object0, object3)  # Place blue_1D_ring in white_box

    robot.pick(object1, object3)  # Pick white_1D_ring
    robot.place(object1, object3)  # Place white_1D_ring in white_box

    # after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. We should never pick and place a box: We did not pick or place the white_box.
    # 2. When fold an object, the object must be foldable: No folding action was needed as all objects were packable without folding.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True, "blue_1D_ring is not in the box"
    assert object1.is_in_box == True, "white_1D_ring is not in the box"
    assert object2.is_in_box == True, "yellow_2D_rectangle is not in the box"
    assert object3.is_in_box == True, "white_box is not in the box"

    print("All objects are correctly packed in the box.")
