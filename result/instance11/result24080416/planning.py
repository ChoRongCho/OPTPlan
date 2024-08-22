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
    is_foldable: bool
    is_elastic: bool
    is_rigid: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        if obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            if obj.is_soft or all(o.is_soft for o in bin.in_bin_objects):
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
            else:
                print(f"Cannot place {obj.name} before placing soft objects")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, is_soft=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_rigid=False, is_soft=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, is_soft=True,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='yellow_3D_polyhedron', color='yellow', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=True, is_rigid=False, is_soft=False,
    in_box=True, out_box=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], is_foldable=False, is_elastic=False, is_rigid=False, is_soft=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True
    # white_box: in_bin_objects=[object2, object3]

    # Goal state:
    # object0: in_box=True, out_box=False
    # object1: in_box=True, out_box=False
    # object2: in_box=True, out_box=False
    # object3: in_box=True, out_box=False
    # white_box: in_bin_objects=[object0, object1, object2, object3]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the white_3D_cylinder (soft object) into the white_box.
    # 2. Pick and place the black_3D_cylinder (rigid object) into the white_box.
    # 3. Ensure all objects are in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box

    # Action sequence:
    # 1. Pick white_3D_cylinder
    robot.pick(object1, box)
    # 2. Place white_3D_cylinder in white_box
    robot.place(object1, box)
    # 3. Pick black_3D_cylinder
    robot.pick(object0, box)
    # 4. Place black_3D_cylinder in white_box
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The white_3D_cylinder is a soft object and should be placed in the box before any rigid objects.
    # - The black_3D_cylinder is a rigid object and can be placed after the soft object is in the box.
    # - The red_3D_polyhedron and yellow_3D_polyhedron are already in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object0.out_box == False
    assert object1.out_box == False
    assert object2.out_box == False
    assert object3.out_box == False
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    assert object2 in box.in_bin_objects
    assert object3 in box.in_bin_objects

    print("All task planning is done")
