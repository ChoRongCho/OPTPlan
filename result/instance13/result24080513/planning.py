from dataclasses import dataclass, field
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
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: List[int] = field(default_factory=list)
    
    # Object physical properties 
    is_foldable: bool = False
    is_rigid: bool = False
    is_elastic: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='white_1D_loop', color='white', shape='1D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='black_3D_cuboid', color='black', shape='3D_cuboid', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The initial state is defined based on the input images.
# Each object has specific properties and predicates that determine its behavior in the bin_packing task.
# The 'white_box' is the only object that starts in the box, while all other objects start out of the box.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='white_1D_loop', color='white', shape='1D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='black_3D_cuboid', color='black', shape='3D_cuboid', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: True,  # white_1D_loop should be in the box
        1: True,  # yellow_2D_rectangle should be in the box
        2: True,  # transparent_2D_circle should be in the box
        3: True,  # black_3D_cuboid should be in the box
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the yellow_2D_rectangle since it is foldable.
    # 2. Place the elastic objects (white_1D_loop and transparent_2D_circle) in the box first.
    # 3. Place the folded yellow_2D_rectangle in the box.
    # 4. Finally, place the rigid black_3D_cuboid in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Fold the yellow_2D_rectangle
    robot.fold(object1)
    assert object1.folded == True

    # Place the white_1D_loop in the box
    robot.place(object0, box)
    assert object0.in_box == True

    # Place the transparent_2D_circle in the box
    robot.place(object2, box)
    assert object2.in_box == True

    # Place the folded yellow_2D_rectangle in the box
    robot.place(object1, box)
    assert object1.in_box == True

    # Place the black_3D_cuboid in the box
    robot.place(object3, box)
    assert object3.in_box == True

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Folded the yellow_2D_rectangle because it is foldable.
    # 2. Placed the elastic objects first as per the rule to place soft objects before rigid ones.
    # 3. Placed the rigid black_3D_cuboid last as per the rule.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True

    print("All task planning is done")
