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
    is_packed: bool
    
    # Object physical properties 
    is_elastic: bool
    is_rigid: bool
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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid:
                if any(o.is_elastic for o in bin.in_bin_objects):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin_objects.append(obj)
                    obj.in_box = True
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} in {bin.name} - no elastic object in bin")
            elif obj.is_elastic:
                if any(o.color == 'blue' for o in bin.in_bin_objects):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin_objects.append(obj)
                    obj.in_box = True
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} in {bin.name} - no blue object in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=True, 
    is_rigid=False, 
    is_foldable=False
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
    in_box=False, 
    is_packed=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_foldable=False
)

object2 = Object(
    index=2, 
    name='blue_linear', 
    color='blue', 
    shape='linear', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=True, 
    is_rigid=False, 
    is_foldable=False
)

object3 = Object(
    index=3, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_packed=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_foldable=True
)

white_box = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not packed
    # object1: out_box, not packed
    # object2: out_box, not packed
    # object3: in_box, not packed
    # white_box: empty

    # Final state:
    # object0: in_bin, packed
    # object1: in_bin, packed
    # object2: in_bin, packed
    # object3: in_bin, packed
    # white_box: contains all objects

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Never attempt to pick up and set down an object named box.
    # 2. When placing a rigid object in the bin, an elastic object must be in the bin before.
    # 3. When placing an elastic object, a blue object must be in the bin before.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Step 1: Place the blue elastic object (object2) in the bin first
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 2: Place the transparent elastic object (object0) in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Place the rigid object (object1) in the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Push the yellow foldable object (object3) in the bin
    robot.push(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed object2 first because it is blue and elastic, satisfying the condition for placing other elastic objects.
    # - Placed object0 next because it is elastic and there is already a blue object in the bin.
    # - Placed object1 next because it is rigid and there is already an elastic object in the bin.
    # - Pushed object3 because it was already in the bin and needed to be packed.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert white_box.in_bin_objects == [object2, object0, object1, object3]
    print("All task planning is done")
