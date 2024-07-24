from dataclasses import dataclass, field

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: list = field(default_factory=list)
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_elastic: bool = False
    is_foldable: bool = False
    
    # Object physical properties
    in_box: bool = False
    out_box: bool = True


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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.out_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj.in_box and obj.object_type != 'box':
            # Effects
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.object_type != 'box':
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and obj.in_box and obj.object_type != 'box':
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='blue_2D_ring', color='blue', shape='2D_ring', object_type='obj', in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_box=False, out_box=True)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: in_box
    # object3: out_box (box)

    # Goal State:
    # object0: out_box
    # object1: in_box
    # object2: in_box, folded
    # object3: out_box (box)

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. You should never pick and place a box.
    # 2. When fold an object, the object must be foldable.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence to achieve the goal state
    # 1. Pick white_2D_ring (object1)
    robot.pick(object1, box)
    
    # 2. Place white_2D_ring (object1) in the box
    robot.place(object1, box)
    
    # 3. Fold yellow_2D_rectangle (object2)
    robot.fold(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Pick and place actions are used to move objects into the box.
    # - Fold action is used to fold the foldable object (yellow_2D_rectangle).

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == False
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_box == False
    print("All task planning is done")
