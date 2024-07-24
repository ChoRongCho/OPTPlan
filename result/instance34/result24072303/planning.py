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
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # Object physical properties
    init_pose: str


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
        if self.robot_handempty and obj.object_type != 'box' and obj.index not in bin.in_bin_objects:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            bin.in_bin_objects.append(obj.index)
            self.state_handempty()
            print(f"Place {obj.name in bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.index in bin.in_bin_objects:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.index in bin.in_bin_objects:
            bin.in_bin_objects.remove(obj.index)
            self.state_holding(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_soft=True, init_pose='out_box')
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_soft=False, init_pose='out_box')
object2 = Object(index=2, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_soft=False, init_pose='in_box')
object3 = Object(index=3, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_soft=True, init_pose='in_box')
object4 = Object(index=4, name='white_1D_linear', color='white', shape='1D_linear', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=True, is_soft=False, init_pose='in_box')
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[2, 3, 4], is_rigid=False, is_elastic=False, is_soft=False, init_pose='box')

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given data

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Don't pick and place a box called bin
    # 2. When fold an object, the object must be foldable
    # 3. When place a rigid object in the bin, the soft objects must be in the bin before

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object5

    # c) Make an action sequence
    # Step 1: Place all soft objects in the bin first
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 2: Place all rigid objects in the bin after soft objects
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 3: Ensure all objects are in the bin
    # Note: Objects 2, 3, and 4 are already in the bin

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Object 0 (soft) is placed first to satisfy rule 3
    # - Object 1 (rigid) is placed after all soft objects are in the bin
    # - Objects 2, 3, and 4 are already in the bin, so no action is needed for them

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.index in box.in_bin_objects
    assert object1.index in box.in_bin_objects
    assert object2.index in box.in_bin_objects
    assert object3.index in box.in_bin_objects
    assert object4.index in box.in_bin_objects
    print("All task planning is done")
