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
    is_soft: bool
    is_foldable: bool
    is_fragile: bool
    is_elastic: bool
    
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
                print(f"Cannot place {obj.name} before placing all soft objects")
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
        if obj.in_box and self.robot_handempty:
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
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_foldable=False, 
    is_fragile=False, is_elastic=True, in_box=False, out_box=True
)

object1 = Object(
    index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=True, 
    is_fragile=False, is_elastic=False, in_box=False, out_box=True
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=True, 
    is_fragile=True, is_elastic=False, in_box=False, out_box=True
)

object3 = Object(
    index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_foldable=False, 
    is_fragile=False, is_elastic=False, in_box=True, out_box=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3], is_soft=False, is_foldable=False, 
    is_fragile=False, is_elastic=False, in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: out_box
    # object3: in_box
    # white_box: contains object3

    # Goal State:
    # object0: in_box
    # object1: in_box and folded
    # object2: in_box and folded
    # object3: in_box
    # white_box: contains object0, object1, object2, object3

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place all soft objects first
    # 2. Fold foldable objects
    # 3. Place foldable objects
    # 4. Place fragile objects last

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = white_box
    
    # Action sequence
    # 1. Pick and place the soft object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 2. Fold the foldable objects (object1 and object2)
    robot.fold(object1, box)
    robot.fold(object2, box)
    
    # 3. Pick and place the folded object1
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 4. Pick and place the folded object2
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # - Placed soft object first (object0)
    # - Folded foldable objects (object1 and object2)
    # - Placed folded objects (object1 and object2)
    # - Ensured all objects are in the box as per the goal state

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object1.folded == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_box == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3}
    
    print("All task planning is done")
