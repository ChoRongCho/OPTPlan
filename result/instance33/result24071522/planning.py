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
    is_fragile: bool
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_heavy: bool
    is_large: bool


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
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_fragile=False, is_rigid=False, is_elastic=False, is_soft=True,
    is_heavy=False, is_large=False
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_fragile=True, is_rigid=True, is_elastic=False, is_soft=False,
    is_heavy=False, is_large=False
)

object2 = Object(
    index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_fragile=False, is_rigid=True, is_elastic=False, is_soft=False,
    is_heavy=False, is_large=False
)

object3 = Object(
    index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_fragile=False, is_rigid=False, is_elastic=True, is_soft=False,
    is_heavy=False, is_large=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[object3], is_fragile=False, is_rigid=False, is_elastic=False, is_soft=False,
    is_heavy=False, is_large=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (red_3D_polyhedron) -> in_box
    # object1 (green_3D_cylinder) -> in_box
    # object2 (yellow_3D_cylinder) -> in_box
    # object3 (white_1D_ring) -> out_box
    # white_box -> box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Avoid handling and moving any box
    # 2. When fold a object, the object must be foldable
    # 3. When place a fragile objects, the soft objects must be in the bin
    # 4. When push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted

    # Step-by-step action sequence
    # 1. Pick and place the red_3D_polyhedron (soft object) into the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick and place the green_3D_cylinder (fragile object) into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 3. Pick and place the yellow_3D_cylinder (rigid object) into the bin
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # 4. Pick out the white_1D_ring (elastic object) from the bin
    robot.pick_out(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 not in bin.in_bin
    assert bin.object_type == 'bin'
    print("All task planning is done")
