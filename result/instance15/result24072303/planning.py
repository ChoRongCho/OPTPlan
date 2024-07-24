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
    is_packable: bool
    
    # Object physical properties 
    is_soft: bool
    is_foldable: bool
    is_elastic: bool
    is_fragile: bool
    is_rigid: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.is_packable:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
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
        if self.robot_handempty and obj.is_foldable:
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
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packable=True,
    is_soft=True, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packable=True,
    is_soft=True, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packable=True,
    is_soft=False, is_foldable=True, is_elastic=True, is_fragile=False, is_rigid=False
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packable=True,
    is_soft=False, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False
)

object4 = Object(
    index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packable=True,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=True, is_rigid=True
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3, object4], in_box=False, is_packable=False,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=False, is_rigid=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not in box
    # object1: out_box, not in box
    # object2: out_box, not in box
    # object3: in_box
    # object4: in_box
    # object5: box, contains object3 and object4

    # Goal state:
    # object0: in_box
    # object1: in_box
    # object2: out_box, not in box
    # object3: in_box
    # object4: out_box, not in box
    # object5: box, contains object0, object1, object3, and object4

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
    # Step 1: Out the fragile object (object4) from the box
    robot.out(object4, box)

    # Step 2: Pick and place a soft object (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Pick and place another soft object (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Place the fragile object (object4) back into the box
    robot.pick(object4, box)
    robot.place(object4, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: Rule 3 requires removing the fragile object initially in the box.
    # Reason for Step 2: Rule 2 requires placing a soft object before placing a fragile object.
    # Reason for Step 3: Ensuring there are enough soft objects in the box.
    # Reason for Step 4: Placing the fragile object back into the box after ensuring soft objects are present.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object4.in_box == True
    print("All task planning is done")
