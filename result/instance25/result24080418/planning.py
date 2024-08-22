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
    is_soft: bool
    
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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.in_box == False and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.is_packable:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
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
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. The 'pick' action allows the robot to pick objects that are not already in the bin and when its hand is empty. The 'place' action ensures that only packable objects are placed in the bin, and the robot's hand must be holding the object. The 'push' action is restricted to soft objects that are already in the bin and requires the robot's hand to be empty. The 'fold' action is limited to elastic objects and also requires the robot's hand to be empty. The 'out' action allows the robot to remove objects from the bin, ensuring they are no longer marked as in the bin. These conditions ensure that the robot's actions are logical and follow the rules provided for the bin packing task

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
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    is_packable=True
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
    is_elastic=False, 
    is_soft=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in any bin, is elastic, is soft, not in box, is packable
    # object1: out_box, not pushed, not folded, not in any bin, is elastic, not soft, not in box, is packable
    # object2: in_box, not pushed, not folded, in bin, not elastic, not soft, in box, not packable

    # Final State:
    # object0: in_box, not pushed, not folded, in bin, is elastic, is soft, in box, is packable
    # object1: in_box, not pushed, not folded, in bin, is elastic, not soft, in box, is packable
    # object2: in_box, not pushed, not folded, in bin, not elastic, not soft, in box, not packable

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick object0 (soft object) and place it in the box.
    # 2. Push object0 (soft object) to ensure it is properly placed.
    # 3. Pick object1 (rigid object) and place it in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object2

    # Action sequence
    robot.pick(object0, box)  # Pick yellow_3D_cuboid
    robot.place(object0, box)  # Place yellow_3D_cuboid in white_box
    robot.push(object0, box)  # Push yellow_3D_cuboid

    robot.pick(object1, box)  # Pick transparent_3D_cylinder
    robot.place(object1, box)  # Place transparent_3D_cylinder in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Pick object0 (yellow_3D_cuboid) because it is not in the box and the robot's hand is empty.
    # 2. Place object0 in the box because it is packable.
    # 3. Push object0 because it is soft and already in the box.
    # 4. Pick object1 (transparent_3D_cylinder) because it is not in the box and the robot's hand is empty.
    # 5. Place object1 in the box because it is packable.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    print("All task planning is done")
