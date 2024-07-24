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
    is_in_box: bool
    is_out_box: bool
    
    # Object physical properties
    is_rigid: bool
    is_elastic: bool
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
        if self.robot_handempty and obj.is_out_box:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            bin.in_bin_objects.append(obj.index)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box and obj.is_soft:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_in_box and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.index in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
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
    is_in_box=False, 
    is_out_box=True, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False
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
    is_in_box=False, 
    is_out_box=True, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True
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
    is_in_box=True, 
    is_out_box=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True
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
    is_in_box=False, 
    is_out_box=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    # object0: is_out_box=True, is_in_box=False
    # object1: is_out_box=True, is_in_box=False
    # object2: is_out_box=False, is_in_box=True
    # object3: in_bin_objects=[2]

    # Goal state
    # object0: is_out_box=False, is_in_box=True, pushed=True
    # object1: is_out_box=False, is_in_box=True, pushed=True
    # object2: is_out_box=True, is_in_box=False
    # object3: in_bin_objects=[0, 1]

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: It is prohibited to lift and relocate a container
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: If there is a soft object, push the object first

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Step 1: Out the red_3D_polyhedron (object2) from the box
    robot.out(object2, box)

    # Step 2: Pick the white_3D_cylinder (object1)
    robot.pick(object1, box)

    # Step 3: Place the white_3D_cylinder (object1) in the box
    robot.place(object1, box)

    # Step 4: Push the white_3D_cylinder (object1)
    robot.push(object1, box)

    # Step 5: Pick the black_3D_cylinder (object0)
    robot.pick(object0, box)

    # Step 6: Place the black_3D_cylinder (object0) in the box
    robot.place(object0, box)

    # Step 7: Push the black_3D_cylinder (object0)
    robot.push(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: The red_3D_polyhedron (object2) needs to be out of the box as per the goal state.
    # Reason for Step 2: The white_3D_cylinder (object1) needs to be placed in the box.
    # Reason for Step 3: The white_3D_cylinder (object1) needs to be in the box as per the goal state.
    # Reason for Step 4: The white_3D_cylinder (object1) is soft and needs to be pushed as per the goal state.
    # Reason for Step 5: The black_3D_cylinder (object0) needs to be placed in the box.
    # Reason for Step 6: The black_3D_cylinder (object0) needs to be in the box as per the goal state.
    # Reason for Step 7: The black_3D_cylinder (object0) is rigid, but it needs to be pushed as per the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.in_bin_objects == [0, 1]
    assert object0.pushed == True
    assert object1.pushed == True
    print("All task planning is done")
