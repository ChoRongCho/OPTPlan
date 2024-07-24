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
    is_out_box: bool
    
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
        if self.robot_handempty and obj.is_out_box:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} due to rule 2")
                return
            if obj.is_fragile and not any(o.is_elastic for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} due to rule 3")
                return
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box and obj.is_soft:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
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
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object1 = Object(
    index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_elastic=False, is_rigid=True, is_fragile=True, is_soft=False
)

object3 = Object(
    index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_out_box=False,
    is_elastic=False, is_rigid=True, is_fragile=False, is_soft=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3], is_in_box=True, is_out_box=False,
    is_elastic=False, is_rigid=False, is_fragile=False, is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given code

    # Second, using given rules and object's states, make a task planning strategy
    # We need to place all objects in the white_box (object4)
    # We need to follow the rules:
    # 1. It is prohibited to lift and relocate a container
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before
    # 3. Do not place a fragile object if there is no elastic object in the bin
    # 4. When pushing an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Step 1: Pick and place white_3D_cylinder (soft and elastic)
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 2: Pick and place yellow_3D_cuboid (soft and elastic)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 3: Pick and place green_3D_cylinder (rigid and fragile)
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - object0 and object1 are soft and elastic, so they can be placed first
    # - object2 is rigid and fragile, but since object0 (elastic) is already in the box, it can be placed

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True  # object3 was already in the box
    assert object4.is_in_box == True  # object4 is the box itself
    print("All task planning is done")
