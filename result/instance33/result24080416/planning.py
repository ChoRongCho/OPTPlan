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
    is_elastic: bool
    is_fragile: bool
    is_rigid: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    can_be_packed: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.can_be_packed:
            # Check if there are any soft objects that need to be placed first
            soft_objects = [o for o in bin.in_bin_objects if o.is_soft and not o.in_box]
            if not soft_objects or all(o.in_box for o in soft_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name in bin.name}")
            else:
                print(f"Cannot Place {obj.name} before placing all soft objects")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
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
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_rigid=False, is_soft=True,
    in_box=False, can_be_packed=True
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_rigid=True, is_soft=False,
    in_box=False, can_be_packed=True
)

object2 = Object(
    index=2, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=False, is_rigid=False, is_soft=False,
    in_box=False, can_be_packed=True
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=False, is_rigid=False, is_soft=False,
    in_box=False, can_be_packed=True
)

object4 = Object(
    index=4, name='black_1D_linear', color='black', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=True, is_rigid=False, is_soft=False,
    in_box=True, can_be_packed=True
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_rigid=False, is_soft=False,
    in_box=False, can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_box,
        white_box.name: white_box.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        object4.name: True,
        white_box.name: [object0, object1, object2, object3, object4]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object first (object0)
    # 2. Place the elastic objects (object2, object3)
    # 3. Place the rigid object (object1)
    # 4. Place the fragile object (object4 is already in the box)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box
    
    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object2, box)
    robot.fold(object2, box)
    robot.place(object2, box)
    
    robot.pick(object3, box)
    robot.fold(object3, box)
    robot.place(object3, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object first to satisfy the rule that soft objects should be placed before rigid or fragile objects.
    # 2. Folded and placed the elastic objects to save space in the box.
    # 3. Placed the rigid object after ensuring all soft objects are in the box.
    # 4. The fragile object was already in the box, so no action was needed for it.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert set(white_box.in_bin_objects) == {object0, object1, object2, object3, object4}
    
    print("All task planning is done")
