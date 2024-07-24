from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic Effect Robot Action Predicates for object_type = obj
    pushed: bool
    folded: bool
    
    # Bin Predicates for object_type = bin
    in_bin: list
    
    # Object physical properties predicates
    is_foldable: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_packed: bool
    is_outside: bool


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
        if obj.object_type != 'bin' and obj.is_outside and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_outside = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj and obj.object_type != 'bin':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            obj.is_packed = True
            obj.is_outside = False
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_foldable and obj in bin.in_bin:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable and obj.is_outside:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            obj.is_packed = False
            obj.is_outside = True
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=True, 
    is_rigid=False, 
    is_packed=False, 
    is_outside=True
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_rigid=True, 
    is_packed=False, 
    is_outside=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='bin', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_packed=False, 
    is_outside=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_2D_rectangle) should be pushed and in the bin
    # object1 (yellow_3D_cylinder) should be in the bin
    # object2 (white_box) should contain object0 and object1

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object2

    # c) Action sequence to achieve the goal state

    # Step 1: Pick the yellow_2D_rectangle (soft object)
    robot.pick(object0, bin)
    
    # Step 2: Place the yellow_2D_rectangle in the white_box
    robot.place(object0, bin)
    
    # Step 3: Push the yellow_2D_rectangle to make space
    robot.push(object0, bin)
    
    # Step 4: Pick the yellow_3D_cylinder (rigid object)
    robot.pick(object1, bin)
    
    # Step 5: Place the yellow_3D_cylinder in the white_box
    robot.place(object1, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. We first pick and place the soft object (yellow_2D_rectangle) into the bin.
    # 2. We push the soft object to make more space in the bin.
    # 3. We then pick and place the rigid object (yellow_3D_cylinder) into the bin.
    # This order ensures that the soft object is placed first and pushed to make space for the rigid object, satisfying the rules.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.is_packed == True
    assert object0.is_outside == False
    assert object0.pushed == True
    assert object1.is_packed == True
    assert object1.is_outside == False
    assert object2.in_bin == [object0, object1]
    print("All task planning is done")
