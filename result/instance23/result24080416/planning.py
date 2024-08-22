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
    is_fragile: bool
    is_rigid: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    can_be_packed: bool


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.in_box:
            print(f"Cannot pick {obj.name}, it is already in the bin.")
            return False
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name}, robot hand is not empty.")
            return False
        print(f"Pick {obj.name}")
        self.state_holding(obj)
        return True
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if not self.robot_now_holding:
            print(f"Cannot place {obj.name}, robot is not holding any object.")
            return False
        if obj.is_fragile or obj.is_rigid:
            if any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot place {obj.name}, soft objects should be placed first.")
                return False
        print(f"Place {obj.name} in {bin.name}")
        bin.in_bin_objects.append(obj)
        obj.in_box = True
        self.state_handempty()
        return True
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if not self.robot_handempty:
            print(f"Cannot push {obj.name}, robot hand is not empty.")
            return False
        if not obj.is_soft:
            print(f"Cannot push {obj.name}, only soft objects can be pushed.")
            return False
        print(f"Push {obj.name}")
        obj.pushed = True
        return True
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name}, robot hand is not empty.")
            return False
        if not obj.can_be_packed:
            print(f"Cannot fold {obj.name}, it is not foldable.")
            return False
        print(f"Fold {obj.name}")
        obj.folded = True
        return True
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj not in bin.in_bin_objects:
            print(f"Cannot out {obj.name}, it is not in the bin.")
            return False
        print(f"Out {obj.name} from {bin.name}")
        bin.in_bin_objects.remove(obj)
        obj.in_box = False
        self.state_handempty()
        return True

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=False, 
    is_soft=True, 
    in_box=False, 
    can_be_packed=False
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
    is_fragile=True, 
    is_rigid=True, 
    is_soft=False, 
    in_box=False, 
    can_be_packed=False
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
    is_fragile=False, 
    is_rigid=False, 
    is_soft=False, 
    in_box=True, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0 (red_3D_polyhedron): out_box, is_soft, not in_box
    # object1 (green_3D_cylinder): out_box, is_rigid, is_fragile, not in_box
    # object2 (white_box): in_box, empty

    # Goal State:
    # object0 (red_3D_polyhedron): in_box, is_soft
    # object1 (green_3D_cylinder): in_box, is_rigid, is_fragile
    # object2 (white_box): in_box, contains object0 and object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the rigid and fragile object (object1) after the soft object is in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object2
    
    # c) Action sequence
    # Pick and place the soft object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the rigid and fragile object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. According to the rule, soft objects should be placed first if there are any soft objects.
    # 2. After placing the soft object, we can place the rigid and fragile object.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")
