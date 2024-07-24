from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates
    is_rigid: bool = False
    is_soft: bool = False
    is_elastic: bool = False
    is_fragile: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_packable: bool = True


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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj.object_type != 'box':
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            # Effects
            obj.is_in_box = True
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
            # Effects
            obj.is_packable = True
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and not self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_packable=True)
object3 = Object(index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=True, is_packable=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_packable=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (red_3D_polyhedron) -> in_box
    # object1 (green_3D_cylinder) -> in_box
    # object2 (yellow_3D_cylinder) -> in_box
    # object3 (white_1D_ring) -> out_box
    # object4 (white_box) -> box (unchanged)

    # Initialize the robot
    robot = Robot()

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step 1: Pick out the white_1D_ring from the box
    robot.pick_out(object3, object4)

    # Step 2: Push the red_3D_polyhedron into the box (since it is soft)
    robot.push(object0, object4)

    # Step 3: Pick the yellow_3D_cylinder and place it in the box
    robot.pick(object2, object4)
    robot.place(object2, object4)

    # Step 4: Pick the green_3D_cylinder and place it in the box (after the soft object is in the box)
    robot.pick(object1, object4)
    robot.place(object1, object4)

    # after making all actions, fill your reasons according to the rules
    # Rule 1: Avoid handling and moving any box - The box was not moved or handled directly.
    # Rule 2: When fold a object, the object must be foldable - No folding action was required.
    # Rule 3: When place a fragile objects, the soft objects must be in the bin - The red_3D_polyhedron (soft) was pushed into the box before placing the green_3D_cylinder (fragile).
    # Rule 4: When push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted - Only the red_3D_polyhedron (soft) was pushed.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == False
    assert object4.is_in_box == False  # The box itself should not be in another box
    print("Goal state achieved successfully.")
