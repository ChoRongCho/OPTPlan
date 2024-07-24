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
    in_box: bool
    out_box: bool
    
    # Object physical properties
    is_elastic: bool
    is_rigid: bool
    is_fragile: bool
    is_soft: bool


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
        if self.robot_handempty and obj.out_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.out_box:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
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
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that the robot can only pick objects that are not already in the bin and when its hand is empty. The 'place' action ensures that objects are placed in the bin only if they are being held by the robot and are not already in the bin. The 'push' and 'fold' actions require the robot's hand to be empty and the object to be in the bin, ensuring that the robot can only push or fold objects that are already in the bin. The 'out' action allows the robot to remove objects from the bin and place them on the platform, ensuring that the robot's hand is empty after the action. These actions ensure that the robot follows the rules for bin packing, such as not picking and placing boxes, pushing soft objects before packing them, and handling rigid objects appropriately.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, out_box=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object1 = Object(
    index=1, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, out_box=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=False
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, out_box=True,
    is_elastic=True, is_rigid=True, is_fragile=False, is_soft=False
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, out_box=False,
    is_elastic=True, is_rigid=False, is_fragile=True, is_soft=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, out_box=False,
    is_elastic=False, is_rigid=False, is_fragile=False, is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    objects = [object0, object1, object2, object3, object4]
    box = object4

    # Second, using given rules and object's states, make a task planning strategy
    # 1. You should never pick and place a box.
    # 2. When placing soft objects, the soft objects must be pushed before packed in the bin.
    # 3. When a rigid object is in the bin at the initial state, out the rigid object and replace it into the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    bin = box

    # c) Action sequence
    # 1. Out the rigid object (white_2D_circle) from the bin and replace it
    robot.out(object3, bin)
    robot.pick(object3, bin)
    robot.place(object3, bin)

    # 2. Pick and push the soft object (yellow_3D_cuboid) before placing it in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)
    robot.push(object0, bin)

    # 3. Pick and place the white_2D_ring in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The white_2D_circle was initially in the bin and is rigid, so it was taken out and replaced.
    # 2. The yellow_3D_cuboid is soft, so it was pushed before being placed in the bin.
    # 3. The white_2D_ring was simply picked and placed in the bin.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object4.in_box == False
    print("All task planning is done")
