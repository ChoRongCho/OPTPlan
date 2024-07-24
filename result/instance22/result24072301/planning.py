from dataclasses import dataclass, field
from typing import List

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: List[int] = field(default_factory=list)
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_rigid: bool = False
    in_box: bool = False

    # Object physical properties
    init_pose: str = 'out_box'


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
        # Preconditions
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj.object_type != 'box':
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj.index)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.object_type != 'box':
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.object_type != 'box':
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj.index in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj.index)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', init_pose='out_box', is_rigid=True, in_box=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', init_pose='out_box', is_rigid=True, in_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', init_pose='box', is_rigid=False, in_box=True)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        object0.name: object0.init_pose,
        object1.name: object1.init_pose,
        object2.name: object2.init_pose
    }
    
    # Goal State
    goal_state = {
        object0.name: 'in_bin',
        object1.name: 'in_bin',
        object2.name: 'out_bin'
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: You should never pick and place a box
    # Rule 2: If there are objects in the box, pick out all objects from bin first, and do packing
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2
    
    # c) Make an action sequence
    # Since the box is initially empty, we can directly start packing objects into the box.
    
    # Pick and place yellow_3D_cylinder
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place black_3D_cylinder
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Now, we need to take the objects out of the box to achieve the goal state
    robot.out(object0, box)
    robot.out(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. We picked and placed the yellow_3D_cylinder and black_3D_cylinder into the box.
    # 2. We then took them out of the box to achieve the goal state where they are 'in_bin'.
    # 3. The white_box should remain out of the bin as per the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == False
    assert object1.in_box == False
    assert object2.in_box == False
    print("All task planning is done")
