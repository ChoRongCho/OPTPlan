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
    is_foldable: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    can_be_packed: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.can_be_packed:
            # Effects
            self.state_handempty()
            obj.in_box = True
            if bin.in_bin_objects is None:
                bin.in_bin_objects = []
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
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
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=False, 
    is_foldable=False, 
    is_soft=True, 
    in_box=False, 
    can_be_packed=True
)

object1 = Object(
    index=1, 
    name='green_2D_circle', 
    color='green', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=True, 
    is_foldable=True, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
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
    is_foldable=False, 
    is_soft=False, 
    in_box=True, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: red_3D_polyhedron, out_box, is_soft, can_be_packed
    # object1: green_2D_circle, out_box, is_foldable, is_rigid, can_be_packed
    # object2: white_box, box, in_bin_objects=[]

    # Goal State:
    # object0: red_3D_polyhedron, in_box, is_soft, can_be_packed
    # object1: green_2D_circle, in_box, is_foldable, is_rigid, can_be_packed, folded
    # object2: white_box, box, in_bin_objects=[object0, object1]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the soft object (object0) first.
    # 2. Fold the foldable object (object1).
    # 3. Pick and place the rigid object (object1).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # Action sequence
    # 1. Pick the soft object (object0)
    robot.pick(object0, box)
    # 2. Place the soft object (object0) in the box
    robot.place(object0, box)
    # 3. Fold the foldable object (object1)
    robot.fold(object1, box)
    # 4. Pick the rigid object (object1)
    robot.pick(object1, box)
    # 5. Place the rigid object (object1) in the box
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Placed the soft object first as per the rule.
    # - Folded the foldable object before placing it in the box.
    # - Placed the rigid object after the soft object was already in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object1.folded == True
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")
