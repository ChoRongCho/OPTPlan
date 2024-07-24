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
    is_soft: bool
    is_elastic: bool

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_fragile: bool


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
        if self.robot_handempty and not obj.is_in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_soft=False, is_elastic=True, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_elastic=False, is_in_box=True, is_fragile=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_soft=False, is_elastic=False, is_in_box=False, is_fragile=False)

if __name__ == '__main__':
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (black_1D_ring) -> in_box
    # object1 (white_3D_cylinder) -> in_box
    # object2 (red_3D_polyhedron) -> out_box
    # object3 (white_box) -> box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. It is prohibited to lift and relocate a container.
    # 2. When placing rigid objects in the bin, the soft objects must be in the bin before.
    # 3. If there is a soft object, push the object first.

    # Step 1: Pick out the red_3D_polyhedron from the box
    robot.pick_out(object2, object3)

    # Step 2: Push the white_3D_cylinder into the box (since it's soft)
    robot.push(object1, object3)

    # Step 3: Pick the white_3D_cylinder and place it in the box
    robot.pick(object1, object3)
    robot.place(object1, object3)

    # Step 4: Pick the black_1D_ring and place it in the box
    robot.pick(object0, object3)
    robot.place(object0, object3)

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Pick out the red_3D_polyhedron because it needs to be out of the box in the goal state.
    # 2. Push the white_3D_cylinder because it is a soft object and needs to be in the box.
    # 3. Pick and place the white_3D_cylinder to ensure it is properly placed in the box.
    # 4. Pick and place the black_1D_ring after the soft object is in the box, following the rule that rigid objects should be placed after soft objects.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == False  # The box itself should not be in another box

    print("All objects are in their goal states.")
