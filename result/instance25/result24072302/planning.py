from dataclasses import dataclass, field
from typing import List

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: List[int] = field(default_factory=list)
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_elastic: bool = False
    is_soft: bool = False
    
    # Object physical properties
    init_pose: str = 'out_box'
    in_bin: bool = False


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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # pick an {object} not in the {bin}, it does not include 'place' action
        if self.robot_handempty and not obj.in_bin and obj.object_type != 'box':
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            obj.in_bin = True
            bin.in_bin_objects.append(obj.index)
            self.state_handempty()
            print(f"Place {obj.name} in bin")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_bin:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_soft:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_bin and obj.object_type != 'box':
            bin.in_bin_objects.remove(obj.index)
            obj.in_bin = False
            self.state_holding(obj)
            print(f"Out {obj.name} from bin")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that the robot only picks objects that are not in the bin and are not boxes, adhering to rule 1. The 'place' action places the object in the bin and updates the object's state. The 'push' action requires the robot's hand to be empty and the object to be in the bin, ensuring proper state management. The 'fold' action checks if the object is foldable (is_soft) before folding, following rule 2. The 'out' action allows the robot to remove objects from the bin, ensuring they are not boxes and updating their state accordingly. These actions ensure the robot operates within the constraints and rules provided for the bin_packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', init_pose='out_box', is_elastic=True, is_soft=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', init_pose='out_box', is_elastic=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', init_pose='box', in_bin=True)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box, not in bin
    # object1: out_box, not in bin
    # object2: in bin, box

    # Goal State
    # object0: out_box, not in bin
    # object1: in bin
    # object2: in bin, box, containing object0 and object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick object1 (transparent_3D_cylinder) and place it in the bin.
    # 2. Pick object0 (yellow_3D_cuboid) and place it in the bin.
    # 3. Push object0 (yellow_3D_cuboid) to ensure it is properly placed in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Step 1: Pick object1 and place it in the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 2: Pick object0 and place it in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Push object0 to ensure it is properly placed in the bin
    robot.push(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Avoid handling and moving any box - The box (object2) is not moved or handled directly.
    # Rule 2: When folding an object, the object must be foldable - No folding action is required.
    # Rule 3: When folding a foldable object, the fragile object must be in the bin - No folding action is required.
    # Rule 4: When a rigid object is in the bin at the initial state, out of the rigid object and replace it into the bin - No rigid object is initially in the bin.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_bin == True
    assert object1.in_bin == True
    assert object2.in_bin == True
    assert object0.index in object2.in_bin_objects
    assert object1.index in object2.in_bin_objects
    print("All task planning is done")
