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
        if self.robot_handempty and obj.is_out_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_out_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            obj.is_in_box = True
            obj.is_out_box = False
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_in_box:
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
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

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
    index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=False, is_fragile=True, is_soft=False, is_rigid=True,
    is_in_box=True, is_out_box=False
)

object4 = Object(
    index=4, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_elastic=True, is_fragile=False, is_soft=False, is_rigid=False,
    is_in_box=True, is_out_box=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
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
    # object5: contains [object0, object1, object3, object4]

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object5

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: it is prohibited to lift and relocate a container
    # Rule 2: do not place a fragile object if there is no soft object in the bin
    # Rule 3: when a fragile object in the bin at the initial state, out of the fragile object and replace it into the bin

    # Step 1: Pick out the fragile object (object3) from the bin
    robot.pick_out(object3, bin)

    # Step 2: Pick and place a soft object (object0) into the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 3: Pick and place another soft object (object1) into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 4: Place the fragile object (object3) back into the bin
    robot.place(object3, bin)

    # Step 5: Pick and place the last object (object4) into the bin
    robot.pick(object4, bin)
    robot.place(object4, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    assert object5.in_bin == [object0, object1, object3, object4]
    print("All task planning is done")
