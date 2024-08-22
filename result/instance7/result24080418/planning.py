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
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        if self.robot_now_holding == obj and obj.out_box == False:
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and obj.in_box and self.robot_handempty:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_foldable and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and self.robot_handempty:
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
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
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

white_box = Object(
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
    # Initial state:
    # object0: out_box
    # object1: out_box
    # object2: out_box
    # object3: in_box
    # white_box: empty

    # Goal state:
    # object0: in_box, folded
    # object1: in_box
    # object2: in_box
    # object3: in_box
    # white_box: contains [object0, object1, object2, object3]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold object0 (yellow_2D_rectangle) since it is foldable.
    # 2. Pick and place object1 (brown_3D_cuboid) since it is soft.
    # 3. Pick and place object3 (red_3D_polyhedron) since it is already in the box.
    # 4. Pick and place object0 (yellow_2D_rectangle) since it is now folded.
    # 5. Pick and place object2 (blue_2D_ring) since it is neither soft nor foldable.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box

    # Action sequence
    robot.fold(object0, box)  # Fold yellow_2D_rectangle
    robot.pick(object1, box)  # Pick brown_3D_cuboid
    robot.place(object1, box)  # Place brown_3D_cuboid in white_box
    robot.pick(object3, box)  # Pick red_3D_polyhedron (already in box)
    robot.place(object3, box)  # Place red_3D_polyhedron in white_box
    robot.pick(object0, box)  # Pick yellow_2D_rectangle (now folded)
    robot.place(object0, box)  # Place yellow_2D_rectangle in white_box
    robot.pick(object2, box)  # Pick blue_2D_ring
    robot.place(object2, box)  # Place blue_2D_ring in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold object0 because it is foldable.
    # 2. Place object1 first because it is soft.
    # 3. Place object3 next because it is already in the box and is soft.
    # 4. Place object0 after folding it.
    # 5. Place object2 last because it is neither soft nor foldable.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3}
    print("All task planning is done")
