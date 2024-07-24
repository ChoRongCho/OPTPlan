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
    
    # Object physical properties 
    is_rigid: bool
    is_fragile: bool
    
    # Additional predicates for bin_packing
    in_box: bool
    is_heavy: bool


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
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid:
                if all(o.is_soft for o in bin.in_bin_objects):
                    bin.in_bin_objects.append(obj)
                    obj.in_box = True
                    self.state_handempty()
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} due to rigid object rule")
            elif obj.is_fragile:
                if any(o.is_elastic for o in bin.in_bin_objects):
                    bin.in_bin_objects.append(obj)
                    obj.in_box = True
                    self.state_handempty()
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} due to fragile object rule")
            else:
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
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
    in_box=False, 
    is_heavy=False
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
    in_box=False, 
    is_heavy=False
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
    in_box=True, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0 (black_3D_cylinder): out_box
    # object1 (green_3D_cylinder): out_box
    # object2 (white_box): in_box, empty

    # Goal State:
    # object0 (black_3D_cylinder): out_box
    # object1 (green_3D_cylinder): in_box
    # object2 (white_box): in_box, contains object1

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: When placing rigid objects in the bin, the soft objects must be in the bin before
    # Rule 3: When placing fragile objects, the elastic objects must be in the bin
    # Rule 4: When a soft object is in the bin at the initial state, out of the soft object and replace it into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Make an action sequence
    # Since there are no soft or elastic objects in the initial state, we can directly place the fragile object in the box

    # Pick the green_3D_cylinder (fragile object)
    robot.pick(object1, box)

    # Place the green_3D_cylinder in the white_box
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Not applicable as we are not picking or setting down the box
    # Rule 2: Not applicable as there are no soft objects
    # Rule 3: Not applicable as there are no elastic objects
    # Rule 4: Not applicable as there are no soft objects in the initial state

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == False
    assert object1.in_box == True
    assert object2.in_box == True
    assert object1 in object2.in_bin_objects
    print("All task planning is done")
