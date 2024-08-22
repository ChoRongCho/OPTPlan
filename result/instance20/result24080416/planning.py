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
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
        if self.robot_now_holding == obj and obj.object_type == 'obj':
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.is_soft:
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
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    is_packed=False
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=True, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True, 
    in_box=False, 
    is_packed=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: [object0, object1, object2]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft objects first (object0 and object2)
    # 2. Fold the foldable object (object2)
    # 3. Pick and place the rigid object (object1)
    # 4. Push the soft objects if needed (object0)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object2, box)
    robot.fold(object2, box)
    robot.place(object2, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.push(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place the soft objects first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Fold the foldable object to satisfy the rule: "Fold objects only if they are foldable."
    # 3. Pick and place the rigid object after the soft objects are in the box.
    # 4. Push the soft objects after placing items in the bin to satisfy the rule: "Only push soft objects after placing items in the bin."
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object0, object1, object2]
    
    print("All task planning is done")
