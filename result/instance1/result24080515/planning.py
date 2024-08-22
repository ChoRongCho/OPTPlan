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
    is_rigid: bool
    is_elastic: bool
    
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
        # Preconditions: Robot hand must be empty, object must be packable and not in the bin
        if self.robot_handempty and obj.is_packable and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, object must be packable
        if self.robot_now_holding == obj and obj.is_packable:
            # Check if there are any soft objects that need to be placed first
            soft_objects = [o for o in bin.in_bin_objects if o.is_soft]
            if not soft_objects or obj.is_soft:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
            else:
                print(f"Cannot Place {obj.name} before placing soft objects")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft and in the bin
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_packable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

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
    is_soft=True, 
    is_rigid=False, 
    is_elastic=True, 
    in_box=False, 
    is_packable=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=True, 
    is_elastic=False, 
    in_box=False, 
    is_packable=True
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
    is_soft=False, 
    is_rigid=False, 
    is_elastic=False, 
    in_box=False, 
    is_packable=True
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
    is_rigid=False, 
    is_elastic=False, 
    in_box=True, 
    is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        white_box.name: white_box.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        white_box.name: [object0, object1, object2]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the rigid object (object1) next.
    # 3. Pick and place the remaining object (object2).
    # 4. Push the soft object (object0) if needed.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = white_box
    
    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    robot.push(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place the soft object (object0) first to satisfy the rule that soft objects should be placed before rigid objects.
    # 2. Pick and place the rigid object (object1) next as there are no more soft objects to place.
    # 3. Pick and place the remaining object (object2) as it is neither soft nor rigid.
    # 4. Push the soft object (object0) to ensure it is properly placed in the bin.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object0 in white_box.in_bin_objects
    assert object1 in white_box.in_bin_objects
    assert object2 in white_box.in_bin_objects
    
    print("All task planning is done")
