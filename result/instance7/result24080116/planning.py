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
    is_foldable: bool
    is_soft: bool
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
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
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if obj.out_box and self.robot_handempty:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
            print(f"Picked {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        if obj.in_box and self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.append(obj)
            print(f"Placed {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        if obj.is_soft and self.robot_handempty:
            obj.pushed = True
            print(f"Pushed {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        if obj.is_foldable and self.robot_handempty:
            obj.folded = True
            print(f"Folded {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=True, 
    is_soft=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_foldable=False, 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='blue_2D_loop', 
    color='blue', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=True, 
    in_box=True, 
    out_box=False
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "yellow_2D_rectangle": "out_box",
        "brown_3D_cuboid": "out_box",
        "blue_2D_loop": "out_box",
        "red_3D_polyhedron": "in_box",
        "white_box": "box"
    }
    
    # Goal state
    goal_state = {
        "yellow_2D_rectangle": "in_box",
        "brown_3D_cuboid": "in_box",
        "blue_2D_loop": "in_box",
        "red_3D_polyhedron": "in_box"
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the brown_3D_cuboid (soft object) first.
    # 2. Pick and place the yellow_2D_rectangle (foldable object).
    # 3. Pick and place the blue_2D_loop (rigid object).
    # 4. Ensure the red_3D_polyhedron is already in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object1, box)  # Pick brown_3D_cuboid
    robot.place(object1, box)  # Place brown_3D_cuboid in the box

    robot.pick(object0, box)  # Pick yellow_2D_rectangle
    robot.fold(object0, box)  # Fold yellow_2D_rectangle
    robot.place(object0, box)  # Place yellow_2D_rectangle in the box

    robot.pick(object2, box)  # Pick blue_2D_loop
    robot.place(object2, box)  # Place blue_2D_loop in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (brown_3D_cuboid) first as per the rule.
    # 2. Folded the foldable object (yellow_2D_rectangle) before placing it.
    # 3. Placed the rigid object (blue_2D_loop) after the soft object was already in the box.
    # 4. The red_3D_polyhedron was already in the box, so no action was needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    print("All task planning is done")
