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
    is_soft: bool
    is_foldable: bool
    is_rigid: bool
    is_fragile: bool


class Robot:
    def __init__(self, name: str = "UR5", goal: str = None, actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False

    def state_base(self):
        self.robot_base_pose = True

    def pick(self, obj, bin):
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
                return
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable and not obj.in_box:
            obj.folded = True
            print(f"Fold {obj.name}")

    def out(self, obj, bin):
        if obj.in_box and obj.is_rigid:
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            print(f"Out {obj.name} from {bin.name}")
            self.place(obj, bin)

# Reason:
# The robot actions are designed to follow the given rules for the bin_packing task. The 'pick' action ensures that the robot does not pick up boxes and only picks objects that are not already in the bin. The 'place' action checks if a rigid object can only be placed in the bin if a soft object is already there, ensuring the safety of fragile items. The 'push' action requires the robot's hand to be empty and the object to be in the bin, simulating a downward push. The 'fold' action ensures foldable objects are folded on the platform, not in the bin. The 'out' action handles the removal and replacement of rigid objects in the bin, ensuring the bin's contents are managed correctly. These actions ensure the robot follows the rules and handles objects appropriately during the bin_packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_soft=True, is_foldable=False, is_rigid=False, is_fragile=False
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=False, is_rigid=True, is_fragile=True
)

object2 = Object(
    index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=True, is_rigid=False, is_fragile=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2], in_box=False, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=False, is_rigid=False, is_fragile=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in bin, not packed
    # object1: out_box, not in bin, not packed
    # object2: in_box, not packed
    # object3: box, contains object2, not packed

    # Goal State:
    # object0: in_bin, packed
    # object1: in_bin, packed
    # object2: in_bin, folded, packed
    # object3: box, contains object0, object1, object2, not packed

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object2) since it is foldable and in the box.
    # 2. Pick and place the white_3D_cylinder (object0) into the box.
    # 3. Pick and place the green_3D_cylinder (object1) into the box.
    # 4. Push the white_3D_cylinder (object0) in the box.
    # 5. Push the green_3D_cylinder (object1) in the box.
    # 6. Push the yellow_2D_rectangle (object2) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    # Fold the yellow_2D_rectangle (object2)
    robot.fold(object2, box)

    # Pick and place the white_3D_cylinder (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place the green_3D_cylinder (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Push the white_3D_cylinder (object0) in the box
    robot.push(object0, box)

    # Push the green_3D_cylinder (object1) in the box
    robot.push(object1, box)

    # Push the yellow_2D_rectangle (object2) in the box
    robot.push(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Fold the yellow_2D_rectangle (object2) because it is foldable and not in the bin (Rule 3).
    # 2. Pick and place the white_3D_cylinder (object0) because it is soft and should be placed before any rigid object (Rule 5).
    # 3. Pick and place the green_3D_cylinder (object1) because it is rigid and should be placed after a soft object (Rule 2).
    # 4. Push the white_3D_cylinder (object0) to ensure it is properly placed in the bin (Rule 5).
    # 5. Push the green_3D_cylinder (object1) to ensure it is properly placed in the bin (Rule 5).
    # 6. Push the yellow_2D_rectangle (object2) to ensure it is properly placed in the bin (Rule 5).

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
