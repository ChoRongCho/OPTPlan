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
    is_rigid: bool
    is_fragile: bool
    
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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid:
                if all(o.is_rigid or o.is_fragile for o in bin.in_bin_objects):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin_objects.append(obj)
                    self.state_handempty()
                    obj.in_box = True
            elif obj.is_fragile:
                if any(o.is_rigid for o in bin.in_bin_objects):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin_objects.append(obj)
                    self.state_handempty()
                    obj.in_box = True
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=False, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=True, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_fragile=False, 
    init_pose='box', 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in box
    # object1: out_box, not in box
    # object2: in box

    # Goal State:
    # object0: out_box, not in box
    # object1: in box
    # object2: in box

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: When placing a fragile object, the elastic objects must be in the bin
    # Rule 4: When a soft object is in the bin at the initial state, out of the soft object and replace it into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # Fourth, after making all actions, fill your reasons according to the rules
    # Step 1: Out the white_box (soft object) and replace it into the bin
    robot.out(box, box)
    robot.place(box, box)

    # Step 2: Pick the green_3D_cylinder (rigid and fragile) and place it in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == False
    assert object1.in_box == True
    assert object2.in_box == True
    print("All task planning is done")
