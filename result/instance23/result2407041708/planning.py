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
    is_fragile: bool = False
    is_rigid: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_heavy: bool = False


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
            if obj.is_rigid and not any(o.is_soft for o in bin):
                return  # Cannot place rigid object if no soft objects in bin
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
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=False)
object1 = Object(index=1, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', is_fragile=True, is_rigid=True, is_in_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (red_3D_polyhedron) -> in_box
    # object1 (green_2D_circle) -> in_box
    # object2 (white_box) -> box (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object2

    # Third, after making all actions, fill your reasons according to the rules
    # Step 1: Push the soft object (red_3D_polyhedron) into the box
    robot.push(object0, bin)
    # Reason: According to rule 4, we can push soft objects into the bin.

    # Step 2: Pick and place the rigid object (green_2D_circle) into the box
    robot.pick(object1, bin)
    robot.place(object1, bin)
    # Reason: According to rule 2, we can place rigid objects into the bin if there are already soft objects in the bin.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True  # The box itself is always in the box
    print("All task planning is done")
