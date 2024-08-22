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
    is_fragile: bool
    
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
        # Preconditions: Object is not in the bin, robot hand is empty
        if not obj.in_box and self.robot_handempty:
            # Effects: Robot is holding the object, object is not in the bin
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot is holding the object, object is packable
        if self.robot_now_holding == obj and obj.is_packable:
            # Effects: Object is in the bin, robot hand is empty
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Object is in the bin, robot hand is empty, object is not rigid
        if obj.in_box and self.robot_handempty and not obj.is_rigid:
            # Effects: Object is pushed
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Object is foldable, robot hand is empty
        if obj.folded and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object is in the bin
        if obj in bin.in_bin_objects:
            # Effects: Object is not in the bin, robot hand is empty
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
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=False, 
    in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=True, 
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
    is_fragile=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    print("Initial State:")
    print(f"{object0.name}: In Box = {object0.in_box}, Is Packable = {object0.is_packable}")
    print(f"{object1.name}: In Box = {object1.in_box}, Is Packable = {object1.is_packable}")
    print(f"{object2.name}: In Box = {object2.in_box}, Is Packable = {object2.is_packable}, In Bin Objects = {object2.in_bin_objects}")

    # Goal State
    print("\nGoal State:")
    print(f"{object0.name}: In Box = True")
    print(f"{object1.name}: In Box = True")
    print(f"{object2.name}: In Box = True, In Bin Objects = [{object0.index}, {object1.index}]")

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the black_3D_cylinder (object0) in the white_box (object2)
    # 2. Pick and place the green_3D_cylinder (object1) in the white_box (object2)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Pick and place black_3D_cylinder
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place green_3D_cylinder
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The black_3D_cylinder (object0) is rigid and not fragile, so it can be placed in the box first.
    # 2. The green_3D_cylinder (object1) is rigid and fragile, and it can be placed in the box after the black_3D_cylinder.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")
