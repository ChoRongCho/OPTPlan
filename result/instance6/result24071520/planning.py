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
    is_soft: bool
    is_foldable: bool
    is_elastic: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


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
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
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
        if self.robot_handempty and obj.object_type == 'obj' and obj in bin.in_bin:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and obj.object_type == 'obj' and obj not in bin.in_bin:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            bin.in_bin.remove(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin=False, is_soft=False, is_foldable=True, is_elastic=False, is_fragile=False, is_heavy=False)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin=False, is_soft=False, is_foldable=False, is_elastic=True, is_fragile=False, is_heavy=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin=True, is_soft=True, is_foldable=False, is_elastic=False, is_fragile=False, is_heavy=False)
object3 = Object(index=3, name='orange_2D_rectangle', color='orange', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin=True, is_soft=False, is_foldable=True, is_elastic=False, is_fragile=False, is_heavy=False)
object4 = Object(index=4, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin=True, is_soft=False, is_foldable=False, is_elastic=True, is_fragile=False, is_heavy=False)
bin = Object(index=5, name='white_box', color='white', shape='box', object_type='bin', pushed=False, folded=False, in_bin=[], is_soft=False, is_foldable=False, is_elastic=False, is_fragile=False, is_heavy=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: in_box, folded
    # object1: in_box
    # object2: in_box
    # object3: in_box, folded
    # object4: in_box
    # bin: contains all objects

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: it is prohibited to lift and relocate a container
    # Rule 2: when place a rigid objects in the bin, the soft objects must be in the bin before
    # Rule 4: if there is a foldable object, fold the object on the platform not in the bin

    # Step-by-step action sequence
    # 1. Fold the foldable objects on the platform
    robot.fold(object0, bin)  # Fold yellow_2D_rectangle
    robot.fold(object3, bin)  # Fold orange_2D_rectangle

    # 2. Place the soft object in the bin first
    # object2 (red_3D_polyhedron) is already in the bin

    # 3. Place the foldable objects in the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)
    robot.pick(object3, bin)
    robot.place(object3, bin)

    # 4. Place the elastic objects in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)
    robot.pick(object4, bin)
    robot.place(object4, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin and object0.folded == True
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 in bin.in_bin and object3.folded == True
    assert object4 in bin.in_bin
    print("All task planning is done")
