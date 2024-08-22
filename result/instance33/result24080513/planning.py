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
    is_rigid: bool
    is_fragile: bool
    is_elastic: bool
    is_soft: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_fragile=False,
    is_elastic=False, is_soft=True, in_box=False, out_box=True
)

object1 = Object(
    index=1, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_fragile=True,
    is_elastic=False, is_soft=False, in_box=False, out_box=True
)

object2 = Object(
    index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_fragile=False,
    is_elastic=True, is_soft=False, in_box=False, out_box=True
)

object3 = Object(
    index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=True, is_fragile=False,
    is_elastic=False, is_soft=False, in_box=False, out_box=True
)

object4 = Object(
    index=4, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_rigid=False, is_fragile=True,
    is_elastic=False, is_soft=False, in_box=True, out_box=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_fragile=False,
    is_elastic=False, is_soft=False, in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': False, 'out_box': True},
        3: {'in_box': False, 'out_box': True},
        4: {'in_box': True, 'out_box': False},
        5: {'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }

    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False},
        5: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3, 4]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    # 1. Place the soft object (object0) in the box first
    robot.place(object0, box)
    # 2. Place the fragile object (object1) in the box
    robot.place(object1, box)
    # 3. Place the elastic object (object2) in the box
    robot.place(object2, box)
    # 4. Place the rigid object (object3) in the box
    robot.place(object3, box)
    # 5. The foldable object (object4) is already in the box, no need to fold or place it

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - object0 (soft) is placed first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # - object1 (fragile) is placed after the soft object.
    # - object2 (elastic) is placed next as it is neither fragile nor rigid.
    # - object3 (rigid) is placed last among the new objects to be placed.
    # - object4 (foldable) is already in the box and does not need to be folded or placed again.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_bin_objects == [0, 1, 2, 3, 4]

    print("All task planning is done")
