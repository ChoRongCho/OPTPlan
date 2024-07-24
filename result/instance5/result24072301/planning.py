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
    is_rigid: bool
    is_soft: bool


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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.shape == '1D' and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_elastic and not obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and not obj.folded:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

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
    is_rigid=False, 
    is_soft=True
)

object1 = Object(
    index=1, 
    name='black_1D_linear', 
    color='black', 
    shape='1D_linear', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_soft=False
)

object2 = Object(
    index=2, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_heavy=False, 
    is_elastic=True, 
    is_rigid=False, 
    is_soft=False
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
    in_box=True, 
    is_heavy=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: not in box, elastic, soft
    # object1: not in box, rigid
    # object2: in box, elastic
    # object3: is a box, in box

    # Goal State
    # object0: not in box, in_bin_objects=[0]
    # object1: not in box
    # object2: not in box, in_bin_objects=[2]
    # object3: is a box, in box

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: never attempt to pick up and set down an object named box
    # Rule 2: when place a 1D object in the bin, the soft object must be in the bin before
    # Rule 3: if there is an elastic object, push the object not in the bin, but on the platform

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Fourth, after making all actions, fill your reasons according to the rules
    # Step 1: Push the elastic object (object0) on the platform
    robot.push(object0, box)

    # Step 2: Pick the soft object (object0) and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Pick the 1D object (object1) and place it in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Out the transparent_3D_cylinder (object2) from the box
    robot.out(object2, box)

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == False
    assert object3.in_box == True
    print("All task planning is done")
