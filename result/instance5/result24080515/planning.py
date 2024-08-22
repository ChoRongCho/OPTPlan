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
        # Preconditions: Object is not in the bin, robot hand is empty
        if not obj.in_box and self.robot_handempty:
            # Effects: Robot is holding the object, object is not in the bin
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot is holding the object, soft objects should be in the box if any
        if self.robot_now_holding == obj and all(o.in_box for o in bin.in_bin_objects if o.is_soft):
            # Effects: Object is in the bin, robot hand is empty
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Object is soft, robot hand is empty
        if obj.is_soft and self.robot_handempty:
            # Effects: Object is pushed
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Object is foldable, robot hand is empty
        if obj.is_elastic and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object is in the bin
        if obj in bin.in_bin_objects:
            # Effects: Object is not in the bin, robot hand is empty
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
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
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    is_fragile=False
)

object1 = Object(
    index=1, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=False, 
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

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
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
    # object3: box, not pushed, not folded, not in box, in_bin_objects=[]
    
    # Final State:
    # object0: in_box, not pushed, not folded, in box
    # object1: in_box, not pushed, not folded, in box
    # object2: in_box, not pushed, not folded, in box
    # object3: box, not pushed, not folded, not in box, in_bin_objects=[object0, object1, object2]
    
    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place the soft object (object0) in the box first.
    # 2. Place the other objects (object1 and object2) in the box.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Pick and place the soft object first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the next object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # The transparent_3D_cylinder is already in the box, no need to pick and place it again
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # 2. The other objects (object1 and object2) are placed in the box after the soft object.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object0, object1, object2]
    
    print("All task planning is done")
