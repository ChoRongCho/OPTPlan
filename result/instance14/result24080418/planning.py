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
    is_rigid: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packable: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj.is_packable:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box and not obj.is_rigid:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable and not obj.is_rigid:
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
    name='white_3D_cone', 
    color='white', 
    shape='3D_cone', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    in_box=False, 
    is_packable=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: white_3D_cone, in_box=False, is_packable=True
    # object1: black_3D_cylinder, in_box=False, is_packable=True
    # object2: white_box, in_box=True, is_packable=False, in_bin_objects=[]

    # Goal State:
    # object0: white_3D_cone, in_box=True, is_packable=True
    # object1: black_3D_cylinder, in_box=True, is_packable=True
    # object2: white_box, in_box=True, is_packable=False, in_bin_objects=[object0, object1]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick object0 (white_3D_cone)
    # 2. Place object0 in object2 (white_box)
    # 3. Pick object1 (black_3D_cylinder)
    # 4. Place object1 in object2 (white_box)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Perform the actions
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # - Pick object0: No preconditions violated.
    # - Place object0: No soft objects to place first, object0 is packable.
    # - Pick object1: No preconditions violated.
    # - Place object1: No soft objects to place first, object1 is packable.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")
