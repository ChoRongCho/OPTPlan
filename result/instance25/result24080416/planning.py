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
    is_elastic: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and (not obj.is_soft or all(o.in_box for o in bin.in_bin_objects if o.is_soft)):
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj in bin.in_bin_objects:
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

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
    is_soft=True, 
    in_box=False, 
    is_packed=False
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
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    is_packed=False
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
    is_soft=False, 
    in_box=True, 
    is_packed=False
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
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not pushed, not folded, not in box, not packed
    # object1: out_box, not pushed, not folded, not in box, not packed
    # object2: in_box, not pushed, not folded, in box, not packed
    # white_box: contains object2

    # Goal state:
    # object0: in_box, not pushed, not folded, in box, packed
    # object1: in_box, not pushed, not folded, in box, packed
    # object2: in_box, not pushed, not folded, in box, packed
    # white_box: contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the soft object (object0) into the box first.
    # 2. Pick and place the rigid object (object1) into the box.
    # 3. Push the soft object (object0) to ensure it is properly placed.
    # 4. Mark all objects as packed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # Action sequence
    robot.pick(object0, box)  # Pick yellow_3D_cuboid
    robot.place(object0, box)  # Place yellow_3D_cuboid in white_box
    robot.pick(object1, box)  # Pick transparent_2D_circle
    robot.place(object1, box)  # Place transparent_2D_circle in white_box
    robot.push(object0, box)  # Push yellow_3D_cuboid
    object0.is_packed = True  # Mark yellow_3D_cuboid as packed
    object1.is_packed = True  # Mark transparent_2D_circle as packed
    object2.is_packed = True  # Mark transparent_3D_cylinder as packed

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # 2. The rigid object (object1) is placed after the soft object.
    # 3. The soft object (object0) is pushed to ensure it is properly placed in the box.
    # 4. All objects are marked as packed to satisfy the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object0.is_packed == True
    assert object1.is_packed == True
    assert object2.is_packed == True
    assert set(box.in_bin_objects) == {object0, object1, object2}

    print("All task planning is done")
