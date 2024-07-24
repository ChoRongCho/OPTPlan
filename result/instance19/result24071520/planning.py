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
    is_foldable: bool
    is_fragile: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_heavy: bool
    is_large: bool


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
            if obj.is_rigid and any(o.is_soft for o in bin.in_bin):
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
            elif not obj.is_rigid:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
            else:
                print(f"Cannot Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj in bin.in_bin:
            if not any(o.is_rigid for o in bin.in_bin):
                print(f"Push {obj.name}")
                obj.pushed = True
            else:
                print(f"Cannot Push {obj.name} due to rigid object in bin")
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
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=True, is_foldable=False, is_fragile=False, is_rigid=False,
    is_heavy=False, is_large=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_foldable=False, is_fragile=False, is_rigid=True,
    is_heavy=False, is_large=False
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_foldable=False, is_fragile=True, is_rigid=True,
    is_heavy=False, is_large=False
)

object3 = Object(
    index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_foldable=True, is_fragile=False, is_rigid=True,
    is_heavy=False, is_large=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[object3], is_soft=False, is_foldable=False, is_fragile=False, is_rigid=False,
    is_heavy=False, is_large=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) -> in_box, pushed=True
    # object1 (yellow_3D_cylinder) -> in_box
    # object2 (green_3D_cylinder) -> in_box
    # object3 (black_2D_circle) -> out_box
    # white_box -> contains [brown_3D_cuboid, yellow_3D_cylinder, green_3D_cylinder]

    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # c) Make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step 1: Pick and place the soft object (brown_3D_cuboid) first
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 2: Push the soft object to make more space
    robot.push(object0, bin)

    # Step 3: Pick and place the rigid object (yellow_3D_cylinder)
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 4: Pick and place the fragile and rigid object (green_3D_cylinder)
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Step 5: Pick out the black_2D_circle from the bin
    robot.pick_out(object3, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (brown_3D_cuboid) is placed first and pushed to make space.
    # 2. The rigid object (yellow_3D_cylinder) is placed after the soft object.
    # 3. The fragile and rigid object (green_3D_cylinder) is placed last.
    # 4. The black_2D_circle is removed from the bin to match the goal state.

    # Fourth, check if the goal state is satisfying goal state table.
    assert object0 in bin.in_bin and object0.pushed == True
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 not in bin.in_bin
    assert bin.in_bin == [object0, object1, object2]
    print("All task planning is done")
