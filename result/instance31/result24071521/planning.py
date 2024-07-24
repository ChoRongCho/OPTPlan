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
    is_rigid: bool
    is_elastic: bool
    is_fragile: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_heavy: bool
    is_large: bool


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
        if self.robot_handempty and obj not in bin.in_bin:
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
        if self.robot_handempty and obj in bin.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin:
            # Effects
            self.state_holding(obj)
            bin.in_bin.remove(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=[], is_rigid=True, is_elastic=False, is_fragile=False, is_heavy=False, is_large=False)
object1 = Object(index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=True, is_fragile=False, is_heavy=False, is_large=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=True, is_fragile=False, is_heavy=False, is_large=False)
object3 = Object(index=3, name='brown_2D_circle', color='brown', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=[3], is_rigid=False, is_elastic=True, is_fragile=True, is_heavy=False, is_large=False)
white_box = Object(index=4, name='white_box', color='white', shape='box', object_type='bin', pushed=False, folded=False, in_bin=[object3], is_rigid=False, is_elastic=False, is_fragile=False, is_heavy=False, is_large=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cylinder) in white_box
    # object1 (white_1D_ring) in white_box
    # object2 (blue_1D_ring) in white_box
    # object3 (brown_2D_circle) in white_box
    # white_box contains all objects

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = white_box

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: It is prohibited to lift and relocate a container
    # Rule 2: When fold an object, the object must be foldable
    # Rule 3: When place a fragile object, the soft objects must be in the bin
    # Rule 4: When a soft object is in the bin at the initial state, take it out and replace it into the bin

    # Step-by-step action sequence
    # 1. Pick out the brown_2D_circle (soft and fragile) from the white_box
    robot.pick_out(object3, bin)

    # 2. Pick and place the yellow_3D_cylinder into the white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick and place the white_1D_ring into the white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 4. Pick and place the blue_1D_ring into the white_box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # 5. Place the brown_2D_circle back into the white_box
    robot.place(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 in bin.in_bin
    assert bin.in_bin == [object0, object1, object2, object3]
    print("All task planning is done")
