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
    is_soft: bool
    is_elastic: bool
    
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
        if obj.object_type != 'box' and obj not in bin.in_bin and self.robot_handempty:
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
        if self.robot_handempty and obj.object_type != 'box' and obj not in bin.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.object_type != 'box':
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
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=[], is_soft=True, is_elastic=False, is_fragile=False, is_heavy=False)
object1 = Object(index=1, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=True, is_fragile=False, is_heavy=False)
object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=True, is_fragile=False, is_heavy=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=[], is_soft=True, is_elastic=False, is_fragile=False, is_heavy=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=False, is_fragile=False, is_heavy=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) -> in white_box
    # object1 (blue_1D_ring) -> in white_box
    # object2 (transparent_3D_cylinder) -> in white_box
    # object3 (white_2D_circle) -> in white_box
    # object4 (white_box) -> remains as is

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: When placing a 1D object in the bin, the soft object must be in the bin before
    # Rule 3: If there is an elastic object, push the object not in the bin, but on the platform

    # Step-by-step action sequence
    # 1. Pick and place the soft object (brown_3D_cuboid) in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Push the elastic object (blue_1D_ring) on the platform
    robot.push(object1, bin)

    # 3. Pick and place the transparent_3D_cylinder in the bin
    robot.pick_out(object2, bin)
    robot.place(object2, bin)

    # 4. Pick and place the white_2D_circle in the bin
    robot.pick_out(object3, bin)
    robot.place(object3, bin)

    # 5. Now place the blue_1D_ring in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 in bin.in_bin
    assert object4.in_bin == []
    print("All task planning is done")
