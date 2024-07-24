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
    is_soft: bool
    is_elastic: bool
    
    # Object physical properties
    init_pose: str
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
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.is_fragile:
            if any(o.is_soft for o in bin.in_bin_objects):
                print(f"Place {obj.name in bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
            else:
                print(f"Cannot Place {obj.name} because no soft objects in bin")
        elif self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            obj.in_box = True
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft:
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
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_soft=True, is_elastic=False,
    init_pose='out_box', in_box=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, is_soft=False, is_elastic=False,
    init_pose='out_box', in_box=False
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, is_soft=False, is_elastic=False,
    init_pose='out_box', in_box=False
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_soft=False, is_elastic=True,
    init_pose='in_box', in_box=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_soft=False, is_elastic=False,
    init_pose='box', in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given objects

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the red_3D_polyhedron (soft object) in the box.
    # 2. Pick and place the yellow_3D_cylinder (rigid object) in the box.
    # 3. Pick and place the green_3D_cylinder (fragile object) in the box.
    # 4. The white_2D_ring is already in the box.
    # 5. Avoid handling and moving the white_box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Step 1: Pick and place the red_3D_polyhedron
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 2: Pick and place the yellow_3D_cylinder
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 3: Pick and place the green_3D_cylinder
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The red_3D_polyhedron is soft, so it can be placed in the box without any issues.
    # 2. The yellow_3D_cylinder is rigid, so it can be placed in the box without any issues.
    # 3. The green_3D_cylinder is fragile, but since the red_3D_polyhedron (soft object) is already in the box, it can be placed in the box.
    # 4. The white_2D_ring is already in the box, so no action is needed.
    # 5. The white_box should not be handled or moved as per the rules.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == False
    print("All task planning is done")
