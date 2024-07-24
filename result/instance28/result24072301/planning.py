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
    is_rigid: bool
    is_soft: bool
    is_foldable: bool
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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and not obj.is_rigid:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and self.robot_handempty:
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules for the bin_packing task. The 'pick' action ensures that only objects (not bins) that are not already in the bin can be picked up, and the robot's hand must be empty. The 'place' action ensures that only objects (not bins) can be placed in the bin, and the robot must be holding the object. The 'push' action is restricted to soft objects that are not rigid, and the robot's hand must be empty. The 'fold' action is restricted to foldable objects, and the robot's hand must be empty. The 'out' action allows the robot to remove objects from the bin, provided the robot's hand is empty. These actions ensure that the robot follows the rules and maintains a consistent state throughout the bin_packing task.

    def dummy(self):
        pass


 # Object Initial State
# Define the initial state of the objects and bin
object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_soft=False, is_foldable=False, in_box=False)
object1 = Object(index=1, name='white_3D_cone', color='white', shape='3D_cone', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_soft=True, is_foldable=False, in_box=False)
object2 = Object(index=2, name='brown_2D_rectangle', color='brown', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_soft=False, is_foldable=True, in_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[object2], is_rigid=False, is_soft=False, is_foldable=False, in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not pushed, not folded, not in box
    # object1: out_box, not pushed, not folded, not in box
    # object2: in_box, not pushed, not folded, in box
    # object3: box, contains object2

    # Goal State:
    # object0: in_box, not pushed, not folded, in box
    # object1: in_box, not pushed, not folded, in box
    # object2: in_box, not pushed, folded, in box
    # object3: box, contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the brown_2D_rectangle (object2) since it is foldable and already in the box.
    # 2. Pick and place the white_3D_cone (object1) into the box.
    # 3. Pick and place the black_3D_cylinder (object0) into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    # Fold the brown_2D_rectangle (object2)
    robot.fold(object2, box)

    # Pick and place the white_3D_cone (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Pick and place the black_3D_cylinder (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Fold action is performed on object2 because it is foldable and already in the box.
    # 2. Pick and place actions are performed on object1 and object0 to move them into the box.
    # 3. The sequence respects the rules: no box is picked or placed, foldable object is folded in the box, and the fragile object (object2) is already in the box before folding.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object2, object1, object0]
    print("All task planning is done")
