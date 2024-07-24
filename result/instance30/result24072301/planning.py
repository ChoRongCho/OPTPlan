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
    is_soft: bool
    is_foldable: bool
    
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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            # Effects
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and not any(o.object_type == 'fragile' for o in bin.in_bin_objects):
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
        if obj.in_box and obj.object_type != 'box':
            # Effects
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. The 'pick' action ensures that only objects (not boxes) that are not already in the bin can be picked up, and the robot's hand must be empty. The 'place' action ensures that the object being placed is currently held by the robot and is not a box. The 'push' action is restricted to soft objects and ensures no fragile objects are on top of the soft object. The 'fold' action is only allowed for foldable objects. The 'out' action allows removing objects from the bin, ensuring they are not boxes. These actions ensure safe and efficient bin packing while adhering to the specified rules

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_foldable=True, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='black_2D_ring', 
    color='black', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_foldable=False, 
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
    in_bin_objects=[object2], 
    is_soft=False, 
    is_foldable=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in box, not pushed, not folded
    # object1: out_box, not in box, not pushed, not folded
    # object2: in_box, in box, not pushed, not folded
    # object3: box, not in box, not pushed, not folded, contains object2

    # Goal State:
    # object0: out_box, not in box, not pushed, not folded
    # object1: in_box, in box, not pushed, folded
    # object2: in_box, in box, pushed, not folded
    # object3: box, not in box, not pushed, not folded, contains object1 and object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Out object2 from the box (since it's rigid and in the box initially)
    # 2. Fold object1 (since it's foldable)
    # 3. Push object2 (since it's soft)
    # 4. Place object1 in the box
    # 5. Place object2 in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    robot.out(object2, box)  # Out black_2D_ring from white_box
    robot.fold(object1, box)  # Fold yellow_2D_rectangle
    robot.push(object2, box)  # Push black_2D_ring
    robot.pick(object1, box)  # Pick yellow_2D_rectangle
    robot.place(object1, box)  # Place yellow_2D_rectangle in white_box
    robot.pick(object2, box)  # Pick black_2D_ring
    robot.place(object2, box)  # Place black_2D_ring in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Out action is performed to remove the rigid object from the box initially.
    # 2. Fold action is performed because the object is foldable.
    # 3. Push action is performed to make more space in the box since the object is soft.
    # 4. Pick and place actions are performed to move the objects into the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == False
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == False
    assert object1.folded == True
    assert object2.pushed == True
    assert object3.in_bin_objects == [object1, object2]
    print("All task planning is done")
