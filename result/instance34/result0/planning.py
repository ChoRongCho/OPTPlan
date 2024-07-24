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
    is_soft: bool = False
    is_foldable: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    is_elastic: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = False


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
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
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
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
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


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_foldable=True, is_fragile=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # Initialize the robot and objects
    robot = Robot()
    bin = object4  # The bin is the white_box

    # Objects
    objects = [object0, object1, object2, object3, object4]

    # Final state description
    # All objects except the bin should be in the box
    goal_state = {
        object0: 'in_box',
        object1: 'in_box',
        object2: 'in_box',
        object3: 'in_box',
        object4: 'box'  # The bin itself
    }

    # Action sequence to achieve the goal state
    # 1. Pick the red_3D_polyhedron (soft object) and place it in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick the yellow_3D_cylinder (rigid object) and place it in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 3. The white_1D_ring and black_1D_ring are already in the bin, no action needed for them

    # Check if the goal state is satisfying the goal state table
    for obj in objects:
        if obj == bin:
            assert obj.is_in_box == False and obj.is_out_box == False, f"{obj.name} is not in the correct state"
        else:
            assert obj.is_in_box == True, f"{obj.name} is not in the correct state"

    print("All objects are in the correct state according to the goal state table.")
