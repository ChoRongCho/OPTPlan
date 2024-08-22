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
    is_fragile: bool
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
        if obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_elastic:
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
        if obj.in_box and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for a bin_packing task. The 'pick' and 'out' actions have minimal preconditions, allowing the robot to handle objects freely. The 'place' action ensures that soft objects are placed first if any are present, adhering to the rule for fragile or rigid objects. The 'push' action is restricted to soft objects, ensuring they are only pushed after being placed in the bin. The 'fold' action is limited to foldable objects, ensuring the robot only attempts to fold objects that can be folded. These conditions and effects ensure the robot's actions are safe and efficient for the bin_packing task

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
    is_rigid=True, 
    is_fragile=False, 
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
    is_rigid=False, 
    is_fragile=False, 
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
    is_rigid=False, 
    is_fragile=True, 
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
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: in_box
    # object3: box (empty)

    # Final State:
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: box (contains object0, object1, object2)

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the soft object (object1) first.
    # 2. Pick and place the rigid object (object0).
    # 3. Ensure the fragile object (object2) is already in the box.
    # 4. Push the soft object (object1) to ensure it is properly placed.
    # 5. Fold the foldable object (object2) if necessary.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object1, box)  # Pick white_2D_ring (soft object)
    robot.place(object1, box)  # Place white_2D_ring in the box
    robot.push(object1, box)  # Push white_2D_ring to ensure it is properly placed

    robot.pick(object0, box)  # Pick black_3D_cylinder (rigid object)
    robot.place(object0, box)  # Place black_3D_cylinder in the box

    # No need to pick object2 as it is already in the box
    # Fold object2 if necessary
    robot.fold(object2, box)  # Fold black_2D_ring (foldable object)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Picked and placed the soft object (object1) first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # 2. Pushed the soft object (object1) to ensure it is properly placed.
    # 3. Picked and placed the rigid object (object0) after the soft object.
    # 4. Folded the foldable object (object2) as it is foldable.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object1, object0, object2]
    print("All task planning is done")
