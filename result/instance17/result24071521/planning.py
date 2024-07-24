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
    is_foldable: bool
    is_elastic: bool
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
        if self.robot_handempty and not obj.is_in_box and obj.object_type == 'obj':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj and obj.object_type == 'obj':
            if obj.is_soft and not obj.pushed:
                print(f"Cannot Place {obj.name} because it is soft and not pushed")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                obj.is_in_box = True
                obj.is_out_box = False
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.object_type == 'obj':
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable and obj.object_type == 'obj':
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin and obj.object_type == 'obj':
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
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_soft=True, is_rigid=False,
    is_in_box=False, is_out_box=True
)

object1 = Object(
    index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=True, is_soft=False, is_rigid=False,
    is_in_box=False, is_out_box=True
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=True, is_soft=False, is_rigid=False,
    is_in_box=False, is_out_box=True
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=True, is_elastic=False, is_soft=False, is_rigid=True,
    is_in_box=True, is_out_box=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_soft=False, is_rigid=False,
    is_in_box=False, is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) should be pushed and in the white_box
    # object1 (white_1D_ring) should be in the white_box
    # object2 (blue_1D_ring) should be out of the box
    # object3 (white_2D_circle) should be in the white_box
    # white_box should contain object0, object1, and object3

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: You should never pick and place a box
    # Rule 3: When placing a soft object, the soft object must be pushed before packed in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, take it out and replace it into the bin

    # Step-by-step action sequence:
    # 1. Pick out the rigid object (white_2D_circle) from the bin and place it back
    robot.pick_out(object3, bin)
    robot.place(object3, bin)

    # 2. Push the soft object (yellow_3D_cuboid) before placing it in the bin
    robot.push(object0, bin)
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick and place the white_1D_ring into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    assert object4.is_in_box == False
    print("All task planning is done")
