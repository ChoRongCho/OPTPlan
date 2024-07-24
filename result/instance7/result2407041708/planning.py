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
    is_foldable: bool = False
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
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
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
        if self.robot_handempty and obj.is_foldable:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False, is_packable=True)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=True, is_packable=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_packable=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: out_box, is_foldable
    # object1: in_box, is_soft
    # object2: in_box, is_elastic
    # object3: in_box, is_soft
    # object4: box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules

    # Rule 2: Fold the foldable object (object0)
    robot.fold(object0, bin)

    # Rule 3: Pick out the rigid object in the bin (object3 is soft, so no rigid object to pick out)

    # Pick and place the objects according to the goal state
    robot.pick(object1, bin)
    robot.place(object1, bin)

    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Rule 4: Push the soft object in the bin (object3)
    robot.push(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == False
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == False
    print("All task planning is done")
