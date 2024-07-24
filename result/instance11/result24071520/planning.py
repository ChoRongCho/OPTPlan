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
    is_rigid: bool
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
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            bin.in_bin.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj in bin.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.object_type == 'obj' and obj.is_soft:
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
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=False, is_rigid=True, is_elastic=False,
    is_fragile=False, is_heavy=False
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_soft=True, is_rigid=False, is_elastic=True,
    is_fragile=False, is_heavy=False
)

object2 = Object(
    index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin=[2], is_soft=True, is_rigid=False, is_elastic=False,
    is_fragile=False, is_heavy=False
)

white_box = Object(
    index=3, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[object2], is_soft=False, is_rigid=False, is_elastic=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (black_3D_cylinder) -> in white_box, pushed
    # object1 (white_3D_cylinder) -> in white_box, pushed
    # object2 (red_3D_polyhedron) -> out of white_box
    # white_box -> contains object0 and object1

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: It is prohibited to lift and relocate a container
    # Rule 2: When placing rigid objects in the bin, the soft objects must be in the bin before
    # Rule 3: If there is a soft object, push the object first

    # Step 1: Push the red_3D_polyhedron (already in the bin)
    robot.push(object2, bin)

    # Step 2: Pick the white_3D_cylinder (soft object)
    robot.pick(object1, bin)

    # Step 3: Place the white_3D_cylinder in the bin
    robot.place(object1, bin)

    # Step 4: Push the white_3D_cylinder
    robot.push(object1, bin)

    # Step 5: Pick the black_3D_cylinder (rigid object)
    robot.pick(object0, bin)

    # Step 6: Place the black_3D_cylinder in the bin
    robot.place(object0, bin)

    # Step 7: Push the black_3D_cylinder
    robot.push(object0, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin and object0.pushed == True
    assert object1 in bin.in_bin and object1.pushed == True
    assert object2 not in bin.in_bin
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    assert object3.in_bin == [object0, object1]
    print("All task planning is done")
