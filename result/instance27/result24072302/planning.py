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
    is_elastic: bool
    is_soft: bool
    
    # Object physical properties
    init_pose: str
    in_box: bool


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
        # Preconditions
        if obj.object_type == 'box':
            print(f"Cannot pick {obj.name} because it is a box.")
            return
        if obj.in_box:
            print(f"Cannot pick {obj.name} because it is already in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        self.state_holding(obj)
        print(f"Picked {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type == 'box':
            print(f"Cannot place {obj.name} because it is a box.")
            return
        if not self.robot_now_holding == obj:
            print(f"Cannot place {obj.name} because the robot is not holding it.")
            return
        if obj.is_soft and not any(o.is_soft for o in bin.in_bin_objects):
            print(f"Cannot place {obj.name} because there are no soft objects in the bin.")
            return
        if not obj.is_soft and not any(o.is_elastic for o in bin.in_bin_objects):
            print(f"Cannot place {obj.name} because there are no elastic objects in the bin.")
            return
        
        # Effects
        self.state_handempty()
        obj.in_box = True
        bin.in_bin_objects.append(obj)
        print(f"Placed {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot push {obj.name} because the robot hand is not empty.")
            return
        if not obj.is_soft:
            print(f"Cannot push {obj.name} because it is not a soft object.")
            return
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        obj.folded = True
        print(f"Folded {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj not in bin.in_bin_objects:
            print(f"Cannot take out {obj.name} because it is not in the bin.")
            return
        
        # Effects
        self.state_handempty()
        obj.in_box = False
        bin.in_bin_objects.remove(obj)
        print(f"Out {obj.name} from {bin.name}")

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
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box', 
    in_box=False
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
    is_elastic=True, 
    is_soft=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=True, 
    init_pose='in_box', 
    in_box=True
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
    is_elastic=False, 
    is_soft=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in box
    # object1: out_box, not in box
    # object2: in_box, in box
    # object3: box, contains object2

    # Final State:
    # object0: in_box, in box
    # object1: in_box, in box
    # object2: in_box, in box
    # object3: box, contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place object0 (soft object) into the box
    # 2. Pick and place object1 (rigid object) into the box (after soft object is in)
    # 3. Ensure object2 remains in the box
    # 4. Ensure object3 (box) is not picked or placed

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Pick and place object0 (soft object) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place object1 (rigid object) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: You should never pick and place a box - Not picking or placing object3 (box)
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before - object0 (soft) is placed before object1 (rigid)
    # Rule 3: Do not place a fragile object if there is no elastic object in the bin - object1 (rigid) is placed after object0 (elastic)
    # Rule 4: When pushing an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted - No push actions used

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
