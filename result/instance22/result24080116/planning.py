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
    is_rigid: bool
    init_pose: str
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_in_box: bool
    is_out_box: bool


class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if self.robot_handempty and obj.is_out_box:
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Picked {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Placed {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_in_box:
            obj.pushed = True
            print(f"Pushed {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_rigid:
            obj.folded = True
            print(f"Folded {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    init_pose='out_box', 
    is_in_box=False, 
    is_out_box=True
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
    is_rigid=True, 
    init_pose='out_box', 
    is_in_box=False, 
    is_out_box=True
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
    init_pose='box', 
    is_in_box=True, 
    is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {
            "is_in_box": False,
            "is_out_box": True
        },
        "object1": {
            "is_in_box": False,
            "is_out_box": True
        },
        "object2": {
            "is_in_box": True,
            "is_out_box": False,
            "in_bin_objects": []
        }
    }

    # Goal state
    goal_state = {
        "object0": {
            "is_in_box": True,
            "is_out_box": False
        },
        "object1": {
            "is_in_box": True,
            "is_out_box": False
        },
        "object2": {
            "is_in_box": True,
            "is_out_box": False,
            "in_bin_objects": [0, 1]
        }
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick yellow_3D_cylinder (object0) and place it in white_box (object2)
    # 2. Pick black_3D_cylinder (object1) and place it in white_box (object2)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Perform actions
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The yellow_3D_cylinder and black_3D_cylinder are rigid objects and can be placed in the box.
    # - The white_box is already in the box, so no need to place it.
    # - The rules are followed as no soft objects are involved, and no folding or pushing actions are required.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    print("All task planning is done")
