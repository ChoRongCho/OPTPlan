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
    in_box: bool
    can_be_packed: bool
    
    # Object physical properties 
    is_elastic: bool
    is_rigid: bool
    is_fragile: bool
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
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.in_box = True
            if bin.in_bin_objects is None:
                bin.in_bin_objects = []
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=None, in_box=False, can_be_packed=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=None, in_box=False, can_be_packed=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=None, in_box=False, can_be_packed=True,
    is_elastic=False, is_rigid=True, is_fragile=False, is_soft=False
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=None, in_box=True, can_be_packed=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=False
)

object4 = Object(
    index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=None, in_box=True, can_be_packed=True,
    is_elastic=False, is_rigid=True, is_fragile=True, is_soft=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, can_be_packed=False,
    is_elastic=False, is_rigid=False, is_fragile=False, is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_box,
        object5.name: object5.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: False,
        object3.name: True,
        object4.name: True,
        object5.name: [object0, object1, object3, object4]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: it is prohibited to lift and relocate a container
    # Rule 2: do not place a fragile object if there is no soft object in the bin
    # Rule 3: when a fragile object in the bin at the initial state, out of the fragile object and replace it into the bin
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object5
    
    # c) Action sequence
    # Step 1: Out the fragile object (green_3D_cylinder) from the box
    robot.out(object4, box)
    
    # Step 2: Pick and place the soft objects into the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Step 3: Place the fragile object back into the box
    robot.pick(object4, box)
    robot.place(object4, box)
    
    # Step 4: Ensure the white_2D_ring is already in the box (no action needed)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: Rule 3 requires us to out the fragile object initially in the box
    # Reason for Step 2: Rule 2 requires us to place soft objects before placing fragile objects
    # Reason for Step 3: Place the fragile object back into the box after soft objects are placed
    # Reason for Step 4: The white_2D_ring is already in the box, no action needed
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_bin_objects == [object0, object1, object3, object4]
    
    print("All task planning is done")
