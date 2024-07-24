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
    is_soft: bool
    is_foldable: bool
    
    # Object physical properties
    init_pose: str
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
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
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
            if bin.in_bin_objects is None:
                bin.in_bin_objects = []
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
        if self.robot_handempty and obj.is_foldable and not obj.folded:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            if bin.in_bin_objects:
                bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' and 'place' actions ensure that the robot does not handle the bin itself and only manipulates objects. The 'fold' action checks if the object is foldable before folding it. The 'push' action ensures that only soft objects are pushed, and the 'out' action allows the robot to remove objects from the bin and place them on a platform. These actions and their preconditions and effects are designed to maintain the integrity of the bin-packing task and ensure that the robot operates within the specified constraints.

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
    is_soft=False, 
    is_foldable=True, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_soft=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_soft=True, 
    is_foldable=False, 
    init_pose='in_box', 
    in_box=True
)

white_box = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_foldable=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not folded
    # object1: out_box
    # object2: in_box, not pushed
    # white_box: empty

    # Goal State:
    # object0: in_box, folded
    # object1: out_box
    # object2: in_box, pushed
    # white_box: contains object0 and object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Out object2 (black_2D_ring) from the box because it is rigid and in the box initially.
    # 2. Fold object0 (yellow_2D_rectangle) because it is foldable.
    # 3. Place object0 (yellow_2D_rectangle) into the box.
    # 4. Place object2 (black_2D_ring) back into the box.
    # 5. Push object2 (black_2D_ring) because it is soft.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Step 1: Out object2 from the box
    robot.out(object2, box)

    # Step 2: Fold object0
    robot.fold(object0, box)

    # Step 3: Place object0 into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 4: Place object2 back into the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 5: Push object2
    robot.push(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Out object2 because it is rigid and in the box initially.
    # 2. Fold object0 because it is foldable.
    # 3. Place object0 into the box to achieve the goal state.
    # 4. Place object2 back into the box to achieve the goal state.
    # 5. Push object2 because it is soft and to make more space in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object2.pushed == True
    assert white_box.in_bin_objects == [object0, object2]
    print("All task planning is done")
