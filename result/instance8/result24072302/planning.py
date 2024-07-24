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
    is_packed: bool
    
    # Object physical properties 
    is_elastic: bool
    is_soft: bool
    is_foldable: bool


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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_elastic or any(o.is_elastic for o in bin.in_bin_objects):
                if obj.is_elastic or any(o.color == 'blue' for o in bin.in_bin_objects):
                    # Effects
                    self.state_handempty()
                    obj.in_box = True
                    obj.is_packed = True
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot place {obj.name}: No blue object in bin")
            else:
                print(f"Cannot place {obj.name}: No elastic object in bin")
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
        if self.robot_handempty and obj.is_foldable and obj.in_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.is_packed = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_soft=False, is_foldable=False
)

object1 = Object(
    index=1, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=False, is_soft=True, is_foldable=True
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_soft=False, is_foldable=True
)

object3 = Object(
    index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3], in_box=False, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given code

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Never attempt to pick up and set down an object named box
    # 2. When placing a rigid object in the bin, an elastic object must be in the bin before
    # 3. When placing an elastic object, a blue object must be in the bin before

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Make an action sequence
    # Step 1: Place blue_1D_linear (elastic and blue) in the bin
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 2: Place transparent_3D_cylinder (elastic) in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Place black_2D_ring (rigid) in the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Out yellow_2D_rectangle from the box
    robot.out(object3, box)

    # Step 5: Place yellow_2D_rectangle (rigid) in the bin
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Placed blue_1D_linear first because it is blue and elastic, satisfying the condition for placing other elastic objects.
    # - Placed transparent_3D_cylinder next because it is elastic and a blue object is already in the bin.
    # - Placed black_2D_ring next because it is rigid and an elastic object is already in the bin.
    # - Removed yellow_2D_rectangle from the box to place it in the bin, as it is rigid and an elastic object is already in the bin.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == False
    print("All task planning is done")
