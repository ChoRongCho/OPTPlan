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
    is_foldable: bool
    
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
        # Preconditions
        if self.robot_handempty and not obj.in_bin:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.in_bin = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and not obj.in_bin:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

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
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=True, 
    init_pose='out_box', 
    in_bin=False
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
    is_foldable=False, 
    init_pose='out_box', 
    in_bin=False
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_bin=False
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
    is_foldable=False, 
    init_pose='box', 
    in_bin=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in bin, not pushed, not folded
    # object1: out_box, not in bin, not pushed, not folded
    # object2: out_box, not in bin, not pushed, not folded
    # object3: in box, in bin, not pushed, not folded

    # Goal State:
    # object0: in bin, folded, in_bin_objects [1, 2]
    # object1: in bin, not folded, in_bin_objects [0, 2]
    # object2: not in bin, not folded, in_bin_objects []
    # object3: in box, in bin, not pushed, not folded, in_bin_objects [0, 1]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place elastic objects (object1 and object2) in the bin first
    # 2. Fold the foldable object (object0) after elastic objects are in the bin
    # 3. Place the folded object (object0) in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place elastic objects in the bin
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fold the foldable object
    robot.fold(object0, box)
    
    # Place the folded object in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Avoid handling and moving any box - The box (object3) is not moved or handled.
    # Rule 2: If there is a foldable object, fold the object at the platform not in the bin - The foldable object (object0) is folded before placing it in the bin.
    # Rule 3: When fold a foldable object, the elastic object must be in the bin - Elastic objects (object1 and object2) are placed in the bin before folding the foldable object (object0).
    # Rule 4: When place a fragile objects, the soft objects must be in the bin - The foldable object (object0) is placed in the bin after the elastic objects (object1 and object2).

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_bin == True
    assert object0.folded == True
    assert object1.in_bin == True
    assert object2.in_bin == True
    assert object3.in_bin == True
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    print("All task planning is done")
