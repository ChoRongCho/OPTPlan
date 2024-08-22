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
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
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
    in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=True, 
    in_box=False, 
    is_packable=True
)

object2 = Object(
    index=2, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_rigid=False, 
    in_box=False, 
    is_packable=True
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: red_3D_polyhedron, out_box, is_soft, is_packable
    # object1: black_3D_cylinder, out_box, is_rigid, is_packable
    # object2: white_2D_circle, out_box, is_soft, is_packable
    # object3: white_box, box, in_bin_objects=[], is_packable=False

    # Goal State
    # object0: red_3D_polyhedron, in_box, is_soft, is_packable
    # object1: black_3D_cylinder, in_box, is_rigid, is_packable
    # object2: white_2D_circle, in_box, is_soft, is_packable
    # object3: white_box, box, in_bin_objects=[object0, object1, object2], is_packable=False

    # Second, using given rules and object's states, make a task planning strategy
    # According to the rules:
    # 1. Place soft objects first before placing rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Place soft objects first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Now place the rigid object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Push soft objects if needed (not necessary in this case as they are already in the box)
    # robot.push(object0, box)
    # robot.push(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Pick and place red_3D_polyhedron (soft) first.
    # 2. Pick and place white_2D_circle (soft) second.
    # 3. Pick and place black_3D_cylinder (rigid) last.
    # 4. No need to push as all objects are already in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object0, object1, object2]
    
    print("All task planning is done")
