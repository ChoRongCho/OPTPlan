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
    is_foldable: bool
    is_elastic: bool
    is_soft: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_soft=True, is_rigid=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_soft=True, is_rigid=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_soft=False, is_rigid=False,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_soft=False, is_rigid=True,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_soft=False, is_rigid=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }
    
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place soft objects first
    robot.place(object0, box)  # Place red_3D_polyhedron
    robot.place(object1, box)  # Place yellow_3D_cuboid

    # 2. Place other objects
    robot.place(object2, box)  # Place white_2D_loop (already in box, no action needed)
    robot.place(object3, box)  # Place black_2D_circle (already in box, no action needed)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - red_3D_polyhedron and yellow_3D_cuboid are soft objects and should be placed first.
    # - white_2D_loop and black_2D_circle are already in the box, so no need to place them again.
    # - No objects need to be folded or pushed according to the rules.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
