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
    is_elastic: bool
    
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
        if self.robot_handempty and not obj.in_box:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.can_be_packed:
            if obj.is_elastic or all(o.is_elastic for o in bin.in_bin_objects):
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name in bin.name}")
            else:
                print(f"Cannot Place {obj.name} in {bin.name} due to preconditions")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_elastic and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj in bin.in_bin_objects:
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
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    in_box=False, 
    can_be_packed=True
)

object1 = Object(
    index=1, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=True, 
    in_box=False, 
    can_be_packed=True
)

object2 = Object(
    index=2, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    in_box=False, 
    can_be_packed=True
)

object3 = Object(
    index=3, 
    name='green_2D_circle', 
    color='green', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=True, 
    in_box=True, 
    can_be_packed=True
)

white_box = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object3], 
    is_rigid=False, 
    is_elastic=False, 
    in_box=True, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: yellow_3D_cylinder, in_box=False
    # object1: white_2D_ring, in_box=False
    # object2: blue_2D_ring, in_box=False
    # object3: green_2D_circle, in_box=True
    # white_box: in_bin_objects=[object3]

    # Goal State:
    # object0: yellow_3D_cylinder, in_box=True
    # object1: white_2D_ring, in_box=True
    # object2: blue_2D_ring, in_box=True
    # object3: green_2D_circle, in_box=True
    # white_box: in_bin_objects=[object0, object1, object2, object3]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the white_2D_ring (soft object) first.
    # 2. Pick and place the blue_2D_ring (rigid object).
    # 3. Pick and place the yellow_3D_cylinder (rigid object).
    # 4. Push the white_2D_ring (soft object) to ensure it is properly placed.
    # 5. Ensure the green_2D_circle is already in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    robot.pick(object1, box)  # Pick white_2D_ring
    robot.place(object1, box)  # Place white_2D_ring in white_box

    robot.pick(object2, box)  # Pick blue_2D_ring
    robot.place(object2, box)  # Place blue_2D_ring in white_box

    robot.pick(object0, box)  # Pick yellow_3D_cylinder
    robot.place(object0, box)  # Place yellow_3D_cylinder in white_box

    robot.push(object1, box)  # Push white_2D_ring

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (white_2D_ring) first as per the rule.
    # 2. Placed the rigid objects (blue_2D_ring and yellow_3D_cylinder) after the soft object.
    # 3. Pushed the soft object (white_2D_ring) to ensure it is properly placed in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3}

    print("All task planning is done")
