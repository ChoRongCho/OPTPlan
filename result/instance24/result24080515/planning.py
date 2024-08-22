from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: list
    
    # Object physical properties 
    is_foldable: bool
    is_rigid: bool
    is_fragile: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, soft objects should be in the box if there are any
        if self.robot_now_holding == obj and all(o.is_elastic and o.in_box for o in bin.in_bin_objects if o.is_elastic):
            print(f"Place {obj.name} in {bin.name}")
            obj.in_box = True
            obj.is_packed = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft and in the bin
        if self.robot_handempty and obj.is_elastic and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            obj.in_box = False
            obj.is_packed = False
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_rigid=False, is_fragile=False, is_elastic=False,
    in_box=False, is_packed=False
)

object1 = Object(
    index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=True, is_fragile=True, is_elastic=False,
    in_box=False, is_packed=False
)

object2 = Object(
    index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=True, is_fragile=False, is_elastic=False,
    in_box=False, is_packed=False
)

object3 = Object(
    index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_rigid=False, is_fragile=False, is_elastic=False,
    in_box=False, is_packed=False
)

object4 = Object(
    index=4, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_fragile=False, is_elastic=True,
    in_box=False, is_packed=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_fragile=False, is_elastic=False,
    in_box=False, is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given table

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold foldable objects
    # 2. Place the elastic object first
    # 3. Place the remaining objects in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Fourth, after making all actions, fill your reasons according to the rules

    # Fold foldable objects
    robot.fold(object0, box)
    robot.fold(object3, box)

    # Place the elastic object first
    robot.pick(object4, box)
    robot.place(object4, box)
    robot.push(object4, box)

    # Place the remaining objects in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    robot.pick(object1, box)
    robot.place(object1, box)

    robot.pick(object2, box)
    robot.place(object2, box)

    robot.pick(object3, box)
    robot.place(object3, box)

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_box == True

    assert object0.folded == True
    assert object3.folded == True
    assert object4.pushed == True

    print("All task planning is done")
