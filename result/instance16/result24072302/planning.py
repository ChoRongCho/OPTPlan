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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_elastic or any(o.is_elastic for o in bin.in_bin_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name in bin.name}")
            else:
                print(f"Cannot Place {obj.name} due to rule constraints")
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
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
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
    name='beige_2D_ring', 
    color='beige', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_box=False
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
    is_elastic=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=True, 
    init_pose='in_box', 
    in_box=True
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
    is_elastic=False, 
    is_foldable=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        "object0": {"name": "beige_2D_ring", "init_pose": "out_box", "in_box": False, "pushed": False, "folded": False, "is_elastic": True, "is_foldable": False},
        "object1": {"name": "transparent_3D_cylinder", "init_pose": "out_box", "in_box": False, "pushed": False, "folded": False, "is_elastic": True, "is_foldable": False},
        "object2": {"name": "white_2D_circle", "init_pose": "in_box", "in_box": True, "pushed": False, "folded": False, "is_elastic": False, "is_foldable": True},
        "object3": {"name": "white_box", "init_pose": "box", "in_box": False, "pushed": False, "folded": False, "is_elastic": False, "is_foldable": False, "in_bin_objects": []}
    }

    # Goal State
    goal_state = {
        "object0": {"name": "beige_2D_ring", "goal_pose": "in_bin", "in_box": False, "pushed": False, "folded": False, "is_elastic": True, "is_foldable": False},
        "object1": {"name": "transparent_3D_cylinder", "goal_pose": "in_bin", "in_box": False, "pushed": False, "folded": False, "is_elastic": True, "is_foldable": False},
        "object2": {"name": "white_2D_circle", "goal_pose": "in_bin", "in_box": True, "pushed": False, "folded": False, "is_elastic": False, "is_foldable": True},
        "object3": {"name": "white_box", "goal_pose": "box", "in_box": False, "pushed": False, "folded": False, "is_elastic": False, "is_foldable": False, "in_bin_objects": [0, 1, 2]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. It is prohibited to lift and relocate a container.
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before.
    # 3. When placing a fragile object, the soft objects must be in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Step 1: Pick beige_2D_ring and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 2: Pick transparent_3D_cylinder and place it in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 3: Push white_2D_circle (already in the box)
    robot.push(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - beige_2D_ring and transparent_3D_cylinder are elastic, so they can be placed in the box without any constraints.
    # - white_2D_circle is already in the box and is foldable, so it can be pushed to make space for other objects.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
