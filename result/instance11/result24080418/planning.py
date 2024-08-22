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
        if obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.out_box == False:
            # Check if there are any soft objects in the bin
            soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
            if obj.is_soft or soft_objects_in_bin:
                # Effects
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot place {obj.name} before placing soft objects")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_elastic and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object2], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[object2]

    # Goal State:
    # object0: out_box=False, in_box=True
    # object1: out_box=False, in_box=True
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the white_3D_cylinder (soft object) into the box first.
    # 2. Pick and place the black_3D_cylinder (rigid object) into the box.
    # 3. Ensure the red_3D_polyhedron (soft object) is already in the box.
    # 4. Verify the final state of the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object1, box)  # Pick white_3D_cylinder
    robot.place(object1, box)  # Place white_3D_cylinder in the box

    robot.pick(object0, box)  # Pick black_3D_cylinder
    robot.place(object0, box)  # Place black_3D_cylinder in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The white_3D_cylinder is soft and should be placed first to satisfy the rule that soft objects should be in the box before rigid objects.
    # 2. The black_3D_cylinder is rigid and can be placed after the soft object is in the box.
    # 3. The red_3D_polyhedron is already in the box, so no action is needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object2, object1, object0]
    print("All task planning is done")
