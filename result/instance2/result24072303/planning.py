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
    is_elastic: bool
    
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
        # Preconditions
        if self.robot_handempty and obj.object_type != 'box' and obj not in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj and obj.object_type != 'box':
            # Effects
            self.state_handempty()
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj in bin.in_bin_objects:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj in bin.in_bin_objects and obj.is_elastic:
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
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, init_pose='out_box')
object1 = Object(index=1, name='blue_2D_ring', color='blue', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, init_pose='out_box')
object2 = Object(index=2, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, init_pose='in_box')
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, init_pose='box')

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.init_pose,
        object1.name: object1.init_pose,
        object2.name: object2.init_pose,
        object3.name: object3.init_pose,
    }
    
    # Goal state
    goal_state = {
        object0.name: 'in_box',
        object1.name: 'in_box',
        object2.name: 'in_box',
        object3.name: 'box',
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # We need to place object0, object1, and object2 into object3 (the box)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Make the action sequence
    # Pick and place black_3D_cylinder into the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place blue_2D_ring into the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # white_2D_ring is already in the box, no need to pick and place
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # We have placed all objects into the box as per the goal state
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    assert object2 in box.in_bin_objects
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
