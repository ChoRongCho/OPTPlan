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
    is_elastic: bool
    is_foldable: bool
    
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
        if obj.in_box:
            print(f"Cannot pick {obj.name}, it is already in the bin.")
            return False
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name}, robot hand is not empty.")
            return False
        print(f"Pick {obj.name}")
        self.state_holding(obj)
        return True
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if not self.robot_now_holding:
            print(f"Cannot place {obj.name}, robot is not holding any object.")
            return False
        if obj.is_soft:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
            return True
        else:
            soft_objects = [o for o in bin.in_bin_objects if o.is_soft]
            if soft_objects:
                print(f"Cannot place {obj.name}, soft objects should be placed first.")
                return False
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
            return True
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if not self.robot_handempty:
            print(f"Cannot push {obj.name}, robot hand is not empty.")
            return False
        if not obj.is_soft:
            print(f"Cannot push {obj.name}, only soft objects can be pushed.")
            return False
        print(f"Push {obj.name}")
        obj.pushed = True
        return True
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name}, robot hand is not empty.")
            return False
        if not obj.is_foldable:
            print(f"Cannot fold {obj.name}, it is not foldable.")
            return False
        print(f"Fold {obj.name}")
        obj.folded = True
        return True
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj not in bin.in_bin_objects:
            print(f"Cannot out {obj.name}, it is not in the bin.")
            return False
        print(f"Out {obj.name} from {bin.name}")
        bin.in_bin_objects.remove(obj)
        obj.in_box = False
        self.state_handempty()
        return True

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
    is_soft=False, 
    is_elastic=False, 
    is_foldable=True, 
    in_box=False, 
    is_packed=False
)

object1 = Object(
    index=1, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=True, 
    is_foldable=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_elastic=False, 
    is_foldable=False, 
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
    in_bin_objects=[object2], 
    is_soft=False, 
    is_elastic=False, 
    is_foldable=False, 
    in_box=False, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not pushed, not folded, not in box, not packed
    # object1: out_box, not pushed, not folded, not in box, not packed
    # object2: in_box, not pushed, not folded, in box, not packed
    # object3: box, not pushed, not folded, contains object2, not packed

    # Goal state:
    # object0: in_box, not pushed, folded, in box, packed
    # object1: in_box, not pushed, not folded, in box, packed
    # object2: in_box, not pushed, not folded, in box, packed
    # object3: box, not pushed, not folded, contains object0, object1, object2, not packed

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold object0 (yellow_2D_rectangle) since it is foldable.
    # 2. Pick and place object0 into the box.
    # 3. Pick and place object1 (transparent_3D_cylinder) into the box.
    # 4. Ensure object2 (red_3D_polyhedron) is already in the box.
    # 5. Mark all objects as packed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    # Fold object0
    robot.fold(object0, box)
    # Pick and place object0 into the box
    robot.pick(object0, box)
    robot.place(object0, box)
    # Pick and place object1 into the box
    robot.pick(object1, box)
    robot.place(object1, box)
    # Ensure object2 is already in the box (no action needed)
    # Mark all objects as packed
    object0.is_packed = True
    object1.is_packed = True
    object2.is_packed = True

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Fold object0 because it is foldable.
    # - Place object0 and object1 into the box after ensuring object2 (soft object) is already in the box.
    # - Mark all objects as packed to satisfy the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.folded == True
    assert object0.is_packed == True

    assert object1.in_box == True
    assert object1.is_packed == True

    assert object2.in_box == True
    assert object2.is_packed == True

    assert object3.in_bin_objects == [object2, object0, object1]

    print("All task planning is done")
