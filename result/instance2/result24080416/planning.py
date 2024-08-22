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
    is_foldable: bool
    is_fragile: bool
    is_rigid: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        # Preconditions: Object is out of the box and robot hand is empty
        if obj.out_box and self.robot_handempty:
            # Effects: Robot is holding the object, object is no longer out of the box
            self.state_holding(obj)
            obj.out_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Effects: Object is in the box, robot hand is empty
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Object is in the box, robot hand is empty, object is soft
        if obj.in_box and self.robot_handempty and obj.is_elastic:
            # Effects: Object is pushed
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Object is foldable, robot hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object is in the box
        if obj.in_box:
            # Effects: Object is out of the box, robot is holding the object
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_holding(obj)
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
    is_foldable=False, 
    is_fragile=False, 
    is_rigid=True, 
    is_elastic=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
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
    is_foldable=True, 
    is_fragile=True, 
    is_rigid=False, 
    is_elastic=False, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object2], 
    is_foldable=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: in_box, not folded
    # object3: contains object2

    # Goal State:
    # object0: in_box
    # object1: in_box
    # object2: in_box, folded
    # object3: contains object2, object0, object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place the soft object (object1) in the box first.
    # 2. Place the rigid object (object0) in the box.
    # 3. Fold the foldable object (object2) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence:
    # 1. Pick object1 (soft object)
    robot.pick(object1, box)
    # 2. Place object1 in the box
    robot.place(object1, box)
    # 3. Pick object0 (rigid object)
    robot.pick(object0, box)
    # 4. Place object0 in the box
    robot.place(object0, box)
    # 5. Fold object2 (foldable object)
    robot.fold(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object1) first as per the rule.
    # - Placed the rigid object (object0) after the soft object.
    # - Folded the foldable object (object2) after placing it in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
