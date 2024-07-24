from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic Effect Robot Action Predicates for object_type = obj
    pushed: bool
    folded: bool
    
    # Bin Predicates for object_type = bin
    in_bin: list
    
    # Object physical properties predicates
    is_elastic: bool
    is_fragile: bool
    is_soft: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_packable: bool
    is_stable: bool


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
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.object_type == 'obj' and obj in bin.in_bin:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.object_type == 'obj' and obj.is_elastic:
            if all(o.is_fragile for o in bin.in_bin):
                print(f"Fold {obj.name}")
                obj.folded = True
            else:
                print(f"Cannot Fold {obj.name} because not all objects in bin are fragile")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_elastic=True, 
    is_fragile=False, 
    is_soft=True, 
    is_rigid=False, 
    is_packable=False, 
    is_stable=False
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_elastic=False, 
    is_fragile=True, 
    is_soft=False, 
    is_rigid=True, 
    is_packable=False, 
    is_stable=False
)

object2 = Object(
    index=2, 
    name='transparent_3D_cone', 
    color='transparent', 
    shape='3D_cone', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_elastic=False, 
    is_fragile=False, 
    is_soft=True, 
    is_rigid=False, 
    is_packable=False, 
    is_stable=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='bin', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_elastic=False, 
    is_fragile=False, 
    is_soft=False, 
    is_rigid=False, 
    is_packable=False, 
    is_stable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # object0: white_3D_cylinder - out of the box
    # object1: green_3D_cylinder - in the box
    # object2: transparent_3D_cone - in the box
    # object3: white_box - contains object1 and object2

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # c) Make the action sequence
    # Pick green_3D_cylinder and place it in the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Pick transparent_3D_cone and place it in the box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: You should never pick and place a box - This rule is followed as we never pick or place the box (object3).
    # Rule 2: When fold a foldable object, the fragile object must be in the bin - This rule is not applicable as we are not folding any object.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin == False
    assert object1 in bin.in_bin == True
    assert object2 in bin.in_bin == True
    assert object3.in_bin == [object1, object2]
    print("All task planning is done")
