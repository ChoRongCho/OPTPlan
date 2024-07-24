from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: list
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_elastic: bool
    is_fragile: bool
    is_soft: bool
    in_box: bool


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.shape == '1D' and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} - No soft object in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_elastic and not obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and not obj.folded:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that the robot does not pick up objects named 'box' and only picks objects not already in the bin. The 'place' action checks for the presence of a soft object in the bin before placing a 1D object, adhering to the second rule. The 'push' action ensures that elastic objects are pushed only when they are not in the bin, following the third rule. The 'fold' action ensures that the robot's hand is empty before folding an object. The 'out' action allows the robot to remove objects from the bin and place them on the platform, ensuring the robot's hand is empty afterward. These actions ensure the robot operates within the constraints provided, maintaining the integrity of the bin-packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_fragile=False, 
    is_soft=True, 
    in_box=False
)

object1 = Object(
    index=1, 
    name='black_1D_linear', 
    color='black', 
    shape='1D_linear', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_fragile=True, 
    is_soft=False, 
    in_box=False
)

object2 = Object(
    index=2, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_fragile=False, 
    is_soft=False, 
    in_box=True
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object2], 
    is_elastic=False, 
    is_fragile=False, 
    is_soft=False, 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: yellow_3D_cuboid, not in box
    # object1: black_1D_linear, not in box
    # object2: transparent_3D_cylinder, in box
    # object3: white_box, contains object2

    # Goal State:
    # object0: yellow_3D_cuboid, not in box, pushed
    # object1: black_1D_linear, not in box
    # object2: transparent_3D_cylinder, not in box
    # object3: white_box, empty

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Out object2 from the box
    # 2. Push object0 (since it is elastic and not in the box)
    # 3. No need to place object1 in the box as it is not required in the goal state

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Out object2 from the box
    robot.out(object2, box)
    
    # Push object0
    robot.push(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The 'out' action is used to remove object2 from the box, as it is required to be out of the box in the goal state.
    # 2. The 'push' action is used to push object0, as it is elastic and not in the box, following rule 3.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == False
    assert object0.pushed == True
    assert object1.in_box == False
    assert object2.in_box == False
    assert object3.in_bin_objects == []
    print("All task planning is done")
