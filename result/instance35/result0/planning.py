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
    is_foldable: bool

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
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = True
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_foldable and self.robot_handempty:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=False, is_foldable=False, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_elastic=False, is_foldable=False, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_soft=False, is_elastic=True, is_foldable=False, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_soft=False, is_elastic=False, is_foldable=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_soft=False, is_elastic=False, is_foldable=False, is_in_box=True, is_out_box=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal state:
    # yellow_3D_cuboid: is_in_box = True, is_out_box = False
    # red_3D_polyhedron: is_in_box = True, is_out_box = False
    # white_1D_ring: is_in_box = False, is_out_box = True
    # black_1D_ring: is_in_box = False, is_out_box = True
    # white_box: is_in_box = True, is_out_box = False (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Plan:
    # 1. Push yellow_3D_cuboid into the box
    robot.push(object0, object4)
    
    # 2. Push red_3D_polyhedron into the box
    robot.push(object1, object4)
    
    # 3. Pick out white_1D_ring from the box
    robot.pick_out(object2, object4)
    
    # 4. Pick out black_1D_ring from the box
    robot.pick_out(object3, object4)

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. yellow_3D_cuboid is soft, so it can be pushed into the box (Rule 4).
    # 2. red_3D_polyhedron is soft, so it can be pushed into the box (Rule 4).
    # 3. white_1D_ring is elastic but not soft, so it cannot be pushed or folded. It needs to be picked out.
    # 4. black_1D_ring is foldable, but since it needs to be out of the box, it is picked out.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == False and object2.is_out_box == True
    assert object3.is_in_box == False and object3.is_out_box == True
    assert object4.is_in_box == True and object4.is_out_box == False

    print("All objects are in their goal states.")
