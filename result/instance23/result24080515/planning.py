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
    is_soft: bool
    is_rigid: bool
    is_fragile: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packable: bool


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
        if self.robot_now_holding == obj and obj.is_packable:
            if obj.is_fragile or obj.is_rigid:
                if any(o.is_soft and not o.in_box for o in bin.in_bin_objects):
                    print(f"Cannot Place {obj.name} before soft objects")
                    return
            # Effects
            self.state_handempty()
            obj.in_box = True
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
        if self.robot_handempty and obj.is_packable:
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
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_rigid=False, 
    is_fragile=False, 
    in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=True, 
    is_fragile=True, 
    in_box=False, 
    is_packable=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=False, 
    is_fragile=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: red_3D_polyhedron, in_box=False
    # object1: green_3D_cylinder, in_box=False
    # object2: white_box, in_box=True, in_bin_objects=[]
    
    # Goal State:
    # object0: red_3D_polyhedron, in_box=True
    # object1: green_3D_cylinder, in_box=True
    # object2: white_box, in_box=True, in_bin_objects=[object0, object1]
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick red_3D_polyhedron (soft object)
    # 2. Place red_3D_polyhedron in white_box
    # 3. Pick green_3D_cylinder (rigid and fragile object)
    # 4. Place green_3D_cylinder in white_box
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object2
    
    # Action Sequence:
    robot.pick(object0, box)  # Pick red_3D_polyhedron
    robot.place(object0, box)  # Place red_3D_polyhedron in white_box
    robot.pick(object1, box)  # Pick green_3D_cylinder
    robot.place(object1, box)  # Place green_3D_cylinder in white_box
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Pick red_3D_polyhedron: No preconditions violated.
    # 2. Place red_3D_polyhedron: No preconditions violated.
    # 3. Pick green_3D_cylinder: No preconditions violated.
    # 4. Place green_3D_cylinder: Placed after soft object as per rule.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")