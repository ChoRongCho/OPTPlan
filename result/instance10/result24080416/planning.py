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
    is_fragile: bool
    is_rigid: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    init_pose: str
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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, soft objects should be in the box if placing fragile or rigid objects
        if self.robot_now_holding == obj:
            if (obj.is_fragile or obj.is_rigid) and any(o.is_soft and not o.in_box for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because soft objects are not in the box")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft, object must be in the bin
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=True, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_fragile=True, 
    is_rigid=True, 
    is_elastic=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=True, 
    init_pose='out_box', 
    in_box=False
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
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=False, 
    init_pose='box', 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box, not in_box
    # object1: out_box, not in_box
    # object2: out_box, not in_box
    # object3: box, in_box

    # Final State
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: box, in_box with [object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place the soft object (object2) in the box first.
    # 2. Place the fragile and rigid object (object1) in the box.
    # 3. Place the elastic object (object0) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    # 1. Pick and place the soft object (object2)
    robot.pick(object2, box)
    robot.place(object2, box)

    # 2. Pick and place the fragile and rigid object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)

    # 3. Pick and place the elastic object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for placing object2 first: Soft objects should be in the box before placing fragile or rigid objects.
    # Reason for placing object1 second: After soft object is placed, fragile and rigid objects can be placed.
    # Reason for placing object0 last: Elastic object can be placed after the above conditions are met.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object2, object1, object0]
    print("All task planning is done")
