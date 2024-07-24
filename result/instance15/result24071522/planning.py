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
    is_in_box: bool
    is_out_box: bool


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
        if self.robot_handempty and obj.is_out_box:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            bin.in_bin.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
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
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=False, is_fragile=False, is_soft=True, is_rigid=False,
    is_in_box=False, is_out_box=True
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=True, is_fragile=False, is_soft=True, is_rigid=False,
    is_in_box=False, is_out_box=True
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=True, is_fragile=False, is_soft=False, is_rigid=False,
    is_in_box=False, is_out_box=True
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=False, is_fragile=True, is_soft=False, is_rigid=False,
    is_in_box=True, is_out_box=False
)

object4 = Object(
    index=4, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=True, is_fragile=False, is_soft=False, is_rigid=False,
    is_in_box=True, is_out_box=False
)

object5 = Object(
    index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=False, is_fragile=True, is_soft=False, is_rigid=True,
    is_in_box=True, is_out_box=False
)

object6 = Object(
    index=6, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[], is_elastic=False, is_fragile=False, is_soft=False, is_rigid=False,
    is_in_box=False, is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: in_box
    # object1: in_box
    # object2: out_box
    # object3: in_box
    # object4: in_box
    # object5: in_box
    # object6: bin (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object6

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: it is prohibited to lift and relocate a container
    # Rule 2: do not place a fragile object if there is no soft object in the bin
    # Rule 3: when a fragile object in the bin at the initial state, out of the fragile object and replace it into the bin

    # Step-by-step action sequence
    # 1. Pick out fragile objects from the bin (object3, object5)
    robot.pick_out(object3, bin)
    robot.pick_out(object5, bin)

    # 2. Place a soft object in the bin first (object0, object1)
    robot.pick(object0, bin)
    robot.place(object0, bin)

    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 3. Place the fragile objects back into the bin (object3, object5)
    robot.pick(object3, bin)
    robot.place(object3, bin)

    robot.pick(object5, bin)
    robot.place(object5, bin)

    # 4. Ensure the elastic object (object4) is in the bin
    # Since object4 is already in the bin, no action is needed

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    assert object5.is_in_box == True
    print("All task planning is done")
