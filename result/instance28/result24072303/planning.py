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
    is_fragile: bool
    is_soft: bool
    is_elastic: bool
    
    # Additional predicates for bin_packing
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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if not obj.is_fragile or (obj.is_fragile and any(o.is_elastic for o in bin.in_bin_objects)):
                print(f"Place {obj.name in bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
            else:
                print(f"Cannot Place {obj.name} due to rule 3")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name} due to rule 4")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_soft and any(o.is_fragile for o in bin.in_bin_objects):
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name} due to rule 2")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to adhere strictly to the given rules for the bin_packing task. The preconditions ensure that actions are only performed when the rules are satisfied, such as not picking or placing a box, ensuring fragile objects are only placed if an elastic object is present, and only allowing soft objects to be pushed. The effects update the state of the robot and objects to reflect the changes brought about by the actions, ensuring consistency and adherence to the task requirements.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, is_soft=False, is_elastic=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_3D_cone', color='white', shape='3D_cone', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, is_soft=False, is_elastic=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_soft=True, is_elastic=True,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2], is_rigid=False, is_fragile=False, is_soft=False, is_elastic=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[object2]

    # Goal State
    # object0: out_box=False, in_box=True
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[object0, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # We need to pick object0 and place it in object3 (the box)
    # object1 remains out of the box
    # object2 is already in the box, no action needed for it

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Make the action sequence
    # Pick object0 and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. We do not pick and place the box itself.
    # 2. We do not need to fold any object as there is no foldable object in the initial state.
    # 3. We do not place the fragile object (object1) in the box as there is no elastic object in the box initially.
    # 4. We do not need to push any object as there is no soft object that needs pushing.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == True
    assert object0 in object3.in_bin_objects
    assert object2 in object3.in_bin_objects
    print("All task planning is done")