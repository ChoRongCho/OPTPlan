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
    is_elastic: bool
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
            if obj.is_soft and not any(o.is_elastic for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because no elastic object in bin")
                return
            if not obj.is_soft and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because no soft object in bin")
                return
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
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. The preconditions ensure that the robot only performs actions when it is in the correct state and the objects meet the necessary criteria. For example, the robot cannot pick an object if it is already holding something, and it cannot place a soft object in the bin unless an elastic object is already there. These rules help to ensure that the bin packing process is efficient and avoids potential issues, such as damaging objects or overloading the bin. The effects of each action update the state of the robot and the objects, ensuring that the system accurately reflects the current situation after each action is performed.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_elastic=True, 
    is_soft=True, 
    is_foldable=False
)

object1 = Object(
    index=1, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_heavy=False, 
    is_elastic=True, 
    is_soft=False, 
    is_foldable=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object1], 
    in_box=True, 
    is_heavy=False, 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: in_box
    # object2: box (contains object1)
    
    # Goal State:
    # object0: in_bin
    # object1: out_box
    # object2: box (contains object1)
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Avoid handling and moving any box
    # Rule 2: When placing a soft object, the elastic object must be in the bin
    # Rule 3: When placing a rigid object, the soft objects must be in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, out of the rigid object first
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2
    
    # c) Action sequence
    # Step 1: Out the rigid object (object1) from the box
    robot.out(object1, box)
    
    # Step 2: Pick the soft object (object0)
    robot.pick(object0, box)
    
    # Step 3: Place the soft object (object0) in the box
    robot.place(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: According to Rule 4, we need to out the rigid object (object1) first.
    # Reason for Step 2: We need to pick the soft object (object0) to place it in the box.
    # Reason for Step 3: According to Rule 2, we can place the soft object (object0) because the elastic object (object0 itself) is in the bin.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    print("All task planning is done")
