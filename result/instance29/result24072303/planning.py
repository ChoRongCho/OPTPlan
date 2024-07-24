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
        if obj.object_type != 'box' and not obj.in_bin and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid or obj.is_elastic or (obj.is_soft and any(o.is_elastic for o in bin.in_bin_objects)):
                print(f"Place {obj.name in bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_bin = True
                self.state_handempty()
            else:
                print(f"Cannot Place {obj.name} due to missing elastic object in bin")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and not any(o.is_rigid or o.is_fragile for o in bin.in_bin_objects):
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable and any(o.is_fragile for o in bin.in_bin_objects):
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_bin and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_holding(obj)
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to adhere to the given rules for the bin_packing task. The preconditions ensure that actions are only performed when the state of the robot and objects meet specific criteria, such as the robot's hand being empty or the object not being a box. The effects update the state of the robot and objects to reflect the changes caused by the actions. This approach ensures that the robot operates within the constraints of the task, such as not picking up or setting down boxes, folding objects only when fragile objects are in the bin, and ensuring elastic objects are present before placing fragile objects

    def dummy(self):
        pass


 # Object Initial State
from dataclasses import dataclass
from typing import List

@dataclass
class Object:
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    pushed: bool
    folded: bool
    in_bin_objects: List[int]
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    init_pose: str
    in_bin: bool

# Initialize objects
object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_soft=False, init_pose='out_box', in_bin=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_soft=True, init_pose='out_box', in_bin=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_soft=True, init_pose='out_box', in_bin=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_soft=False, init_pose='box', in_bin=True)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in bin
    # object1: out_box, not in bin
    # object2: out_box, not in bin
    # object3: in_box, in bin

    # Goal State:
    # object0: out_box, not in bin
    # object1: in_box, in bin
    # object2: in_box, in bin
    # object3: in_box, in bin with objects [1, 2]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick white_3D_cylinder (object1)
    # 2. Place white_3D_cylinder (object1) in white_box (object3)
    # 3. Pick red_3D_polyhedron (object2)
    # 4. Push red_3D_polyhedron (object2) in white_box (object3)
    # 5. Place red_3D_polyhedron (object2) in white_box (object3)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.push(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Pick white_3D_cylinder (object1) because it is not in the bin and the robot's hand is empty.
    # 2. Place white_3D_cylinder (object1) in white_box (object3) because it is elastic and can be placed in the bin.
    # 3. Pick red_3D_polyhedron (object2) because it is not in the bin and the robot's hand is empty.
    # 4. Push red_3D_polyhedron (object2) in white_box (object3) because it is soft and there are no rigid or fragile objects in the bin.
    # 5. Place red_3D_polyhedron (object2) in white_box (object3) because it is soft and there is already an elastic object in the bin.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_bin == False
    assert object1.in_bin == True
    assert object2.in_bin == True
    assert object3.in_bin == True
    assert object3.in_bin_objects == [object1, object2]
    print("All task planning is done")
