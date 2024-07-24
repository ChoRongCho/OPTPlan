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
    is_in_box: bool
    is_heavy: bool
    
    # Object physical properties 
    is_rigid: bool
    is_fragile: bool
    is_soft: bool
    is_elastic: bool


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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.is_in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and not obj.is_rigid and not obj.is_fragile:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.is_in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.is_in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot only picks objects that are not in the bin and are not boxes. The 'place' action ensures the robot places objects it is holding into the bin. The 'push' action is restricted to soft objects that are neither rigid nor fragile, adhering to the rule that only soft objects can be pushed. The 'fold' action is restricted to objects that are foldable (elastic). The 'out' action allows the robot to remove objects from the bin and place them on a platform, ensuring the robot's hand is empty afterward. These actions ensure safe and efficient bin packing while adhering to the specified constraints

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_heavy=False,
    is_rigid=False, is_fragile=False, is_soft=True, is_elastic=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_heavy=False,
    is_rigid=True, is_fragile=False, is_soft=False, is_elastic=False
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_heavy=False,
    is_rigid=True, is_fragile=True, is_soft=False, is_elastic=False
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_heavy=False,
    is_rigid=False, is_fragile=False, is_soft=False, is_elastic=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_heavy=False,
    is_rigid=False, is_fragile=False, is_soft=False, is_elastic=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.is_in_box,
        object1.name: object1.is_in_box,
        object2.name: object2.is_in_box,
        object3.name: object3.is_in_box,
        object4.name: object4.is_in_box,
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: False,
        object4.name: True,
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4
    
    # c) Action sequence
    # 1. Pick red_3D_polyhedron and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 2. Pick yellow_3D_cylinder and place it in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 3. Pick green_3D_cylinder and place it in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # 4. Out white_2D_ring from the box
    robot.out(object3, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The robot picks and places objects that are not in the box initially.
    # 2. The robot avoids handling the box directly.
    # 3. The robot ensures that soft objects are in the bin before placing fragile objects.
    # 4. The robot does not push or fold any objects as it is not required by the goal state.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == False
    assert object4.is_in_box == True
    print("All task planning is done")
