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
        if obj.object_type != 'bin' and obj not in bin.in_bin and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            bin.in_bin.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj in bin.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
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
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=False, is_soft=True, is_fragile=False, is_heavy=False)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=[], is_rigid=True, is_elastic=False, is_soft=False, is_fragile=False, is_heavy=False)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', pushed=False, folded=False, in_bin=[2], is_rigid=False, is_elastic=True, is_soft=False, is_fragile=False, is_heavy=False)
object3 = Object(index=3, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=[3], is_rigid=True, is_elastic=False, is_soft=False, is_fragile=False, is_heavy=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='bin', pushed=False, folded=False, in_bin=[2, 3], is_rigid=False, is_elastic=False, is_soft=False, is_fragile=False, is_heavy=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (red_3D_polyhedron) -> in white_box
    # object1 (yellow_3D_cylinder) -> in white_box
    # object2 (white_1D_ring) -> out of white_box
    # object3 (black_3D_cylinder) -> in white_box
    # object4 (white_box) -> contains [red_3D_polyhedron, yellow_3D_cylinder, black_3D_cylinder]

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # c) Make the action sequence
    # 1. Pick out white_1D_ring from white_box
    robot.pick_out(object2, bin)

    # 2. Pick red_3D_polyhedron and place it in white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick yellow_3D_cylinder and place it in white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Don't pick and place a box called bin - Followed
    # Rule 2: When fold an object, the object must be foldable - No folding action needed
    # Rule 3: When place a rigid objects in the bin, the soft objects must be in the bin before - Followed

    # Fourth, check if the goal state is satisfying goal state table.
    assert object0 in bin.in_bin  # red_3D_polyhedron should be in white_box
    assert object1 in bin.in_bin  # yellow_3D_cylinder should be in white_box
    assert object2 not in bin.in_bin  # white_1D_ring should be out of white_box
    assert object3 in bin.in_bin  # black_3D_cylinder should be in white_box
    assert object4.in_bin == [object2, object3, object0, object1]  # white_box should contain [red_3D_polyhedron, yellow_3D_cylinder, black_3D_cylinder]

    print("All task planning is done")
