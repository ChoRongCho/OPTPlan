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
    
    # Object physical properties
    is_soft: bool
    is_elastic: bool
    is_foldable: bool
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, is_foldable=True,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, is_foldable=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, is_foldable=False,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=False, is_foldable=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[3], is_soft=False, is_elastic=False, is_foldable=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True, 'folded': False, 'pushed': False},
        1: {'in_box': False, 'out_box': True, 'folded': False, 'pushed': False},
        2: {'in_box': False, 'out_box': True, 'folded': False, 'pushed': False},
        3: {'in_box': True, 'out_box': False, 'folded': False, 'pushed': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [3]}
    }

    goal_state = {
        0: {'in_box': True, 'out_box': False, 'folded': True, 'pushed': False},
        1: {'in_box': True, 'out_box': False, 'folded': False, 'pushed': True},
        2: {'in_box': True, 'out_box': False, 'folded': False, 'pushed': False},
        3: {'in_box': True, 'out_box': False, 'folded': False, 'pushed': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the yellow_2D_rectangle (object0) since it is foldable.
    # 2. Place the brown_3D_cuboid (object1) in the box first because it is soft.
    # 3. Place the yellow_2D_rectangle (object0) in the box.
    # 4. Place the blue_2D_loop (object2) in the box.
    # 5. Push the brown_3D_cuboid (object1) since it is soft.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Perform actions
    # Fold the yellow_2D_rectangle
    robot.fold(object0)
    assert object0.folded == True

    # Place the brown_3D_cuboid in the box
    robot.place(object1, box)
    assert object1.in_box == True
    assert object1.out_box == False
    box.in_bin_objects.append(object1.index)

    # Place the yellow_2D_rectangle in the box
    robot.place(object0, box)
    assert object0.in_box == True
    assert object0.out_box == False
    box.in_bin_objects.append(object0.index)

    # Place the blue_2D_loop in the box
    robot.place(object2, box)
    assert object2.in_box == True
    assert object2.out_box == False
    box.in_bin_objects.append(object2.index)

    # Push the brown_3D_cuboid
    robot.push(object1)
    assert object1.pushed == True

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Folded the yellow_2D_rectangle because it is foldable.
    # 2. Placed the brown_3D_cuboid first because it is soft.
    # 3. Placed the yellow_2D_rectangle after the soft object.
    # 4. Placed the blue_2D_loop after the soft object.
    # 5. Pushed the brown_3D_cuboid after placing it in the bin.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [3, 1, 0, 2]

    print("All task planning is done")
