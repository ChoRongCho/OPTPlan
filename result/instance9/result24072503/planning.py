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
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
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
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_fragile or obj.is_rigid:
                if any(o.is_soft for o in bin.in_bin_objects):
                    self.state_handempty()
                    obj.in_box = True
                    obj.out_box = False
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} without soft object")
            else:
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
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
        if obj.in_box and self.robot_handempty:
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
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_rigid=False, 
    is_soft=True, 
    is_fragile=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_soft=False, 
    is_fragile=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=True, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False, 
    is_fragile=False, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='green_2D_rectangle', 
    color='green', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=True, 
    is_rigid=True, 
    is_soft=False, 
    is_fragile=False, 
    in_box=True, 
    out_box=False
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False, 
    is_fragile=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: in_box
    # object3: in_box
    # object4: box
    
    # Goal State:
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: in_box
    # object4: box
    
    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold yellow_2D_rectangle (object2) if not already folded.
    # 2. Pick white_3D_cylinder (object0) and place it in the box.
    # 3. Pick green_3D_cylinder (object1) and place it in the box.
    # 4. Push white_3D_cylinder (object0) to make space for rigid objects.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # c) Action sequence
    # Fold yellow_2D_rectangle (object2)
    robot.fold(object2, box)
    
    # Pick white_3D_cylinder (object0) and place it in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick green_3D_cylinder (object1) and place it in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Push white_3D_cylinder (object0) to make space for rigid objects
    robot.push(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold yellow_2D_rectangle (object2) because it is foldable.
    # 2. Pick white_3D_cylinder (object0) and place it in the box because it is soft and can be placed without any conditions.
    # 3. Pick green_3D_cylinder (object1) and place it in the box because there is already a soft object (object0) in the box.
    # 4. Push white_3D_cylinder (object0) to make space for rigid objects as per the rules.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    # Don't include a box in the goal state. Only express objects.
    
    print("All task planning is done")
