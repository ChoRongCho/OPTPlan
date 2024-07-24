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
    is_fragile: bool
    
    # Object physical properties 
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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_fragile:
                if any(o.is_elastic for o in bin.in_bin_objects):
                    print(f"Place {obj.name in bin.name}")
                    bin.in_bin_objects.append(obj)
                    obj.in_box = True
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} in {bin.name} because no elastic object in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that the robot does not pick up objects named 'box' and only picks objects not already in the bin. The 'place' action checks for the presence of an elastic object in the bin before placing a fragile object, adhering to the second rule. The 'out' action ensures that rigid objects are removed and replaced in the bin as per the third rule. The 'push' and 'fold' actions require the robot's hand to be empty, ensuring that the robot is not holding any object while performing these actions. This design ensures that the robot's actions are consistent with the rules and the state of the objects and the bin.

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
    in_box=False, 
    is_fragile=False, 
    is_elastic=True, 
    is_soft=True
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_fragile=False, 
    is_elastic=True, 
    is_soft=True
)

object2 = Object(
    index=2, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_fragile=False, 
    is_elastic=True, 
    is_soft=True
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
    is_fragile=False, 
    is_elastic=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box
    # object1: out_box
    # object2: out_box
    # object3: in_box (white_box)

    # Goal State
    # object0: in_box
    # object1: out_box
    # object2: in_box
    # object3: in_box (white_box)

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Never attempt to pick up and set down an object named box.
    # 2. Do not place a fragile object if there is no elastic object in the bin.
    # 3. When a rigid object is in the bin at the initial state, out of the rigid object and replace it into the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Make an action sequence
    # Step 1: Out the rigid object (if any) and replace it into the bin
    # In this case, there is no rigid object initially in the bin, so we skip this step.

    # Step 2: Pick and place objects into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The robot does not attempt to pick up or set down the object named 'box'.
    # 2. The objects being placed are not fragile, so no need to check for elastic objects in the bin.
    # 3. There was no rigid object in the bin initially, so no need to out and replace any object.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == True
    print("All task planning is done")
