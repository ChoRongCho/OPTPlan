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
    is_elastic: bool
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
        if self.robot_handempty and obj.is_elastic:
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
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    can_be_packed=True
)

object1 = Object(
    index=1, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
)

object2 = Object(
    index=2, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
)

object3 = Object(
    index=3, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=True, 
    is_elastic=True, 
    is_soft=False, 
    in_box=True, 
    can_be_packed=True
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_bin_objects
    }
    
    # Goal State
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        object4.name: [object0, object1, object2, object3]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (yellow_3D_cuboid) first.
    # 2. Place the remaining objects (blue_2D_ring, white_2D_ring, white_2D_circle).
    # 3. Push the soft object if necessary.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # c) Action sequence
    # Place yellow_3D_cuboid (soft object) first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Place blue_2D_ring
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Place white_2D_ring
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Place white_2D_circle (already in the box, no action needed)
    
    # Push the yellow_3D_cuboid (soft object) if necessary
    robot.push(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (yellow_3D_cuboid) first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Placed the remaining objects (blue_2D_ring, white_2D_ring, white_2D_circle) after the soft object.
    # 3. Pushed the soft object (yellow_3D_cuboid) after placing all items in the bin to satisfy the rule: "Only push soft objects after placing items in the bin."
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == goal_state[object0.name]
    assert object1.in_box == goal_state[object1.name]
    assert object2.in_box == goal_state[object2.name]
    assert object3.in_box == goal_state[object3.name]
    assert box.in_bin_objects == goal_state[object4.name]
    
    print("All task planning is done")
