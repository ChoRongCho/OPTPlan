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
    is_rigid: bool
    is_fragile: bool

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
        if obj.object_type != 'box' and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and not obj.is_in_box:
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
        if self.robot_handempty and obj.is_out_box:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Create objects based on the initial state table
object0 = Object(index=0, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_rigid=True, is_fragile=False, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_fragile=False, is_in_box=True, is_out_box=False)

# Create a bin object (assuming the bin is also an object)
bin = Object(index=3, name='bin', color='gray', shape='box', object_type='box', is_rigid=True, is_fragile=False, is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal State:
    # black_1D_ring: out_box
    # green_3D_cylinder: in_box
    # white_box: in_box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    robot = Robot()

    # Step 1: Pick the green_3D_cylinder (fragile object)
    robot.pick(object1, bin)
    
    # Step 2: Place the green_3D_cylinder in the white_box
    robot.place(object1, bin)
    
    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. We never attempt to pick up and set down an object named box.
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before. (Not applicable here as we are not placing any rigid object in the bin)
    # 3. When placing a fragile object, the elastic objects must be in the bin. (Not applicable here as there are no elastic objects)
    # 4. When a soft object is in the bin at the initial state, take it out and replace it into the bin. (Not applicable here as there are no soft objects in the initial state)

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == False and object0.is_out_box == True, "black_1D_ring is not in the correct state"
    assert object1.is_in_box == True and object1.is_out_box == False, "green_3D_cylinder is not in the correct state"
    assert object2.is_in_box == True and object2.is_out_box == False, "white_box is not in the correct state"

    print("Goal state achieved successfully!")
