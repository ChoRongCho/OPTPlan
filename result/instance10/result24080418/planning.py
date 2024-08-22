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
    is_fragile: bool
    is_soft: bool
    is_elastic: bool
    
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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, if object is fragile or rigid, soft objects should be in the box
        if self.robot_now_holding == obj:
            if (obj.is_fragile or obj.is_rigid) and any(o.is_soft and not o.in_box for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because soft objects are not in the box")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft and in the bin
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_foldable=False, 
    is_fragile=False, 
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    is_packed=False
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
    is_foldable=False, 
    is_fragile=True, 
    is_soft=False, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='transparent_3D_cuboid', 
    color='transparent', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_foldable=True, 
    is_fragile=False, 
    is_soft=False, 
    is_elastic=True, 
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
    is_rigid=False, 
    is_foldable=False, 
    is_fragile=False, 
    is_soft=False, 
    is_elastic=False, 
    in_box=True, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_bin_objects
    }
    
    # Goal State
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: [object0, object1, object2]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the foldable object (object2) and fold it.
    # 3. Pick and place the fragile and rigid object (object1).
    # 4. Push the soft object (object0) to ensure it is properly placed.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # Action Sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.fold(object2, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.push(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place the soft object (object0) first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # 2. Pick and place the foldable object (object2) and fold it to ensure it fits well in the box.
    # 3. Pick and place the fragile and rigid object (object1) after the soft object is already in the box.
    # 4. Push the soft object (object0) to ensure it is properly placed and does not obstruct other objects.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object0, object1, object2]
    
    print("All task planning is done")
