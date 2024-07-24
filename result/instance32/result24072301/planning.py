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
    is_elastic: bool
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
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic and obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, is_elastic=False, in_box=False)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, is_elastic=False, in_box=False)
object2 = Object(index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=True, is_elastic=True, in_box=False)
object3 = Object(index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_elastic=True, in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[object3], is_rigid=False, is_fragile=False, is_elastic=False, in_box=True)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_bin_objects
    }
    
    # Goal State
    goal_state = {
        object0.name: True,
        object1.name: False,
        object2.name: True,
        object3.name: True,
        object4.name: [object0, object2, object3]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4
    
    # Action sequence to achieve the goal state
    # 1. Pick green_3D_cylinder and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 2. Pick blue_1D_linear and place it in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # 3. Fold blue_1D_linear (since it is elastic and fragile, it must be in the box)
    robot.fold(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - green_3D_cylinder is not in the box initially, so we pick and place it in the box.
    # - blue_1D_linear is not in the box initially, so we pick and place it in the box.
    # - blue_1D_linear is elastic and fragile, so we fold it after placing it in the box.
    # - white_2D_ring is already in the box, so no action is needed for it.
    # - yellow_3D_cylinder should remain outside the box, so no action is needed for it.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object3, object0, object2]
    print("All task planning is done")
