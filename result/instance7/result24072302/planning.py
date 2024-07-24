from dataclasses import dataclass
from typing import List

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
    in_bin_objects: List[int]
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_elastic: bool
    is_soft: bool
    is_foldable: bool
    in_box: bool


class Robot:
    def __init__(self, name: str = "UR5", goal: str = None, actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False

    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
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
        if self.robot_now_holding == obj and obj.object_type != 'box':
            obj.in_box = True
            bin.in_bin_objects.append(obj.index)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def out(self, obj, bin):
        if obj.in_box and not obj.is_soft:
            obj.in_box = False
            bin.in_bin_objects.remove(obj.index)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to adhere strictly to the given rules for the bin_packing task. The 'pick' and 'place' actions ensure that boxes are never picked or placed, aligning with rule 1. The 'fold' action is prioritized for foldable objects as per rule 2. The 'out' action handles rigid objects already in the bin, ensuring they are removed and replaced, in line with rule 3. The 'push' action is specifically for soft objects in the bin, following rule 4. These actions ensure the robot operates within the constraints and requirements of the task, maintaining a clear and logical flow of operations.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=True, 
    in_box=False
)

object1 = Object(
    index=1, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=True, 
    is_foldable=False, 
    in_box=False
)

object2 = Object(
    index=2, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False, 
    in_box=False
)

object3 = Object(
    index=3, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=True, 
    is_foldable=False, 
    in_box=True
)

white_box = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[3], 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False, 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given objects

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the foldable object (yellow_2D_rectangle)
    # 2. Out the rigid object (red_3D_polyhedron) from the bin and replace it
    # 3. Push the soft object (red_3D_polyhedron) in the bin
    # 4. Pick and place all objects into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Fold the foldable object
    robot.fold(object0, box)

    # Out the rigid object from the bin
    robot.out(object3, box)

    # Pick and place the yellow_2D_rectangle into the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place the brown_3D_cuboid into the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Pick and place the blue_2D_ring into the bin
    robot.pick(object2, box)
    robot.place(object2, box)

    # Pick and place the red_3D_polyhedron into the bin
    robot.pick(object3, box)
    robot.place(object3, box)

    # Push the soft object in the bin
    robot.push(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Fold the foldable object (yellow_2D_rectangle) as per rule 2.
    # 2. Out the rigid object (red_3D_polyhedron) from the bin and replace it as per rule 3.
    # 3. Push the soft object (brown_3D_cuboid) in the bin as per rule 4.
    # 4. Pick and place all objects into the bin to achieve the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    print("All task planning is done")
