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
    is_soft: bool
    is_elastic: bool
    
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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, soft objects should be in the box if there are any
        if self.robot_now_holding == obj and all(o.in_box for o in bin.in_bin_objects if o.is_soft):
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft, object must be in the bin
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_elastic:
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
            self.state_holding(obj)
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=False, 
    in_box=False, 
    is_packable=True
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
    is_soft=False, 
    is_elastic=True, 
    in_box=False, 
    is_packable=True
)

object2 = Object(
    index=2, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_elastic=True, 
    in_box=True, 
    is_packable=True
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
    is_soft=False, 
    is_elastic=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in box
    # object1: out_box, not pushed, not folded, not in box
    # object2: in_box, not pushed, not folded, in box
    # object3: box, not pushed, not folded, in box, contains object2

    # Final State:
    # object0: in_box, not pushed, not folded, in box
    # object1: in_box, not pushed, not folded, in box
    # object2: in_box, not pushed, not folded, in box
    # object3: box, not pushed, not folded, in box, contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick object0 and place it in the box.
    # 2. Fold object1 (since it is elastic) and then place it in the box.
    # 3. Ensure object2 (soft) is already in the box.
    # 4. Push object2 (soft) to make space if needed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.fold(object1, box)
    robot.place(object1, box)
    robot.push(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Pick object0: No preconditions violated.
    # - Place object0: object2 (soft) is already in the box.
    # - Fold object1: object1 is elastic.
    # - Place object1: object2 (soft) is already in the box.
    # - Push object2: object2 is soft and already in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
