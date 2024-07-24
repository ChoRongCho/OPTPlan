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
    is_foldable: bool = False
    is_soft: bool = False

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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_out_box = True
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and not obj.is_rigid and not obj.is_in_box:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            obj.is_rigid = True  # Assuming folding makes it rigid
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")
            self.state_handempty()

    def dummy(self):
        pass


object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_out_box=True)
object1 = Object(index=1, name='white_3D_cone', color='white', shape='3D_cone', object_type='obj', is_foldable=True, is_out_box=True)
object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # Final state of each object according to the goal table
    goal_state = {
        object0: {'is_in_box': True, 'is_out_box': False},
        object1: {'is_in_box': True, 'is_out_box': False},
        object2: {'is_in_box': True, 'is_out_box': False},
        object3: {'is_in_box': True, 'is_out_box': False}
    }

    # Action sequence to achieve the goal state
    # 1. Fold the white_3D_cone (object1) to make it rigid
    robot.fold(object1, object3)
    
    # 2. Pick the black_3D_cylinder (object0) and place it in the white_box (object3)
    robot.pick(object0, object3)
    robot.place(object0, object3)
    
    # 3. Pick the white_3D_cone (object1) and place it in the white_box (object3)
    robot.pick(object1, object3)
    robot.place(object1, object3)
    
    # 4. The brown_3D_cuboid (object2) is already in the box, no action needed

    # Check if the goal state is satisfying the goal state table
    for obj, state in goal_state.items():
        assert obj.is_in_box == state['is_in_box'], f"{obj.name} is not in the correct state"
        assert obj.is_out_box == state['is_out_box'], f"{obj.name} is not in the correct state"

    print("All objects are in the correct state.")
