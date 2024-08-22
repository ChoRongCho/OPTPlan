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
    is_transparent: bool


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
        # Preconditions
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
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
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=True, 
    in_box=False, 
    is_transparent=True
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
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    is_transparent=False
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
    is_soft=False, 
    is_elastic=True, 
    in_box=False, 
    is_transparent=True
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
    in_box=True, 
    is_transparent=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: in_box=False
    # object1: in_box=False
    # object2: in_box=False
    # object3: in_box=True, in_bin_objects=[]

    # Goal State:
    # object0: in_box=True
    # object1: in_box=True
    # object2: in_box=True
    # object3: in_box=True, in_bin_objects=[object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object1) first.
    # 2. Pick and place the remaining objects (object0 and object2).
    # 3. Push the soft object (object1) if needed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Pick and place the soft object first
    robot.pick(object1, box)
    robot.place(object1, box)

    # Pick and place the remaining objects
    robot.pick(object0, box)
    robot.place(object0, box)

    robot.pick(object2, box)
    robot.place(object2, box)

    # Push the soft object if needed
    robot.push(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object1) first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Placed the remaining objects (object0 and object2) after the soft object.
    # 3. Pushed the soft object (object1) to ensure it fits well in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object1, object0, object2]
    print("All task planning is done")
