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
        if obj.object_type != 'box' and self.robot_now_holding == obj:
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
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")
            self.state_handempty()

    def dummy(self):
        pass


# Create objects based on the initial state
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_out_box=True)
object1 = Object(index=1, name='black_3D_circle', color='black', shape='3D_circle', object_type='obj', is_soft=True, is_out_box=True)
object2 = Object(index=2, name='brown_2D_flat_rectangle', color='brown', shape='2D_flat_rectangle', object_type='obj', is_elastic=True, is_in_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

# Initialize the robot
robot = Robot()

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # | Index | Name                    | Shape              | Color  | Object Type | Is Rigid | Is Soft | Is Elastic | Is In Box | Is Out Box |
    # |-------|-------------------------|--------------------|--------|-------------|----------|---------|------------|-----------|------------|
    # | 0     | yellow_3D_cylinder      | 3D_cylinder        | yellow | obj         | True     | False   | False      | True      | False      |
    # | 1     | black_3D_circle         | 3D_circle          | black  | obj         | False    | True    | False      | True      | False      |
    # | 2     | brown_2D_flat_rectangle | 2D_flat_rectangle  | brown  | obj         | False    | False   | True       | True      | False      |
    # | 3     | white_box               | box                | white  | box         | False    | False   | False      | True      | False      |

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    
    # Step 1: Pick the yellow_3D_cylinder and place it in the white_box
    robot.pick(object0, object3)
    robot.place(object0, object3)
    
    # Step 2: Pick the black_3D_circle and fold it (since it is soft)
    robot.pick(object1, object3)
    robot.fold(object1, object3)
    
    # Step 3: Place the black_3D_circle in the white_box
    robot.place(object1, object3)
    
    # Step 4: Ensure the brown_2D_flat_rectangle is already in the white_box (no action needed)
    
    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. We never pick and place a box (Rule 1).
    # 2. When folding the black_3D_circle (soft object), the brown_2D_flat_rectangle (elastic object) is already in the bin (Rule 2).
    # 3. We do not place the black_3D_circle (fragile object) without ensuring the brown_2D_flat_rectangle (elastic object) is in the bin (Rule 3).

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == True and object2.is_out_box == False
    assert object3.is_in_box == True and object3.is_out_box == False

    print("All objects are correctly placed in the box.")
