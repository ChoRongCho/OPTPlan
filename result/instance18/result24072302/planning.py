from dataclasses import dataclass
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
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: List[int]
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool
    
    # Object physical properties
    is_elastic: bool
    is_rigid: bool
    is_soft: bool


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
        if self.robot_handempty and obj.out_box:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            if obj.is_soft and any(o.is_elastic for o in bin.in_bin_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj.index)
                print(f"Place {obj.name} in {bin.name}")
            elif obj.is_rigid and any(o.is_soft for o in bin.in_bin_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj.index)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} due to rule constraints")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj.index in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj.index)
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
    in_box=False, 
    out_box=True, 
    is_elastic=True, 
    is_rigid=False, 
    is_soft=True
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
    in_box=False, 
    out_box=True, 
    is_elastic=True, 
    is_rigid=False, 
    is_soft=False
)

object2 = Object(
    index=2, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    out_box=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_soft=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[2], 
    in_box=False, 
    out_box=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box
    # object1: out_box
    # object2: in_box
    # object3: box (contains object2)

    # Goal State
    # object0: in_bin
    # object1: out_box
    # object2: out_box
    # object3: box (empty)

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: avoid handling and moving any box
    # Rule 2: when place a soft object, the elastic object must be in the bin
    # Rule 3: when place a rigid objects, the soft objects must be in the bin
    # Rule 4: when a rigid object in the bin at the initial state, out of the rigid object first

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Fourth, after making all actions, fill your reasons according to the rules
    # Step 1: Out the rigid object (object2) from the box (Rule 4)
    robot.out(object2, box)

    # Step 2: Pick the soft object (object0)
    robot.pick(object0, box)

    # Step 3: Place the soft object (object0) in the box (Rule 2)
    robot.place(object0, box)

    # Step 4: Pick the rigid object (object2)
    robot.pick(object2, box)

    # Step 5: Place the rigid object (object2) in the box (Rule 3)
    robot.place(object2, box)

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == False
    print("All task planning is done")
