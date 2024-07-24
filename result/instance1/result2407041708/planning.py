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
    is_elastic: bool = False
    is_rigid: bool = False
    is_soft: bool = False

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
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid and any(o.is_soft for o in bin if o.is_in_box):
                # Effects
                obj.is_in_box = True
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
            elif not obj.is_rigid:
                # Effects
                obj.is_in_box = True
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} due to rule constraints")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False, is_packable=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_packable=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) -> in_box
    # object1 (black_3D_cylinder) -> in_box
    # object2 (blue_1D_ring) -> out_box
    # object3 (white_box) -> box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # c) Make the action sequence
    # Step 1: Pick the soft object (brown_3D_cuboid) and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 2: Pick the elastic object (blue_1D_ring) and place it in the box temporarily to satisfy the rule for fragile objects
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Step 3: Pick the rigid object (black_3D_cylinder) and place it in the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 4: Pick out the elastic object (blue_1D_ring) from the box to satisfy the goal state
    robot.pick_out(object2, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Pick and place the soft object first to allow placing the rigid object later.
    # 2. Temporarily place the elastic object to satisfy the rule for placing fragile objects.
    # 3. Place the rigid object after the soft object is already in the box.
    # 4. Remove the elastic object to achieve the final goal state.

    # Fourth, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    print("All task planning is done")