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
    is_foldable: bool
    is_soft: bool
    
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
        if obj.out_box and self.robot_handempty:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if obj.in_box and self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj in bin.in_bin_objects:
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
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=False, in_box=False, out_box=True)
object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, is_soft=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=True, in_box=False, out_box=True)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=False, in_box=False, out_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, is_soft=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code reflect the properties and initial positions of the objects as described in the input.
# The 'in_bin_objects' list is empty for all objects initially, indicating no objects are inside any bin at the start.
# The 'pushed' and 'folded' properties are set to False for all objects initially.
# The 'in_box' and 'out_box' properties are mutually exclusive and set according to the 'init_pose' provided in the input.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, is_soft=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=False, in_box=False, out_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, is_soft=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        object0: {'in_box': True, 'out_box': False},
        object1: {'in_box': True, 'out_box': False},
        object2: {'in_box': True, 'out_box': False},
        object3: {'in_box': True, 'out_box': False},
        object4: {'in_bin_objects': [object0, object1, object2, object3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place soft objects first (object1 and object2)
    # 2. Pick and place remaining objects (object0 and object3)
    # 3. Push soft objects if necessary (not needed in this case)
    # 4. Fold foldable objects if necessary (not needed in this case)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place soft objects first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Pick and place remaining objects after soft objects are placed.
    # 3. No need to push or fold any objects as per the goal state requirements.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object0.out_box == False
    assert object1.out_box == False
    assert object2.out_box == False
    assert object3.out_box == False
    assert object4.in_bin_objects == [object0, object1, object2, object3]

    print("All task planning is done")
