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
    out_box: bool


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
        if obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=True, 
    in_box=True, 
    out_box=False
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
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=False, in_bin_objects=[]

    # Goal State:
    # object0: out_box=False, in_box=True
    # object1: out_box=False, in_box=True
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Ensure the soft object (object2) is in the box.
    # 2. Pick and place the remaining objects (object0 and object1) in the box.
    # 3. Push the soft object (object2) to make space if needed.
    # 4. Fold the elastic object (object1) if needed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action Sequence:
    # 1. Pick object0 and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # 2. Pick object1 and place it in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # 3. Push the soft object (object2) to make space if needed
    robot.push(object2, box)

    # 4. Fold the elastic object (object1) if needed
    robot.fold(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The soft object (object2) is already in the box, so no need to place it.
    # - Pick and place object0 and object1 in the box.
    # - Push the soft object (object2) to make space if needed.
    # - Fold the elastic object (object1) if needed.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object0.out_box == False
    assert object1.out_box == False
    assert object2.out_box == False
    assert object3.out_box == False
    assert object3.in_bin_objects == [object0, object1, object2]

    print("All task planning is done")
