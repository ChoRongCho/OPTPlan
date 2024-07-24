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
    is_foldable: bool = False
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
        if self.robot_handempty and obj.is_foldable and not obj.is_in_box:
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


object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, is_elastic=False, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_foldable=False, is_elastic=True, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_foldable=False, is_elastic=True, is_in_box=False, is_fragile=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_foldable=False, is_elastic=False, is_in_box=True, is_fragile=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_2D_rectangle) -> in_box
    # object1 (white_1D_ring) -> in_box
    # object2 (transparent_2D_circle) -> out_box
    # object3 (white_box) -> in_box (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. Avoid handling and moving any box
    # 2. If there is a foldable object, fold the object at the platform not in the bin
    # 3. When fold a foldable object, the elastic object must be in the bin
    # 4. When place a fragile objects, the soft objects must be in the bin

    # Step-by-step action sequence:
    # 1. Place the elastic object (white_1D_ring) in the box
    robot.pick(object1, object3)
    robot.place(object1, object3)

    # 2. Fold the foldable object (yellow_2D_rectangle) at the platform
    robot.fold(object0, object3)

    # 3. Place the foldable object (yellow_2D_rectangle) in the box
    robot.pick(object0, object3)
    robot.place(object0, object3)

    # 4. Ensure the transparent_2D_circle remains out of the box (no action needed as it is already out)

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Rule 1: We avoided handling and moving the box (white_box).
    # - Rule 2: We folded the foldable object (yellow_2D_rectangle) at the platform.
    # - Rule 3: Before folding the foldable object, we ensured the elastic object (white_1D_ring) was in the box.
    # - Rule 4: There were no fragile objects to place, so this rule did not apply.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True, "yellow_2D_rectangle should be in the box"
    assert object1.is_in_box == True, "white_1D_ring should be in the box"
    assert object2.is_in_box == False, "transparent_2D_circle should be out of the box"
    assert object3.is_in_box == True, "white_box should be in the box"

    print("All objects are in their goal states.")
