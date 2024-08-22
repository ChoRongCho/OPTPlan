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
    
    # Object physical properties 
    is_soft: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_fragile: bool


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
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            if obj.is_fragile or not obj.is_soft:
                if any(o.is_soft and not o.in_box for o in bin.in_bin_objects):
                    print(f"Cannot place {obj.name} because soft objects are not in the box")
                    return
            print(f"Place {obj.name in bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

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
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    is_fragile=False
)

object1 = Object(
    index=1, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=True, 
    in_box=False, 
    is_fragile=False
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
    is_soft=False, 
    is_elastic=True, 
    in_box=True, 
    is_fragile=False
)

white_box = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object2], 
    is_soft=False, 
    is_elastic=False, 
    in_box=False, 
    is_fragile=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in box
    # object1: out_box, not pushed, not folded, not in box
    # object2: in_box, not pushed, not folded, in box
    # white_box: contains object2

    # Goal State:
    # object0: in_box, not pushed, not folded, in box
    # object1: in_box, not pushed, not folded, in box
    # object2: in_box, not pushed, not folded, in box
    # white_box: contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick object0 (yellow_3D_cuboid)
    # 2. Place object0 in white_box
    # 3. Push object0 (since it is soft)
    # 4. Pick object1 (transparent_2D_circle)
    # 5. Place object1 in white_box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Pick object0: No precondition for picking
    # - Place object0: No soft objects in the box before placing
    # - Push object0: It is soft and already in the box
    # - Pick object1: No precondition for picking
    # - Place object1: Soft object (object0) is already in the box

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object0 in white_box.in_bin_objects
    assert object1 in white_box.in_bin_objects
    assert object2 in white_box.in_bin_objects
    print("All task planning is done")
