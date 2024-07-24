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
        if self.robot_handempty and obj.index not in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid:
                if any(o.is_soft for o in bin.in_bin_objects):
                    # Effects
                    bin.in_bin_objects.append(obj.index)
                    self.state_handempty()
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
            else:
                # Effects
                bin.in_bin_objects.append(obj.index)
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.index in bin.in_bin_objects:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.index in bin.in_bin_objects:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.index in bin.in_bin_objects:
            # Effects
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
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='out_box'
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
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box'
)

object2 = Object(
    index=2, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True, 
    init_pose='in_box'
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
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='box'
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box
    # object1: out_box
    # object2: in_box
    # object3: box (contains object2)
    
    # Goal state:
    # object0: in_box
    # object1: in_box (pushed)
    # object2: out_box
    # object3: box (contains object0 and object1)
    
    # Second, using given rules and object's states, make a task planning strategy
    # 1. Push the white_3D_cylinder (object1) into the box (object3)
    # 2. Out the red_3D_polyhedron (object2) from the box (object3)
    # 3. Pick and place the white_3D_cylinder (object1) into the box (object3)
    # 4. Pick and place the black_3D_cylinder (object0) into the box (object3)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Push the white_3D_cylinder (object1) into the box (object3)
    robot.push(object1, box)
    
    # 2. Out the red_3D_polyhedron (object2) from the box (object3)
    robot.out(object2, box)
    
    # 3. Pick and place the white_3D_cylinder (object1) into the box (object3)
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 4. Pick and place the black_3D_cylinder (object0) into the box (object3)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.index in box.in_bin_objects
    assert object1.index in box.in_bin_objects
    assert object2.index not in box.in_bin_objects
    assert object3.in_bin_objects == [0, 1]
    print("All task planning is done")
