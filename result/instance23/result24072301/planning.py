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
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_heavy: bool
    
    # Object physical properties 
    is_rigid: bool
    is_fragile: bool
    is_soft: bool
    is_foldable: bool


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft objects in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
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
    in_box=False, 
    is_heavy=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_soft=True, 
    is_foldable=False
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
    in_box=False, 
    is_heavy=False, 
    is_rigid=True, 
    is_fragile=True, 
    is_soft=False, 
    is_foldable=False
)

object2 = Object(
    index=2, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_heavy=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_soft=False, 
    is_foldable=True
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
    in_box=True, 
    is_heavy=False, 
    is_rigid=False, 
    is_fragile=False, 
    is_soft=False, 
    is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: red_3D_polyhedron, not in box
    # object1: green_3D_cylinder, not in box
    # object2: yellow_2D_rectangle, in box
    # object3: white_box, in box

    # Goal State:
    # object0: red_3D_polyhedron, in box
    # object1: green_3D_cylinder, in box
    # object2: yellow_2D_rectangle, in box and folded
    # object3: white_box, in box

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object2) since it is foldable and already in the box.
    # 2. Pick and place the red_3D_polyhedron (object0) into the box.
    # 3. Pick and place the green_3D_cylinder (object1) into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    # Fold the yellow_2D_rectangle
    robot.fold(object2, box)

    # Pick and place the red_3D_polyhedron
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place the green_3D_cylinder
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold the yellow_2D_rectangle because it is foldable and already in the box.
    # 2. Pick and place the red_3D_polyhedron because it is soft and can be placed in the box.
    # 3. Pick and place the green_3D_cylinder because it is rigid and can be placed in the box after the soft object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_box == True
    print("All task planning is done")
