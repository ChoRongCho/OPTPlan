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
    is_foldable: bool
    
    # Object physical properties
    init_pose: str


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
        if self.robot_handempty and obj.object_type != 'box' and obj not in bin.in_bin_objects:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid:
                if all(o.is_rigid or o.pushed for o in bin.in_bin_objects):
                    bin.in_bin_objects.append(obj)
                    self.state_handempty()
                    print(f"Place {obj.name in bin.name}")
                else:
                    print(f"Cannot Place {obj.name} due to unpushed soft objects in bin")
            else:
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                print(f"Place {obj.name} in bin.name")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj in bin.in_bin_objects and not obj.is_rigid:
            if not any(o.is_rigid for o in bin.in_bin_objects if o != obj):
                obj.pushed = True
                print(f"Push {obj.name}")
            else:
                print(f"Cannot Push {obj.name} due to fragile objects on it")
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
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_foldable=True, 
    init_pose='out_box'
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_foldable=False, 
    init_pose='out_box'
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
    is_foldable=False, 
    init_pose='box'
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    print("Initial State:")
    print(f"{object0.name} is {object0.init_pose}")
    print(f"{object1.name} is {object1.init_pose}")
    print(f"{object2.name} is {object2.init_pose}")

    # Goal state
    print("\nGoal State:")
    print(f"{object0.name} should be in {object2.name} and pushed")
    print(f"{object1.name} should be in {object2.name}")
    print(f"{object2.name} should contain {object0.name} and {object1.name}")

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Don't pick and place a box called bin
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # 1. Pick the yellow_2D_rectangle (soft object)
    robot.pick(object0, box)
    
    # 2. Place the yellow_2D_rectangle in the white_box
    robot.place(object0, box)
    
    # 3. Push the yellow_2D_rectangle to make space
    robot.push(object0, box)
    
    # 4. Pick the yellow_3D_cylinder (rigid object)
    robot.pick(object1, box)
    
    # 5. Place the yellow_3D_cylinder in the white_box
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for each action:
    # 1. Pick the yellow_2D_rectangle because it is a soft object and needs to be placed first.
    # 2. Place the yellow_2D_rectangle in the white_box to follow the rule that soft objects must be in the bin before rigid objects.
    # 3. Push the yellow_2D_rectangle to make more space in the bin.
    # 4. Pick the yellow_3D_cylinder because it is a rigid object and can be placed after the soft object.
    # 5. Place the yellow_3D_cylinder in the white_box to complete the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    assert object0.pushed == True
    print("All task planning is done")
