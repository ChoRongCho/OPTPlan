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
    is_packed: bool
    
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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
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
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules and ensure logical consistency in the bin_packing task. 
# The 'pick' action ensures that only objects (not boxes) that are not already in the bin can be picked up if the robot's hand is empty.
# The 'place' action ensures that the object being placed is currently held by the robot and is not a box.
# The 'push' action ensures that the robot's hand is empty and the object is already in the bin.
# The 'fold' action ensures that the object is foldable and the robot's hand is empty.
# The 'out' action ensures that the object is in the bin and the robot's hand is empty before removing it from the bin.
# These actions and their preconditions/effects are designed to maintain the integrity of the bin_packing process and adhere to the specified rules.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_rigid=False, is_fragile=False, is_soft=True, is_foldable=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_rigid=True, is_fragile=False, is_soft=False, is_foldable=False
)

object2 = Object(
    index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_rigid=False, is_fragile=False, is_soft=True, is_foldable=True
)

object3 = Object(
    index=3, name='white_1D_linear', color='white', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_rigid=False, is_fragile=True, is_soft=False, is_foldable=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], in_box=False, is_packed=False,
    is_rigid=False, is_fragile=False, is_soft=False, is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box, not packed
    # object1: out_box, not packed
    # object2: in_box, not packed
    # object3: in_box, not packed
    # white_box: contains object2 and object3

    # Goal State
    # object0: in_bin, packed
    # object1: in_bin, packed
    # object2: in_bin, packed, folded
    # object3: in_box, packed
    # white_box: contains object3

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold object2 (black_2D_ring) since it is foldable and needs to be folded in the goal state.
    # 2. Place object0 (red_3D_polyhedron) in the bin.
    # 3. Place object2 (black_2D_ring) in the bin.
    # 4. Place object1 (yellow_3D_cylinder) in the bin.
    # 5. Ensure object3 (white_1D_linear) remains in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Perform the actions
    # Step 1: Fold object2 (black_2D_ring)
    robot.fold(object2, box)

    # Step 2: Pick and place object0 (red_3D_polyhedron) in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Pick and place object2 (black_2D_ring) in the bin
    robot.out(object2, box)
    robot.place(object2, box)

    # Step 4: Pick and place object1 (yellow_3D_cylinder) in the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 5: Ensure object3 (white_1D_linear) remains in the box (no action needed)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Fold action is performed on object2 because it is foldable.
    # 2. Object0 is placed in the bin first because it is soft and must be in the bin before placing the rigid object1.
    # 3. Object2 is placed in the bin after folding.
    # 4. Object1 is placed in the bin after object0 to satisfy the rule that soft objects must be in the bin before rigid objects.
    # 5. Object3 remains in the box as required by the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object2.folded == True
    assert object3.in_box == True
    assert object0.is_packed == True
    assert object1.is_packed == True
    assert object2.is_packed == True
    assert object3.is_packed == True
    print("All task planning is done")
