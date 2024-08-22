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
    is_foldable: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    can_be_packed: bool


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
        if not self.robot_handempty and obj == self.robot_now_holding:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box and not obj.pushed:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and not obj.folded:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. Each action has specific preconditions that must be met before the action can be executed, ensuring that the robot operates within the constraints of the task. For example, the 'place' action requires the robot to be holding an object, and the 'fold' action can only be performed on foldable objects. These preconditions and effects ensure that the robot's actions are logical and adhere to the task requirements, such as placing soft objects before fragile or rigid ones and only pushing soft objects after placing them in the bin. This structured approach helps in maintaining a clear and predictable state of the robot and objects, facilitating efficient task planning and execution.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=True, 
    is_foldable=False, 
    in_box=False, 
    can_be_packed=True
)

object1 = Object(
    index=1, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=True, 
    is_rigid=False, 
    is_foldable=True, 
    in_box=False, 
    can_be_packed=True
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_rigid=False, 
    is_foldable=False, 
    in_box=True, 
    can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in box
    # object1: out_box, not pushed, not folded, not in box
    # object2: in_box, not pushed, not folded, in box, empty

    # Final State:
    # object0: in_box, not pushed, not folded, in box
    # object1: in_box, not pushed, folded, in box
    # object2: in_box, not pushed, not folded, in box, contains object0 and object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the black_2D_ring (object1) since it is foldable.
    # 2. Pick and place the black_2D_ring (object1) in the white_box (object2).
    # 3. Pick and place the yellow_3D_cylinder (object0) in the white_box (object2).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object2

    # Action sequence
    robot.fold(object1, box)  # Fold the black_2D_ring
    robot.pick(object1, box)  # Pick the black_2D_ring
    robot.place(object1, box)  # Place the black_2D_ring in the white_box
    robot.pick(object0, box)  # Pick the yellow_3D_cylinder
    robot.place(object0, box)  # Place the yellow_3D_cylinder in the white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Fold the black_2D_ring because it is foldable.
    # 2. Place the black_2D_ring in the box first because it is a soft object (foldable and not rigid).
    # 3. Place the yellow_3D_cylinder in the box after the black_2D_ring because it is a rigid object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object1.folded == True
    assert object2.in_bin_objects == [object1, object0]
    print("All task planning is done")
