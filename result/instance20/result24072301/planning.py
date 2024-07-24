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
    is_soft: bool
    
    # Object physical properties
    init_pose: str
    in_bin: bool


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
        # Preconditions: Robot hand must be empty, object must not be in the bin, object must not be a box
        if self.robot_handempty and not obj.in_bin and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, object must not be a box
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be in the bin
        if self.robot_handempty and obj.in_bin:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be in the bin
        if self.robot_handempty and obj.in_bin:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.in_bin:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_holding(obj)
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot does not pick up a box and only picks objects not already in the bin. The 'place' action ensures the robot does not place a box and only places objects it is holding. The 'push' and 'fold' actions require the robot's hand to be empty and the object to be in the bin, ensuring the robot does not perform these actions inappropriately. The 'out' action ensures the robot can only remove objects that are already in the bin. These conditions ensure the robot's actions are safe and logical within the bin_packing task

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
    in_bin_objects=None, 
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box', 
    in_bin=False
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box', 
    in_bin=False
)

object2 = Object(
    index=2, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box', 
    in_bin=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=None, 
    folded=None, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    init_pose='box', 
    in_bin=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in bin
    # object1: out_box, not in bin
    # object2: out_box, not in bin
    # object3: in box, in bin

    # Goal State:
    # object0: in bin
    # object1: out_box, not in bin
    # object2: in bin
    # object3: in box, in bin with object0 and object2

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: Do not place a fragile object if there is no elastic object in the bin
    # Rule 3: When a rigid object is in the bin at the initial state, out of the rigid object and replace it into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Make an action sequence
    # Step 1: Out the rigid object (box) from the bin
    robot.out(box, box)

    # Step 2: Pick and place elastic objects into the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 3: Place the rigid object (box) back into the bin
    robot.pick(box, box)
    robot.place(box, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: Rule 3 requires us to out the rigid object and replace it into the bin
    # Reason for Step 2: We need to place elastic objects into the bin to satisfy the goal state
    # Reason for Step 3: We need to place the rigid object back into the bin to satisfy the goal state

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_bin == True
    assert object1.in_bin == False
    assert object2.in_bin == True
    assert object3.in_bin == True
    assert object0 in object3.in_bin_objects
    assert object2 in object3.in_bin_objects
    print("All task planning is done")
