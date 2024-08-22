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
    is_elastic: bool
    is_foldable: bool
    
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
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box and obj.is_elastic:
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
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for a bin_packing task. The preconditions ensure that actions are only performed when the robot is in the correct state and the objects meet the necessary criteria. For example, the robot can only fold objects that are foldable and can only push objects that are elastic and already in the bin. These conditions help to maintain the integrity of the task and ensure that the robot performs actions in a logical and efficient manner. The effects update the state of the robot and objects to reflect the changes made by the actions, ensuring that the system remains consistent and accurate.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=True, 
    in_box=False, 
    is_packed=False
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
    is_elastic=True, 
    is_foldable=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_foldable=False, 
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
    is_elastic=False, 
    is_foldable=False, 
    in_box=False, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: yellow_2D_rectangle, out_box, not pushed, not folded, not in box, not packed
    # object1: white_2D_ring, out_box, not pushed, not folded, not in box, not packed
    # object2: transparent_2D_circle, out_box, not pushed, not folded, not in box, not packed
    # object3: white_box, box, not pushed, not folded, not in box, not packed

    # Goal State
    # object0: yellow_2D_rectangle, in_box, not pushed, folded, in box, packed
    # object1: white_2D_ring, in_box, pushed, not folded, in box, packed
    # object2: transparent_2D_circle, in_box, pushed, not folded, in box, packed
    # object3: white_box, box, not pushed, not folded, in box, packed

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the yellow_2D_rectangle (foldable) into the box
    # 2. Fold the yellow_2D_rectangle
    # 3. Pick and place the white_2D_ring (elastic) into the box
    # 4. Pick and place the transparent_2D_circle (elastic) into the box
    # 5. Push the white_2D_ring
    # 6. Push the transparent_2D_circle

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.fold(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.push(object1, box)
    robot.push(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The yellow_2D_rectangle is foldable, so it should be folded after placing it in the box.
    # 2. The white_2D_ring and transparent_2D_circle are elastic, so they should be pushed after placing them in the box.
    # 3. The soft object (yellow_2D_rectangle) is placed first before placing the rigid objects (white_2D_ring and transparent_2D_circle).

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object2.pushed == True
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
