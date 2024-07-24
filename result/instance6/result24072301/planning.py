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
    is_foldable: bool
    is_elastic: bool
    is_soft: bool


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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.is_in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, if object is rigid, soft objects must be in the bin
        if self.robot_now_holding == obj:
            if not obj.is_soft:
                if any(o.is_soft for o in bin.in_bin_objects):
                    print(f"Place {obj.name in bin.name}")
                    bin.in_bin_objects.append(obj)
                    obj.is_in_box = True
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} in bin, no soft objects in bin")
            else:
                print(f"Place {obj.name} in bin.name")
                bin.in_bin_objects.append(obj)
                obj.is_in_box = True
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}, not holding the object")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be in the bin
        if self.robot_handempty and obj.is_in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable and not in the bin
        if self.robot_handempty and obj.is_foldable and not obj.is_in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.is_in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.is_in_box = False
            self.state_handempty()
        else:
            print(f"Cannot out {obj.name}, not in the bin")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_in_box=False, 
    is_foldable=True, 
    is_elastic=False, 
    is_soft=False
)

object1 = Object(
    index=1, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_in_box=False, 
    is_foldable=False, 
    is_elastic=True, 
    is_soft=False
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
    is_in_box=True, 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=True
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
    is_in_box=False, 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not folded
    # object1: out_box
    # object2: in_box
    # object3: box, contains object2

    # Goal State:
    # object0: in_bin, folded
    # object1: in_bin
    # object2: in_bin
    # object3: box, contains object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object0) on the platform
    # 2. Pick and place the yellow_2D_rectangle (object0) in the box
    # 3. Pick and place the transparent_3D_cylinder (object1) in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Step 1: Fold the yellow_2D_rectangle (object0) on the platform
    robot.fold(object0, box)
    assert object0.folded == True

    # Step 2: Pick and place the yellow_2D_rectangle (object0) in the box
    robot.pick(object0, box)
    assert robot.robot_now_holding == object0
    robot.place(object0, box)
    assert object0.is_in_box == True

    # Step 3: Pick and place the transparent_3D_cylinder (object1) in the box
    robot.pick(object1, box)
    assert robot.robot_now_holding == object1
    robot.place(object1, box)
    assert object1.is_in_box == True

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: It is prohibited to lift and relocate a container - Not violated
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before - Followed
    # Rule 4: If there is a foldable object, fold the object on the platform not in the bin - Followed

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
