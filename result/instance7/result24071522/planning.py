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
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


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
        if self.robot_handempty and obj.is_soft and obj in bin.in_bin:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
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
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_soft=True,
    is_fragile=False, is_heavy=False
)

object1 = Object(
    index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=True, is_elastic=False, is_soft=False,
    is_fragile=False, is_heavy=False
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=True, is_soft=False,
    is_fragile=False, is_heavy=False
)

object3 = Object(
    index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin=[3], is_foldable=False, is_elastic=False, is_soft=True,
    is_fragile=False, is_heavy=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin=[object3], is_foldable=False, is_elastic=False, is_soft=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: in_box
    # object1: in_box, folded
    # object2: in_box
    # object3: out_box, pushed
    # white_box: contains object0, object1, object2

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # Third, after making all actions, fill your reasons according to the rules

    # Rule 3: When a rigid object in the bin at the initial state, out of the rigid object and replace it into the bin
    robot.pick_out(object3, bin)  # Pick out red_3D_polyhedron from white_box
    robot.place(object3, bin)     # Place red_3D_polyhedron out of the box

    # Rule 2: If there is a foldable object, you must fold the object neither it is packed or not
    robot.fold(object1, bin)      # Fold yellow_2D_rectangle

    # Rule 1: You should never pick and place a box
    # Rule 4: You must push a soft object in the bin
    robot.pick(object0, bin)      # Pick brown_3D_cuboid
    robot.place(object0, bin)     # Place brown_3D_cuboid in white_box
    robot.push(object0, bin)      # Push brown_3D_cuboid

    robot.pick(object1, bin)      # Pick yellow_2D_rectangle
    robot.place(object1, bin)     # Place yellow_2D_rectangle in white_box

    robot.pick(object2, bin)      # Pick blue_1D_ring
    robot.place(object2, bin)     # Place blue_1D_ring in white_box

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin and object1.folded
    assert object2 in bin.in_bin
    assert object3 not in bin.in_bin and object3.pushed
    assert set(bin.in_bin) == {object0, object1, object2}
    print("All task planning is done")
