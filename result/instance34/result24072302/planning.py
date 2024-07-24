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
    is_out_box: bool
    
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
        if self.robot_handempty and obj.is_out_box and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if not self.robot_handempty and self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid and any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} due to rule 3")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.is_in_box = True
                obj.is_out_box = False
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_in_box:
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
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_rigid=False, is_fragile=False, is_soft=True, is_elastic=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_rigid=True, is_fragile=False, is_soft=False, is_elastic=False
)

object2 = Object(
    index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_out_box=False,
    is_rigid=False, is_fragile=True, is_soft=False, is_elastic=True
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_out_box=False,
    is_rigid=False, is_fragile=False, is_soft=False, is_elastic=True
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], is_in_box=True, is_out_box=False,
    is_rigid=False, is_fragile=False, is_soft=False, is_elastic=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: red_3D_polyhedron, is_out_box=True, is_in_box=False
    # object1: yellow_3D_cylinder, is_out_box=True, is_in_box=False
    # object2: black_2D_ring, is_out_box=False, is_in_box=True
    # object3: white_2D_ring, is_out_box=False, is_in_box=True
    # white_box: contains object2 and object3

    # Goal State
    # object0: red_3D_polyhedron, is_out_box=False, is_in_box=True
    # object1: yellow_3D_cylinder, is_out_box=False, is_in_box=True
    # object2: black_2D_ring, is_out_box=False, is_in_box=True
    # object3: white_2D_ring, is_out_box=True, is_in_box=False
    # white_box: contains object0, object1, and object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Out white_2D_ring (object3) from white_box
    # 2. Pick red_3D_polyhedron (object0) and place it in white_box
    # 3. Pick yellow_3D_cylinder (object1) and place it in white_box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Perform the actions
    robot.out(object3, box)  # Out white_2D_ring from white_box
    robot.pick(object0, box)  # Pick red_3D_polyhedron
    robot.place(object0, box)  # Place red_3D_polyhedron in white_box
    robot.pick(object1, box)  # Pick yellow_3D_cylinder
    robot.place(object1, box)  # Place yellow_3D_cylinder in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Don't pick and place a box called bin - Followed
    # Rule 2: When fold a object, the object must be foldable - Not applicable
    # Rule 3: When place a rigid objects in the bin, the soft objects must be in the bin before - Followed

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == False
    assert object3.is_out_box == True
    assert object4.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
