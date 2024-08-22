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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.in_box == False and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.is_packable:
            if obj.is_soft or all(o.is_soft for o in bin.in_bin_objects):
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name in bin.name}")
            else:
                print(f"Cannot Place {obj.name} because soft objects are not in the box")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj in bin.in_bin_objects:
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
    is_packable=True
)

object1 = Object(
    index=1, 
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
    in_box=False, 
    is_packable=True
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
    is_elastic=True, 
    is_foldable=False, 
    is_soft=False, 
    in_box=True, 
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
    in_bin_objects=[object2], 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=False, 
    in_box=False, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in box
    # object1: out_box, not pushed, not folded, not in box
    # object2: in_box, not pushed, not folded, in box
    # object3: box, not pushed, not folded, contains object2

    # Goal State:
    # object0: in_box, not pushed, folded, in box
    # object1: in_box, pushed, not folded, in box
    # object2: in_box, not pushed, not folded, in box
    # object3: box, not pushed, not folded, contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the soft object (object1) first.
    # 2. Fold the foldable object (object0) before placing it.
    # 3. Place the folded object (object0) in the box.
    # 4. Push the soft object (object1) after placing it in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object1, box)  # Pick red_3D_polyhedron
    robot.place(object1, box)  # Place red_3D_polyhedron in the box
    robot.fold(object0, box)  # Fold yellow_2D_rectangle
    robot.pick(object0, box)  # Pick yellow_2D_rectangle
    robot.place(object0, box)  # Place yellow_2D_rectangle in the box
    robot.push(object1, box)  # Push red_3D_polyhedron

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Pick and place the soft object (object1) first to satisfy the rule that soft objects should be in the box before placing rigid objects.
    # 2. Fold the foldable object (object0) before placing it to satisfy the rule that foldable objects should be folded.
    # 3. Place the folded object (object0) in the box.
    # 4. Push the soft object (object1) after placing it in the box to satisfy the rule that soft objects should be pushed after placing.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object2, object1, object0]
    print("All task planning is done")
