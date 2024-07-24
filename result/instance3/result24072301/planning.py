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
    in_box: bool
    is_heavy: bool
    
    # Object physical properties 
    is_rigid: bool
    is_elastic: bool
    is_soft: bool


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
        if self.robot_handempty and not obj.in_box and obj.is_rigid:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name in bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that only rigid objects not already in the bin can be picked up, adhering to the rule that rigid objects should be picked first if they are not in the bin. The 'place' action ensures that only objects (not boxes) can be placed in the bin, following the rule that boxes should not be picked and placed. The 'push' and 'fold' actions require the robot's hand to be empty and the object to be in the bin, ensuring that these actions are only performed on objects already in the bin. The 'out' action allows objects to be removed from the bin and placed on a platform, ensuring the robot's hand is empty after the action. These actions and their preconditions and effects are designed to facilitate efficient bin packing while adhering to the specified rules.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False
)

object2 = Object(
    index=2, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_heavy=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in bin, not heavy, not rigid, not elastic, soft
    # object1: out_box, not pushed, not folded, not in bin, not heavy, rigid, not elastic, not soft
    # object2: out_box, not pushed, not folded, not in bin, not heavy, not rigid, elastic, not soft
    # object3: in_box, not pushed, not folded, in bin, not heavy, not rigid, not elastic, not soft

    # Goal State:
    # object0: in_bin, not pushed, not folded, not in bin, not heavy, not rigid, not elastic, soft
    # object1: in_bin, not pushed, not folded, not in bin, not heavy, rigid, not elastic, not soft
    # object2: out_box, not pushed, not folded, not in bin, not heavy, not rigid, elastic, not soft
    # object3: in_box, not pushed, not folded, in bin, not heavy, not rigid, not elastic, not soft

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: You should never pick and place a box
    # Rule 4: When a rigid object is not in the bin at the initial state, pick a rigid object first

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # According to Rule 4, pick the rigid object first
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.push(object1, box)

    # Now pick the soft object and place it in the bin
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: 
    # 1. Picked and placed the rigid object (yellow_3D_cylinder) first as per Rule 4.
    # 2. Then picked and placed the soft object (red_3D_polyhedron) in the bin.
    # 3. Ensured that the box (white_box) was not picked or placed as per Rule 1.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    print("All task planning is done")
