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
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot can only pick objects not in the bin and not boxes. The 'place' action allows placing objects in the bin. The 'push' action is restricted to soft objects in the bin, ensuring the robot's hand is empty. The 'fold' action is for foldable objects, also requiring an empty hand. The 'pick_out' action allows removing objects from the bin, ensuring the robot's hand is empty afterward. These conditions ensure the robot's actions are consistent with the rules and constraints provided.

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
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_soft=True,
    is_fragile=False, is_heavy=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_soft=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # object0: in_box
    # object1: in_box, folded
    # object2: in_box
    # object3: out_box
    # object4: box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: You should never pick and place a box
    # Rule 2: If there is a foldable object, you must fold the object neither it is packed or not
    # Rule 3: When a rigid object in the bin at the initial state, out of the rigid object and replace it into the bin
    # Rule 4: You must push a soft object in the bin

    # Action sequence to achieve the goal state
    # Step 1: Pick out the rigid object (red_3D_polyhedron) from the bin
    robot.pick_out(object3, bin)

    # Step 2: Fold the foldable object (yellow_2D_rectangle)
    robot.fold(object1, bin)

    # Step 3: Pick and place the yellow_2D_rectangle into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 4: Pick and place the blue_1D_ring into the bin
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Step 5: Pick and place the brown_3D_cuboid into the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 6: Push the soft object (brown_3D_cuboid) in the bin
    robot.push(object0, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin and object1.folded
    assert object2 in bin.in_bin
    assert object3 not in bin.in_bin
    assert object4.object_type == 'box'
    print("All task planning is done")
