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
    is_flexible: bool
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
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
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
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            print(f"Out {obj.name} from {bin.name}")
    def dummy(self):
        pass


object0 = Object(
    index=0, 
    name='blue_1D_ring', 
    color='blue', 
    shape='1D_ring', 
    object_type='obj', 
    is_elastic=True, 
    is_flexible=True, 
    is_foldable=False, 
    is_in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='white_1D_ring', 
    color='white', 
    shape='1D_ring', 
    object_type='obj', 
    is_elastic=True, 
    is_flexible=True, 
    is_foldable=False, 
    is_in_box=False, 
    is_packable=True
)

object2 = Object(
    index=2, 
    name='brown_2D_rectangle', 
    color='brown', 
    shape='2D_rectangle', 
    object_type='obj', 
    is_elastic=False, 
    is_flexible=False, 
    is_foldable=True, 
    is_in_box=True, 
    is_packable=True
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    is_elastic=False, 
    is_flexible=False, 
    is_foldable=False, 
    is_in_box=False, 
    is_packable=False
)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Define the bin (box)
    bin = object3

    # Action sequence to achieve the goal state
    # 1. Pick blue_1D_ring and place it in the white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick white_1D_ring and place it in the white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 3. The brown_2D_rectangle is already in the box, no action needed

    # Final state of each object
    print(f"Final state of {object0.name}: is_in_box = {object0.is_in_box}")
    print(f"Final state of {object1.name}: is_in_box = {object1.is_in_box}")
    print(f"Final state of {object2.name}: is_in_box = {object2.is_in_box}")
    print(f"Final state of {object3.name}: is_in_box = {object3.is_in_box}")

    # Check if the goal state is satisfied
    goal_state = [
        (object0.is_in_box, True),
        (object1.is_in_box, True),
        (object2.is_in_box, True),
        (object3.is_in_box, False)
    ]

    all_satisfied = all([current == goal for current, goal in goal_state])
    print(f"Goal state satisfied: {all_satisfied}")

    # Reasons according to the rules:
    # 1. We did not pick and place the box (white_box).
    # 2. We did not fold any object since none of the actions required folding.
    # 3. The brown_2D_rectangle is already in the box and is foldable, but no folding action was needed.
