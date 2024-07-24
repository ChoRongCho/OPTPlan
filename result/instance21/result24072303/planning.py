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
    is_packed: bool
    
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
        if self.robot_now_holding == obj and obj.is_rigid:
            if any(o.is_soft for o in bin.in_bin_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} in {bin.name} because no soft objects in bin")
        elif self.robot_now_holding == obj and obj.is_fragile:
            if any(o.is_elastic for o in bin.in_bin_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} in {bin.name} because no elastic objects in bin")
        elif self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and not obj.is_rigid and not obj.is_fragile:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
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
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object1 = Object(
    index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=False, is_rigid=True, is_fragile=True, is_soft=False
)

object3 = Object(
    index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=False, is_rigid=True, is_fragile=False, is_soft=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3], in_box=False, is_packed=False,
    is_elastic=False, is_rigid=False, is_fragile=False, is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given code

    # Second, using given rules and object's states, make a task planning strategy
    # We need to pack all objects into the white_box (object4)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4
    
    # c) Make an action sequence
    # Step 1: Place soft objects first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Step 2: Place rigid object (since soft objects are already in the box)
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Step 3: Ensure all objects are packed
    object0.is_packed = True
    object1.is_packed = True
    object2.is_packed = True
    object3.is_packed = True  # Already in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: It is prohibited to lift and relocate a container - We did not move the box
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before - Followed
    # Rule 3: Do not place a fragile object if there is no elastic object in the bin - Followed
    # Rule 4: When pushing an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted - Not used in this plan

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object3, object0, object1, object2]
    print("All task planning is done")
