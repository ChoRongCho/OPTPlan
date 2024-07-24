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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_soft or (not obj.is_soft and all(o.is_soft for o in bin if o.is_in_box)):
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
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Create objects based on the initial state
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_soft=True, is_in_box=True, is_fragile=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_soft=False, is_in_box=True, is_fragile=False)

if __name__ == "__main__":
    # Create the robot instance
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal: All objects should be in the box
    goal_state = {
        object0.name: True,  # brown_3D_cuboid should be in the box
        object1.name: True,  # black_1D_ring should be in the box
        object2.name: True   # white_box should be in the box (already in the box)
    }

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. Avoid handling and moving any box
    # 2. When placing a soft object, the elastic object must be in the bin
    # 3. When placing a rigid object, the soft objects must be in the bin
    # 4. When a rigid object is in the bin at the initial state, take out the rigid object first

    # Since there are no rigid objects in the bin initially, we can proceed with placing the soft objects.

    # Step 1: Pick the brown_3D_cuboid (soft object) and place it in the box
    robot.pick(object0, object2)  # Pick brown_3D_cuboid
    robot.place(object0, object2)  # Place brown_3D_cuboid in white_box

    # Step 2: The black_1D_ring is already in the box, so no action is needed for it.

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - We picked and placed the brown_3D_cuboid (soft object) in the box because it was outside initially.
    # - The black_1D_ring (soft object) was already in the box, so no action was needed.
    # - The white_box (box) was not handled or moved as per rule 1.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == goal_state[object0.name], f"{object0.name} is not in the box as expected."
    assert object1.is_in_box == goal_state[object1.name], f"{object1.name} is not in the box as expected."
    assert object2.is_in_box == goal_state[object2.name], f"{object2.name} is not in the box as expected."

    print("All objects are in the correct final state.")
