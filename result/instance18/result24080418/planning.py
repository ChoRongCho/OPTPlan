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
    is_fragile: bool
    is_elastic: bool
    is_soft: bool
    
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
        # Preconditions
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and (not obj.is_fragile or any(o.is_soft for o in bin.in_bin_objects)):
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.is_packed = True
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
            obj.in_box = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    is_packed=False
)

object1 = Object(
    index=1, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_elastic=True, 
    is_soft=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=True, 
    is_packed=False
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
    is_fragile=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in box, not packed
    # object1: out_box, not pushed, not folded, not in box, not packed
    # object2: in_box, not pushed, not folded, in box, not packed
    # object3: box, not pushed, not folded, not in box, not packed

    # Final State:
    # object0: in_box, not pushed, not folded, in box, packed
    # object1: in_box, not pushed, not folded, in box, packed
    # object2: in_box, not pushed, not folded, in box, packed
    # object3: box, not pushed, not folded, in box, packed

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the non-fragile, non-soft object (object1).
    # 3. Ensure the fragile object (object2) is already in the box.
    # 4. Push the soft object (object0) if needed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object0, box)  # Pick yellow_3D_cuboid
    robot.place(object0, box)  # Place yellow_3D_cuboid in white_box

    robot.pick(object1, box)  # Pick transparent_2D_circle
    robot.place(object1, box)  # Place transparent_2D_circle in white_box

    # object2 (black_2D_ring) is already in the box, so no need to pick and place

    # Push the soft object if needed (not necessary in this case as it is already placed)
    # robot.push(object0, box)  # Push yellow_3D_cuboid

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object0) first to satisfy the rule for placing fragile objects.
    # 2. Placed the non-fragile, non-soft object (object1) next.
    # 3. The fragile object (object2) was already in the box.
    # 4. No need to push the soft object as it was already placed correctly.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object0, object1, object2]
    assert object0.is_packed == True
    assert object1.is_packed == True
    assert object2.is_packed == True

    print("All task planning is done")
