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
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_fragile: bool
    is_soft: bool
    is_foldable: bool
    
    # Object physical properties
    init_pose: str
    in_box: bool


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and not obj.is_fragile:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj.object_type != 'box':
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that only objects (not boxes) that are not already in the bin can be picked up, and the robot's hand must be empty. The 'place' action ensures that only objects currently held by the robot can be placed in the bin. The 'push' action is restricted to soft objects that are not fragile, ensuring safety and space optimization in the bin. The 'fold' action is only applicable to foldable objects, adhering to the rule that foldable objects must be folded. The 'out' action allows the robot to remove objects from the bin, ensuring that the robot's hand is empty after the action. These actions ensure that the robot operates within the constraints of the bin_packing task, maintaining safety and efficiency.

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
    in_bin_objects=[], 
    is_fragile=False, 
    is_soft=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_soft=False, 
    is_foldable=True, 
    init_pose='out_box', 
    in_box=False
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
    is_fragile=True, 
    is_soft=False, 
    is_foldable=False, 
    init_pose='in_box', 
    in_box=True
)

white_box = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object2], 
    is_fragile=False, 
    is_soft=False, 
    is_foldable=False, 
    init_pose='box', 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded
    # object1: out_box, not pushed, not folded
    # object2: in_box, not pushed, not folded
    # white_box: contains object2

    # Goal State:
    # object0: out_box, pushed
    # object1: in_box, folded
    # object2: in_box, not pushed, not folded
    # white_box: contains object2 and object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Out the rigid object (object2) from the box and place it back in the box.
    # 2. Fold the foldable object (object1).
    # 3. Place the folded object (object1) in the box.
    # 4. Push the soft object (object0).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # Action sequence
    # Step 1: Out the rigid object (object2) from the box
    robot.out(object2, box)

    # Step 2: Place the rigid object (object2) back in the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 3: Fold the foldable object (object1)
    robot.fold(object1, box)

    # Step 4: Place the folded object (object1) in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 5: Push the soft object (object0)
    robot.push(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The rigid object (object2) was initially in the box, so it was taken out and placed back in the box to satisfy the rule.
    # 2. The foldable object (object1) was folded before placing it in the box.
    # 3. The soft object (object0) was pushed to make more space in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == False
    assert object0.pushed == True
    assert object1.in_box == True
    assert object1.folded == True
    assert object2.in_box == True
    assert object2.pushed == False
    assert object2.folded == False
    assert white_box.in_bin_objects == [object2, object1]
    print("All task planning is done")
