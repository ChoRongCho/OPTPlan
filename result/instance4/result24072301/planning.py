from dataclasses import dataclass, field
from typing import List

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
    in_bin_objects: List[int] = field(default_factory=list)
    
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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and obj.in_box and not self.robot_handempty:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj.index)
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj.index in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj.index)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
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
    # Initial state:
    # object0: out_box, not in_box
    # object1: out_box, not in_box
    # object2: in_box, not out_box, not folded
    # object3: out_box, not in_box (box itself)

    # Final state:
    # object0: in_box, not out_box
    # object1: in_box, not out_box
    # object2: in_box, not out_box, folded
    # object3: out_box, not in_box (box itself)

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. You should never pick and place a box.
    # 2. When fold a object, the object must be foldable.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Pick and place blue_2D_ring (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place white_2D_ring (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fold yellow_2D_rectangle (object2) in the box
    robot.fold(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - object0 and object1 need to be picked and placed into the box to satisfy the goal state.
    # - object2 is already in the box but needs to be folded to satisfy the goal state.
    # - object3 is the box itself and should not be picked or placed.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_box == False
    print("All task planning is done")
