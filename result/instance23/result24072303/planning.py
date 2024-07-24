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
    is_in_box: bool = False
    is_out_box: bool = True
    
    # Object physical properties 
    is_rigid: bool = False
    is_elastic: bool = False
    is_soft: bool = False


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.is_out_box and self.robot_handempty and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid:
                if any(o.is_soft for o in bin.in_bin_objects):
                    print(f"Place {obj.name in bin.name}")
                    bin.in_bin_objects.append(obj)
                    self.state_handempty()
                    obj.is_in_box = True
                    obj.is_out_box = False
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} because no soft objects in bin")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.is_in_box = True
                obj.is_out_box = False
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.is_in_box:
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
        if obj.is_in_box and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_rigid=False, is_elastic=False, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', is_soft=False, is_rigid=True, is_elastic=False, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_rigid=False, is_elastic=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[2], is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    # object0: out_box, is_soft=True, is_rigid=False, is_elastic=False
    # object1: out_box, is_soft=False, is_rigid=True, is_elastic=False
    # object2: in_box, is_soft=True, is_rigid=False, is_elastic=True
    # object3: box, in_bin_objects=[2]

    # Goal state
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: box, in_bin_objects=[0, 1, 2]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place object0 (red_3D_polyhedron) into the box
    # 2. Pick and place object1 (green_2D_circle) into the box
    # 3. Push object0 (red_3D_polyhedron) to ensure it fits well
    # 4. Fold object2 (yellow_3D_cuboid) to ensure it fits well

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Pick and place object0 (red_3D_polyhedron) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place object1 (green_2D_circle) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Push object0 (red_3D_polyhedron) to ensure it fits well
    robot.push(object0, box)

    # Fold object2 (yellow_3D_cuboid) to ensure it fits well
    robot.fold(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. object0 is soft, so it can be placed in the box without any issues.
    # 2. object1 is rigid, but since object0 (a soft object) is already in the box, it can be placed.
    # 3. object0 is soft, so it can be pushed to ensure it fits well.
    # 4. object2 is elastic, so it can be folded to ensure it fits well.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.in_bin_objects == [2, 0, 1]
    print("All task planning is done")
