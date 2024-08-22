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
    is_elastic: bool
    is_soft: bool
    is_rigid: bool
    is_foldable: bool
    is_fragile: bool
    
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
        # Preconditions: Object is out of the box and robot hand is empty
        if obj.out_box and self.robot_handempty:
            # Effects: Robot is holding the object, object is no longer out of the box
            self.state_holding(obj)
            obj.out_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Effects: Object is in the box, robot hand is empty
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Object is soft and robot hand is empty
        if obj.is_soft and self.robot_handempty:
            # Effects: Object is pushed
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Object is foldable and robot hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Effects: Object is folded
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object is in the box
        if obj.in_box:
            # Effects: Object is out of the box, robot is holding the object
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False,
    is_foldable=False, is_fragile=False, in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False,
    is_foldable=False, is_fragile=False, in_box=False, out_box=True
)

object2 = Object(
    index=2, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True,
    is_foldable=False, is_fragile=False, in_box=True, out_box=False
)

object3 = Object(
    index=3, name='red_3D_cylinder', color='red', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False,
    is_foldable=True, is_fragile=True, in_box=True, out_box=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], is_elastic=False, is_soft=False,
    is_rigid=False, is_foldable=False, is_fragile=False, in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: in_box
    # object3: in_box
    # white_box: contains object2, object3

    # Goal State:
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: in_box
    # white_box: contains object0, object1, object2, object3

    # Second, using given rules and object's states, make a task planning strategy
    # - Place soft objects before rigid or fragile objects
    # - Fold objects if they are foldable
    # - Push soft objects after placing items in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box

    # Action sequence:
    # 1. Pick and place the soft object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)

    # 2. Pick and place the non-soft object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)

    # 3. Ensure the foldable object (object3) is folded
    robot.fold(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - object0 is soft, so it is placed first
    # - object1 is not soft, so it is placed after the soft object
    # - object3 is foldable, so it is folded

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object0.out_box == False
    assert object1.out_box == False
    assert object2.out_box == False
    assert object3.out_box == False
    assert object3.folded == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3}

    print("All task planning is done")
