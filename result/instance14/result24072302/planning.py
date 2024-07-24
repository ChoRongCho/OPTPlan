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
    is_heavy: bool
    
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
        if obj.object_type == 'box':
            print(f"Cannot pick {obj.name}: Rule 1 - You should never pick a box.")
            return
        if obj.in_box:
            print(f"Cannot pick {obj.name}: Object is already in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name}: Robot hand is not empty.")
            return
        
        # Effects
        self.state_holding(obj)
        print(f"Picked {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type == 'box':
            print(f"Cannot place {obj.name}: Rule 1 - You should never place a box.")
            return
        if obj.is_rigid and not obj.in_box:
            print(f"Cannot place {obj.name}: Rule 3 - Rigid object must be in the bin before placing.")
            return
        if not self.robot_now_holding:
            print(f"Cannot place {obj.name}: Robot is not holding any object.")
            return
        
        # Effects
        self.state_handempty()
        bin.in_bin_objects.append(obj)
        obj.in_box = True
        print(f"Placed {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot push {obj.name}: Robot hand is not empty.")
            return
        if not obj.is_soft:
            print(f"Cannot push {obj.name}: Object is not soft.")
            return
        for item in bin.in_bin_objects:
            if item.is_fragile and item.index == obj.index:
                print(f"Cannot push {obj.name}: Rule 4 - There is a fragile object on the soft object.")
                return
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name}: Robot hand is not empty.")
            return
        if not obj.is_elastic:
            print(f"Cannot fold {obj.name}: Rule 2 - Object is not foldable.")
            return
        
        # Effects
        obj.folded = True
        print(f"Folded {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj not in bin.in_bin_objects:
            print(f"Cannot out {obj.name}: Object is not in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot out {obj.name}: Robot hand is not empty.")
            return
        
        # Effects
        bin.in_bin_objects.remove(obj)
        obj.in_box = False
        self.state_handempty()
        print(f"Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=True
)

object1 = Object(
    index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_elastic=False, is_rigid=True, is_fragile=False, is_soft=False
)

object2 = Object(
    index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False,
    is_elastic=True, is_rigid=False, is_fragile=True, is_soft=False
)

object3 = Object(
    index=3, name='blue_2D_circle', color='blue', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False,
    is_elastic=False, is_rigid=True, is_fragile=True, is_soft=False
)

object4 = Object(
    index=4, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False,
    is_elastic=True, is_rigid=False, is_fragile=False, is_soft=False
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3, object4], in_box=True, is_heavy=False,
    is_elastic=False, is_rigid=False, is_fragile=False, is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state:
    # object0: out_box, not pushed, not folded
    # object1: out_box, not pushed, not folded
    # object2: in_box, not pushed, not folded
    # object3: in_box, not pushed, not folded
    # object4: in_box, not pushed, not folded
    # white_box: in_box, contains [object2, object3, object4]

    # Final state:
    # object0: in_box, pushed
    # object1: in_box, not pushed, not folded
    # object2: in_box, not pushed, not folded
    # object3: in_box, not pushed, not folded
    # object4: in_box, not pushed, not folded
    # white_box: in_box, contains [object0, object1, object2, object3, object4]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Push object0 (soft and elastic) to make space in the bin.
    # 2. Pick and place object1 (rigid) in the bin.
    # 3. Ensure all objects are in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Push object0 to make space in the bin
    robot.push(object0, box)
    
    # Pick and place object1 in the bin
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Pick and place object0 in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Never pick and place a box - Followed
    # Rule 2: Fold only foldable objects - Not applicable
    # Rule 3: Place rigid objects only if 3D object is in the bin - Followed
    # Rule 4: Push soft objects to make space, avoid if fragile object on top - Followed

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object0.pushed == True
    print("All task planning is done")
