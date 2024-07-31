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
    is_fragile: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        if self.robot_handempty and obj.out_box:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if not self.robot_handempty and obj.in_box:
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True,
    is_soft=False, is_fragile=False, in_box=False, out_box=True
)

object1 = Object(
    index=1, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False,
    is_soft=False, is_fragile=False, in_box=False, out_box=True
)

object2 = Object(
    index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_rigid=False,
    is_soft=False, is_fragile=False, in_box=True, out_box=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False,
    is_soft=False, is_fragile=False, in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[]

    # Goal state:
    # object0: out_box=False, in_box=True
    # object1: out_box=False, in_box=True, folded=True
    # object2: out_box=False, in_box=True, folded=True
    # object3: out_box=False, in_box=True, in_bin_objects=[object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold object1 and object2 since they are foldable.
    # 2. Pick and place object0, object1, and object2 into the box.
    # 3. Ensure the order of placing objects follows the rule for fragile and rigid objects.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Fold object1 and object2
    robot.fold(object1, box)
    robot.fold(object2, box)

    # Pick and place object0 into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place object1 into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Pick and place object2 into the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold object1 and object2 because they are foldable.
    # 2. Pick and place object0, object1, and object2 into the box to achieve the goal state.
    # 3. Ensure the order of placing objects follows the rule for fragile and rigid objects.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object1.folded == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    assert object2 in box.in_bin_objects

    print("All task planning is done")
