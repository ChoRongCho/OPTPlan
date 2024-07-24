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
    is_elastic: bool
    is_soft: bool
    is_foldable: bool
    in_box: bool


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
        # Preconditions: Robot hand must be empty, object must not be in the bin, object must not be a box
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, object must not be a box
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft, object must be in the bin
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be in the bin, object must not be a box
        if self.robot_handempty and obj.in_box and obj.object_type != 'box':
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to adhere strictly to the given rules for the bin_packing task. The preconditions ensure that the robot does not perform actions that violate these rules, such as picking or placing a box, or failing to fold a foldable object. The effects update the state of the robot and objects to reflect the outcome of each action, ensuring consistency and enabling proper task planning. This approach ensures that the robot's behavior is predictable and rule-compliant, facilitating effective bin packing

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
    in_bin_objects=None, 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=True, 
    in_box=False
)

object1 = Object(
    index=1, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=True, 
    is_soft=True, 
    is_foldable=False, 
    in_box=False
)

object2 = Object(
    index=2, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False, 
    in_box=False
)

object3 = Object(
    index=3, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=False, 
    is_soft=True, 
    is_foldable=False, 
    in_box=True
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=None, 
    folded=None, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False, 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not folded
    # object1: out_box, not pushed
    # object2: out_box
    # object3: in_box
    # object4: box, empty

    # Final State:
    # object0: out_box, folded
    # object1: in_box, pushed
    # object2: in_box
    # object3: out_box
    # object4: box, contains object1 and object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the foldable object (object0)
    # 2. Out the rigid object in the bin (object3) and replace it into the bin
    # 3. Pick and place object1 into the bin
    # 4. Push the soft object (object1) in the bin
    # 5. Pick and place object2 into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Fold the foldable object (object0)
    robot.fold(object0, box)

    # Out the rigid object in the bin (object3)
    robot.out(object3, box)

    # Place the rigid object back into the bin
    robot.place(object3, box)

    # Pick and place object1 into the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Push the soft object (object1) in the bin
    robot.push(object1, box)

    # Pick and place object2 into the bin
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Never pick and place a box - Followed
    # Rule 2: Fold the foldable object - Followed (object0)
    # Rule 3: Out and replace rigid object in the bin - Followed (object3)
    # Rule 4: Push the soft object in the bin - Followed (object1)

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == False
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object3.in_box == False
    assert object4.in_bin_objects == [object1, object2]
    print("All task planning is done")
