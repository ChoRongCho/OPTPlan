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
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


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
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            bin.in_bin.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            bin.in_bin.remove(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=False, is_soft=True,
    is_fragile=False, is_heavy=False
)

object1 = Object(
    index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=False, is_soft=True,
    is_fragile=False, is_heavy=False
)

object2 = Object(
    index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=True, is_soft=False,
    is_fragile=False, is_heavy=False
)

object3 = Object(
    index=3, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=True, is_elastic=False, is_soft=False,
    is_fragile=False, is_heavy=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin=[object2, object3], is_rigid=False, is_elastic=False, is_soft=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> in_box
    # object1 (red_3D_polyhedron) -> in_box
    # object2 (white_1D_ring) -> out_box
    # object3 (black_3D_cylinder) -> in_box
    # white_box -> contains [object0, object1, object3]

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # c) Make the action sequence
    # 1. Pick out white_1D_ring from the box
    robot.pick_out(object2, bin)

    # 2. Pick yellow_3D_cuboid and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick red_3D_polyhedron and place it in the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: You should never pick and place a box
    # - We only pick and place objects, not the box itself.
    # Rule 2: When fold an object, the object must be foldable
    # - We did not fold any objects.
    # Rule 3: When fold a foldable object, the fragile object must be in the bin
    # - We did not fold any objects.
    # Rule 4: When push an object, neither fragile and rigid objects are permitted, but only soft objects are permitted
    # - We did not push any objects.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    assert object3 in bin.in_bin
    assert object4 == bin  # white_box should be the bin

    print("All task planning is done")
