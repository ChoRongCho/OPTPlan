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
    is_soft: bool = False
    
    # Object physical properties
    init_pose: str = 'out_box'
    in_bin: bool = False


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
        if self.robot_handempty and not obj.in_bin and obj.object_type == 'obj':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type == 'obj':
            # Effects
            self.state_handempty()
            obj.in_bin = True
            bin.in_bin_objects.append(obj.index)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_bin and obj.object_type == 'obj':
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.object_type == 'obj':
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_bin and obj.object_type == 'obj':
            # Effects
            self.state_holding(obj)
            obj.in_bin = False
            bin.in_bin_objects.remove(obj.index)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_elastic=True, is_soft=True, init_pose='out_box')
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, init_pose='out_box')
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', init_pose='box')

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in bin
    # object1: out_box, not in bin
    # object2: box, not in bin, in_bin_objects = []

    # Goal State:
    # object0: out_box, not in bin
    # object1: in bin
    # object2: box, in_bin_objects = [1]

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Avoid handling and moving any box
    # Rule 2: When fold an object, the object must be foldable
    # Rule 3: When fold a foldable object, the fragile object must be in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, out of the rigid object and replace it into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence to achieve the goal state
    # Pick the transparent_3D_cylinder (object1)
    robot.pick(object1, box)
    
    # Place the transparent_3D_cylinder (object1) in the white_box (box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - We picked and placed the transparent_3D_cylinder (object1) into the white_box (box) to satisfy the goal state.
    # - We did not handle or move the box itself, adhering to Rule 1.
    # - No folding was required, so Rules 2 and 3 are not applicable.
    # - There were no rigid objects in the bin initially, so Rule 4 is not applicable.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_bin == False
    assert object1.in_bin == True
    assert object2.in_bin_objects == [1]
    print("All task planning is done")