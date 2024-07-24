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
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # Object physical properties
    in_box: bool
    can_be_packed: bool


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
        if self.robot_handempty and not obj.in_box and obj.can_be_packed:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.can_be_packed:
            # Effects
            self.state_handempty()
            obj.in_box = True
            if bin.in_bin_objects is None:
                bin.in_bin_objects = []
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules and ensure proper state transitions for the bin_packing task. 
# The 'pick' action ensures that the robot can only pick objects that are not already in the bin and can be packed. 
# The 'place' action ensures that the robot can only place objects it is holding into the bin. 
# The 'push' and 'fold' actions require the robot's hand to be empty and the object to be in the bin, ensuring logical consistency. 
# The 'out' action allows the robot to remove objects from the bin, updating the states accordingly. 
# These actions ensure that the robot follows the rules and maintains a consistent state throughout the bin_packing task.

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
    in_bin_objects=None, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True, 
    in_box=False, 
    can_be_packed=True
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
)

object2 = Object(
    index=2, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
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
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=True, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, can_be_packed=True
    # object1: out_box, can_be_packed=True
    # object2: out_box, can_be_packed=True
    # object3: in_box, can_be_packed=False

    # Goal state:
    # object0: in_box
    # object1: in_box
    # object2: out_box
    # object3: in_box with [object0, object1]

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: you should never pick and place a box
    # Rule 4: when a rigid object is not in the bin at the initial state, pick a rigid object first

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Make an action sequence
    # According to Rule 4, pick the rigid object first
    robot.pick(object1, box)
    robot.place(object1, box)

    # Then pick and place the soft object
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: The robot actions are designed to follow the given rules and ensure proper state transitions for the bin_packing task.
    # The 'pick' action ensures that the robot can only pick objects that are not already in the bin and can be packed.
    # The 'place' action ensures that the robot can only place objects it is holding into the bin.
    # These actions ensure that the robot follows the rules and maintains a consistent state throughout the bin_packing task.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object0 in object3.in_bin_objects
    assert object1 in object3.in_bin_objects
    print("All task planning is done")
