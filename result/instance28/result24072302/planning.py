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
    is_rigid: bool
    is_elastic: bool
    is_foldable: bool
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
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and not obj.is_rigid and not obj.is_foldable:
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
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing tasks. The 'pick' action ensures that only objects (not bins) that are not already in the bin can be picked up, and the robot's hand must be empty. The 'place' action ensures that only objects (not bins) can be placed in the bin, and the robot must be holding the object. The 'push' action ensures that only non-rigid and non-foldable objects can be pushed, and the robot's hand must be empty. The 'fold' action ensures that only foldable objects can be folded, and the robot's hand must be empty. The 'out' action ensures that objects can be removed from the bin and placed on the platform, and the robot's hand must be empty before and after the action. These actions and their preconditions and effects are designed to ensure that the robot follows the rules and constraints of the bin packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_foldable=False, in_box=False
)

object1 = Object(
    index=1, name='white_3D_cone', color='white', shape='3D_cone', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_foldable=True, in_box=False
)

object2 = Object(
    index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_foldable=False, in_box=False
)

object3 = Object(
    index=3, name='brown_2D_rectangle', color='brown', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_foldable=True, in_box=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3], is_rigid=False, is_elastic=False, is_foldable=False, in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: black_3D_cylinder, not in box
    # object1: white_3D_cone, not in box
    # object2: transparent_2D_circle, not in box
    # object3: brown_2D_rectangle, in box
    # object4: white_box, contains object3

    # Goal State
    # object0: black_3D_cylinder, in box
    # object1: white_3D_cone, in box
    # object2: transparent_2D_circle, in box
    # object3: brown_2D_rectangle, in box
    # object4: white_box, contains object0, object1, object2, object3

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place the elastic object (object2) in the box first.
    # 2. Fold the foldable object (object1) and place it in the box.
    # 3. Place the rigid object (object0) in the box.
    # 4. Ensure the fragile object (object3) remains in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Step 1: Place the elastic object (object2) in the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 2: Fold the foldable object (object1) and place it in the box
    robot.fold(object1, box)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 3: Place the rigid object (object0) in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The elastic object (object2) is placed first to satisfy rule 3.
    # 2. The foldable object (object1) is folded and placed next, ensuring the fragile object (object3) is already in the box as per rule 2.
    # 3. The rigid object (object0) is placed last, ensuring it does not interfere with the placement of other objects.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object3, object2, object1, object0]
    print("All task planning is done")
