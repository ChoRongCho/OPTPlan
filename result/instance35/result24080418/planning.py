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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, soft objects should be in the box if any
        if self.robot_now_holding == obj and all(o.is_soft and o.in_box for o in bin.in_bin_objects if o.is_soft):
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft, object must be in the bin
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, in_box=False, is_packed=False)
object1 = Object(index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=True, in_box=False, is_packed=False)
object2 = Object(index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, in_box=True, is_packed=False)
object3 = Object(index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, in_box=True, is_packed=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[object2, object3], is_elastic=False, is_soft=False, in_box=False, is_packed=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not pushed, not folded, not in box, not packed
    # object1: out_box, not pushed, not folded, not in box, not packed
    # object2: in_box, not pushed, not folded, in box, not packed
    # object3: in_box, not pushed, not folded, in box, not packed
    # object4: box, not pushed, not folded, contains [object2, object3], not packed

    # Goal state:
    # object0: in_box, not pushed, not folded, in box, packed
    # object1: in_box, not pushed, not folded, in box, packed
    # object2: in_box, not pushed, not folded, in box, packed
    # object3: in_box, not pushed, not folded, in box, packed
    # object4: box, not pushed, not folded, contains [object0, object1, object2, object3], not packed

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place object0 (yellow_3D_cuboid) into the box
    # 2. Pick and place object1 (red_3D_polyhedron) into the box
    # 3. Push object0 (yellow_3D_cuboid) since it is soft
    # 4. Push object1 (red_3D_polyhedron) since it is soft

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.push(object0, box)
    robot.push(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick object0: Robot hand is empty and object0 is not in the box
    # 2. Place object0: Robot is holding object0 and all soft objects (object0) are in the box
    # 3. Pick object1: Robot hand is empty and object1 is not in the box
    # 4. Place object1: Robot is holding object1 and all soft objects (object0, object1) are in the box
    # 5. Push object0: Robot hand is empty, object0 is soft, and object0 is in the box
    # 6. Push object1: Robot hand is empty, object1 is soft, and object1 is in the box

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object2, object3, object0, object1]
    print("All task planning is done")
