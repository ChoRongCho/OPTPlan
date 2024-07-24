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
    is_fragile: bool
    
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
            print(f"Pick {obj.name}")
            self.state_holding(obj)
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
        if self.robot_handempty and obj.is_soft:
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

# Reason:
# The robot actions are designed to follow the given rules strictly. The preconditions ensure that actions are only performed when the robot is in the correct state and the objects meet the necessary criteria. For example, the robot can only pick an object if it is not already in the bin and the robot's hand is empty. Similarly, the robot can only place an object if it is currently holding it. The push and fold actions require the robot's hand to be empty, and the pick_out action ensures the object is in the bin and the robot's hand is empty before picking it out. These conditions and effects ensure the robot's actions are consistent with the rules and maintain the correct state of the objects and the robot.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=True, is_elastic=False, is_fragile=False,
    is_in_box=False, is_out_box=True
)

object1 = Object(
    index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=True, is_fragile=False,
    is_in_box=False, is_out_box=True
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=True, is_fragile=False,
    is_in_box=False, is_out_box=True
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=False, is_fragile=True,
    is_in_box=True, is_out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_elastic=False, is_fragile=False,
    is_in_box=True, is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) should be in white_box
    # object1 (white_1D_ring) should be in white_box
    # object2 (blue_1D_ring) should be out of the box
    # object3 (white_2D_circle) should be in white_box
    # object4 (white_box) should contain yellow_3D_cuboid, white_1D_ring, and white_2D_circle

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: You should never pick and place a box
    # Rule 3: When placing a soft object, the soft object must be pushed before packed in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, take it out and replace it into the bin

    # Step-by-step action sequence:
    # 1. Pick out the rigid object (white_2D_circle) from the bin
    robot.pick_out(object3, bin)

    # 2. Pick the yellow_3D_cuboid (soft object)
    robot.pick(object0, bin)

    # 3. Push the yellow_3D_cuboid (soft object)
    robot.push(object0, bin)

    # 4. Place the yellow_3D_cuboid into the bin
    robot.place(object0, bin)

    # 5. Pick the white_1D_ring (rigid object)
    robot.pick(object1, bin)

    # 6. Place the white_1D_ring into the bin
    robot.place(object1, bin)

    # 7. Pick the white_2D_circle (rigid object)
    robot.pick(object3, bin)

    # 8. Place the white_2D_circle into the bin
    robot.place(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object3 in bin.in_bin
    print("All task planning is done")
