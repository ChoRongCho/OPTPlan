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
    is_rigid: bool
    
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
        if self.robot_handempty and obj.object_type != 'box' and obj not in bin.in_bin:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_rigid:
                if any(o.is_elastic for o in bin.in_bin):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} - No elastic object in bin")
            elif obj.is_elastic:
                if any(o.color == 'blue' for o in bin.in_bin):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} - No blue object in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj in bin.in_bin:
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
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=True, is_rigid=False,
    is_fragile=False, is_heavy=False
)

object1 = Object(
    index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_rigid=True,
    is_fragile=False, is_heavy=False
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=True, is_rigid=False,
    is_fragile=False, is_heavy=False
)

object3 = Object(
    index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_foldable=True, is_elastic=False, is_rigid=False,
    is_fragile=False, is_heavy=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin=[], is_foldable=False, is_elastic=False, is_rigid=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: out_box
    # object1: in_box
    # object2: in_box
    # object3: in_box
    # object4: box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Step 1: Pick blue_1D_ring (object2) and place it in the bin
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Step 2: Pick black_3D_cylinder (object1) and place it in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 3: Pick yellow_2D_rectangle (object3) and place it in the bin
    robot.pick(object3, bin)
    robot.place(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin == False
    assert object1 in bin.in_bin == True
    assert object2 in bin.in_bin == True
    assert object3 in bin.in_bin == True
    assert object4 in bin.in_bin == False
    print("All task planning is done")
