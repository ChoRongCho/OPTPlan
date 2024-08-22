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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.in_box == False and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            if obj.is_soft or all(o.is_soft for o in bin.in_bin_objects):
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
            else:
                print(f"Cannot Place {obj.name} in {bin.name} because soft objects are not in the box")
        else:
            print(f"Cannot Place {obj.name} because it is not being held")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
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
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. The 'pick' action allows the robot to pick up objects that are not already in the bin and when its hand is empty. The 'place' action ensures that soft objects are placed first if there are any, adhering to the rule that soft objects should be in the box before placing fragile or rigid objects. The 'push' action is restricted to soft objects that are already in the bin and requires the robot's hand to be empty, ensuring that the robot does not push non-soft objects. The 'fold' action is only applicable to foldable objects and requires the robot's hand to be empty, ensuring that only foldable objects are folded. The 'out' action allows the robot to remove objects from the bin and place them on a platform, ensuring that the robot's hand is empty after the action. These actions and their conditions ensure that the robot follows the rules and maintains a consistent state throughout the bin packing process.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    can_be_packed=True
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
    is_foldable=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
)

object2 = Object(
    index=2, 
    name='blue_1D_linear', 
    color='blue', 
    shape='1D_linear', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=True
)

object3 = Object(
    index=3, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=True, 
    in_box=True, 
    can_be_packed=True
)

bin = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object3], 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=True, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not pushed, not folded, not in bin
    # object1: out_box, not pushed, not folded, not in bin
    # object2: out_box, not pushed, not folded, not in bin
    # object3: in_box, not pushed, not folded, in bin
    # bin: contains object3

    # Goal state:
    # object0: in_box, not pushed, not folded, in bin
    # object1: in_box, not pushed, folded, in bin
    # object2: in_box, not pushed, not folded, in bin
    # object3: in_box, not pushed, not folded, in bin
    # bin: contains object0, object1, object2, object3

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place object0 (soft) in the bin
    # 2. Pick and fold object1 (foldable)
    # 3. Place object1 in the bin
    # 4. Pick and place object2 (rigid) in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = bin

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.fold(object1, box)
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Pick and place object0 first because it is soft and should be in the bin before placing rigid objects.
    # 2. Fold object1 because it is foldable.
    # 3. Place object1 in the bin after folding.
    # 4. Pick and place object2 last because it is rigid and all soft objects are already in the bin.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object1.folded == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3}

    print("All task planning is done")
