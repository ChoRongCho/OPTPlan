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
    is_soft: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
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
        if obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
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
        if obj.in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=False, is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=False, is_soft=True, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_soft=False, in_box=False, out_box=True)
object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=True, is_soft=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_fragile=False, is_soft=False, in_box=True, out_box=False)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_fragile=False, is_soft=False, in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {"in_box": False, "out_box": True},
        "object1": {"in_box": False, "out_box": True},
        "object2": {"in_box": False, "out_box": True},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_box": True, "out_box": False},
        "object5": {"in_box": True, "out_box": False, "in_bin_objects": []}
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_box": True, "out_box": False},
        "object5": {"in_box": True, "out_box": False, "in_bin_objects": [0, 1, 2, 3, 4]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place soft objects first (object0, object1)
    # 2. Pick and place other objects (object2)
    # 3. Ensure all objects are in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place soft objects first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Pick and place other objects after soft objects are in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    print("All task planning is done")
