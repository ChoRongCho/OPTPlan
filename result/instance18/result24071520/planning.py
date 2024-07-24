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
    is_fragile: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_out_box: bool


class Robot:
    def __init__(self, name: str = "UR5", goal: str = None, actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False
    
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if self.robot_handempty and not obj.is_in_box:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_soft or obj.is_rigid:
                if obj.is_soft and all(o.is_soft for o in bin.in_bin):
                    bin.in_bin.append(obj)
                    obj.is_in_box = True
                    obj.is_out_box = False
                    self.state_handempty()
                    print(f"Place {obj.name} in {bin.name}")
                elif obj.is_rigid and all(o.is_soft for o in bin.in_bin):
                    bin.in_bin.append(obj)
                    obj.is_in_box = True
                    obj.is_out_box = False
                    self.state_handempty()
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} due to rule constraints")
            else:
                bin.in_bin.append(obj)
                obj.is_in_box = True
                obj.is_out_box = False
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin):
        if self.robot_handempty:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin:
            bin.in_bin.remove(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

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
    in_bin=[], 
    is_soft=True, 
    is_fragile=False, 
    is_rigid=False, 
    is_in_box=False, 
    is_out_box=True
)

object1 = Object(
    index=1, 
    name='black_2D_circle', 
    color='black', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_fragile=True, 
    is_rigid=True, 
    is_in_box=True, 
    is_out_box=False
)

bin2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='bin', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_in_box=False, 
    is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) should be in bin2 (white_box)
    # object1 (black_2D_circle) should be in bin2 (white_box)
    # bin2 (white_box) should contain object0 and object1

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = bin2

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: avoid handling and moving any box
    # Rule 2: when place a soft object, the elastic object must be in the bin
    # Rule 3: when place a rigid objects, the soft objects must be in the bin
    # Rule 4: when a rigid object in the bin at the initial state, out of the rigid object first

    # Step 1: Pick out the rigid object (black_2D_circle) from the bin
    robot.pick_out(object1, bin)

    # Step 2: Pick the soft object (brown_3D_cuboid)
    robot.pick(object0, bin)

    # Step 3: Place the soft object (brown_3D_cuboid) in the bin
    robot.place(object0, bin)

    # Step 4: Pick the rigid object (black_2D_circle)
    robot.pick(object1, bin)

    # Step 5: Place the rigid object (black_2D_circle) in the bin
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert bin2.in_bin == [object0, object1]
    print("All task planning is done")
