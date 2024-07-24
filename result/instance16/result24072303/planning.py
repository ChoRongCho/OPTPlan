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
    is_fragile: bool
    
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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_fragile or obj.is_elastic:
                if all(o.is_elastic for o in bin.in_bin_objects):
                    # Effects
                    self.state_handempty()
                    obj.in_box = True
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} due to rule constraints")
            else:
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
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_handempty()
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='beige_2D_ring', 
    color='beige', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_fragile=False, 
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
    is_fragile=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_fragile=True, 
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
    in_bin_objects=[], 
    is_elastic=False, 
    is_fragile=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box, not in box
    # object1: out_box, not in box
    # object2: in_box, in box
    # object3: box, not in box

    # Final State
    # object0: in_bin, not in box
    # object1: in_bin, not in box
    # object2: in_bin, in box
    # object3: box, not in box, contains [object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: It is prohibited to lift and relocate a container
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: When placing a fragile object, the soft objects must be in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Step 1: Pick beige_2D_ring (object0)
    robot.pick(object0, box)
    
    # Step 2: Place beige_2D_ring (object0) in white_box (object3)
    robot.place(object0, box)
    
    # Step 3: Pick transparent_3D_cylinder (object1)
    robot.pick(object1, box)
    
    # Step 4: Place transparent_3D_cylinder (object1) in white_box (object3)
    robot.place(object1, box)
    
    # Step 5: Out white_2D_circle (object2) from white_box (object3)
    robot.out(object2, box)
    
    # Step 6: Place white_2D_circle (object2) in white_box (object3)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: beige_2D_ring is elastic and can be picked
    # Reason for Step 2: beige_2D_ring is elastic and can be placed in the box
    # Reason for Step 3: transparent_3D_cylinder is elastic and can be picked
    # Reason for Step 4: transparent_3D_cylinder is elastic and can be placed in the box
    # Reason for Step 5: white_2D_circle is fragile and elastic, needs to be out and placed again to satisfy the rules
    # Reason for Step 6: white_2D_circle is fragile and elastic, can be placed in the box after elastic objects

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
