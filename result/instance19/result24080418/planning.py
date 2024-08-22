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
    is_fragile: bool
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
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
        if obj.in_box:
            print(f"Cannot pick {obj.name}, it is already in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name}, robot hand is not empty.")
            return
        
        # Effects
        self.state_holding(obj)
        print(f"Picked {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_handempty:
            print(f"Cannot place {obj.name}, robot hand is empty.")
            return
        if obj.is_fragile or obj.is_rigid:
            if any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot place {obj.name}, soft objects should be placed first.")
                return
        
        # Effects
        self.state_handempty()
        obj.in_box = True
        bin.in_bin_objects.append(obj)
        print(f"Placed {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot push {obj.name}, robot hand is not empty.")
            return
        if not obj.is_soft:
            print(f"Cannot push {obj.name}, only soft objects can be pushed.")
            return
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name}, robot hand is not empty.")
            return
        if not obj.is_elastic:
            print(f"Cannot fold {obj.name}, object is not foldable.")
            return
        
        # Effects
        obj.folded = True
        print(f"Folded {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if not obj.in_box:
            print(f"Cannot take out {obj.name}, it is not in the bin.")
            return
        
        # Effects
        self.state_holding(obj)
        obj.in_box = False
        bin.in_bin_objects.remove(obj)
        self.state_handempty()
        print(f"Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=True, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='out_box', 
    in_box=False
)

object3 = Object(
    index=3, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=True, 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='in_box', 
    in_box=True
)

white_box = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        white_box.name: white_box.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        white_box.name: [object0, object1, object2, object3]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft and elastic object (object0) first.
    # 2. Place the rigid object (object1) next.
    # 3. Place the fragile and rigid object (object2) last.
    # 4. Ensure object3 is already in the box.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = white_box
    
    # c) Action sequence
    # Pick and place the soft and elastic object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the rigid object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Pick and place the fragile and rigid object (object2)
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed object0 first because it is soft and elastic.
    # 2. Placed object1 next because it is rigid and there are no more soft objects to place.
    # 3. Placed object2 last because it is fragile and rigid, and all soft objects are already placed.
    # 4. Object3 is already in the box, so no action is needed for it.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert set(white_box.in_bin_objects) == {object0, object1, object2, object3}
    
    print("All task planning is done")
