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
    out_box: bool
    
    # Object physical properties
    is_elastic: bool
    is_soft: bool
    is_foldable: bool
    is_rigid: bool
    is_fragile: bool


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
        if obj.object_type != 'box' and obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid:
                soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
                if not soft_objects_in_bin:
                    print(f"Cannot Place {obj.name} because no soft object in bin")
                    return
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
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
        if self.robot_handempty and obj.is_foldable and obj.out_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that the robot does not attempt to pick up a box and only picks objects that are not already in the bin. The 'place' action ensures that rigid objects are only placed in the bin if a soft object is already present, adhering to the rule. The 'push' and 'fold' actions ensure that the robot's hand is empty before performing these actions, and the 'fold' action is only performed on foldable objects that are not in the bin. The 'out' action ensures that objects are removed from the bin and placed on the platform, making the robot's hand empty afterward. These actions ensure that the robot follows the rules and maintains the correct state of objects and the bin during the bin-packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, out_box=True,
    is_elastic=True, is_soft=True, is_foldable=False, is_rigid=False, is_fragile=False
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, out_box=True,
    is_elastic=False, is_soft=False, is_foldable=False, is_rigid=True, is_fragile=True
)

object2 = Object(
    index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, out_box=False,
    is_elastic=False, is_soft=False, is_foldable=True, is_rigid=False, is_fragile=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2], in_box=False, out_box=False,
    is_elastic=False, is_soft=False, is_foldable=False, is_rigid=False, is_fragile=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    # object0: out_box, is_soft
    # object1: out_box, is_rigid
    # object2: in_box, is_foldable
    # object3: box, contains object2

    # Final state
    # object0: in_box, is_soft, pushed
    # object1: in_box, is_rigid
    # object2: in_box, is_foldable, folded
    # object3: box, contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the foldable object (object2) that is not in the bin but on the platform.
    # 2. Out the rigid object (object1) from the bin and replace it into the bin.
    # 3. Pick, place, and push the soft object (object0) into the bin.
    # 4. Place the rigid object (object1) into the bin after the soft object is in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Fold the foldable object (object2)
    robot.fold(object2, box)
    
    # Out the rigid object (object1) from the bin
    robot.out(object2, box)
    
    # Pick, place, and push the soft object (object0) into the bin
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)
    
    # Place the rigid object (object1) into the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box.
    # Rule 2: When placing a rigid object in the bin, the soft object must be in the bin before.
    # Rule 3: If there is a foldable object, fold the object not in the bin but on the platform.
    # Rule 4: When a rigid object is in the bin at the initial state, out of the rigid object and replace it into the bin.
    # Rule 5: If there are soft objects, pick, place, and push them into the bin.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
