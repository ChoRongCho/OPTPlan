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
    is_rigid: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.is_elastic:
            # Effects
            obj.in_box = True
            obj.is_packed = True
            self.state_handempty()
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_elastic and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            obj.in_box = False
            obj.is_packed = False
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
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
    is_foldable=False, 
    is_rigid=True, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

object1 = Object(
    index=1, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=True, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='brown_2D_rectangle', 
    color='brown', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=True, 
    is_rigid=False, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

object3 = Object(
    index=3, 
    name='black_3D_cuboid', 
    color='black', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_rigid=False, 
    is_elastic=True, 
    in_box=False, 
    is_packed=False
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
    is_rigid=False, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not packed
    # object1: out_box, not packed
    # object2: out_box, not packed
    # object3: out_box, not packed
    # object4: box, empty

    # Final state:
    # object0: in_box, packed
    # object1: in_box, packed
    # object2: in_box, folded, packed
    # object3: in_box, pushed, packed
    # object4: box, contains [object0, object1, object2, object3]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the foldable object (object2)
    # 2. Place the elastic object (object3) in the box
    # 3. Place the rigid objects (object0, object1) in the box
    # 4. Push the elastic object (object3) in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.fold(object2, box)  # Fold the foldable object
    robot.pick(object3, box)  # Pick the elastic object
    robot.place(object3, box)  # Place the elastic object in the box
    robot.pick(object0, box)  # Pick the first rigid object
    robot.place(object0, box)  # Place the first rigid object in the box
    robot.pick(object1, box)  # Pick the second rigid object
    robot.place(object1, box)  # Place the second rigid object in the box
    robot.push(object3, box)  # Push the elastic object in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold object2 because it is foldable.
    # 2. Place object3 first because it is elastic and should be placed before rigid objects.
    # 3. Place object0 and object1 after object3 because they are rigid.
    # 4. Push object3 after placing all items in the bin because it is elastic.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_box == True
    assert object3.pushed == True
    assert object4.in_bin_objects == [object3, object0, object1, object2]
    print("All task planning is done")
