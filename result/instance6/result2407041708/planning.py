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
    is_fragile: bool = False
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
        self.robot_now_holding = False
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
        if self.robot_handempty and not obj.is_in_box and obj.is_packable:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and not obj.is_in_box:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and not obj.is_in_box:
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
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, is_in_box=False)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, is_in_box=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=True)
object3 = Object(index=3, name='orange_2D_triangle', color='orange', shape='2D_triangle', object_type='obj', is_fragile=True, is_in_box=True)
object4 = Object(index=4, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj', is_elastic=True, is_in_box=True)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', is_in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_2D_rectangle) -> in_box
    # object1 (transparent_3D_cylinder) -> in_box
    # object2 (red_3D_polyhedron) -> in_box
    # object3 (orange_2D_triangle) -> in_box
    # object4 (green_2D_rectangle) -> in_box
    # object5 (white_box) -> box (remains the same)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object5

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: it is prohibited to lift and relocate a container
    # Rule 2: when place a rigid objects in the bin, the soft objects must be in the bin before
    # Rule 4: if there is a foldable object, fold the object on the platform not in the bin

    # Action sequence:
    # 1. Fold the foldable object (yellow_2D_rectangle) on the platform
    robot.fold(object0, bin)
    
    # 2. Pick and place the soft object (red_3D_polyhedron) in the bin (already in the bin)
    # No action needed as it is already in the bin

    # 3. Pick and place the elastic object (transparent_3D_cylinder) in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 4. Pick and place the foldable object (yellow_2D_rectangle) in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 5. Pick and place the fragile object (orange_2D_triangle) in the bin (already in the bin)
    # No action needed as it is already in the bin

    # 6. Pick and place the elastic object (green_2D_rectangle) in the bin (already in the bin)
    # No action needed as it is already in the bin

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    print("All task planning is done")
