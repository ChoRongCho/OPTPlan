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
    is_elastic: bool
    is_soft: bool
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=True, is_fragile=False, is_rigid=False,
    init_pose='out_box', in_box=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_fragile=False, is_rigid=True,
    init_pose='out_box', in_box=False
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_fragile=True, is_rigid=True,
    init_pose='out_box', in_box=False
)

object3 = Object(
    index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_fragile=False, is_rigid=False,
    init_pose='in_box', in_box=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_fragile=False, is_rigid=False,
    init_pose='box', in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'red_3D_polyhedron', 'in_box': False},
        1: {'name': 'yellow_3D_cylinder', 'in_box': False},
        2: {'name': 'green_3D_cylinder', 'in_box': False},
        3: {'name': 'white_2D_loop', 'in_box': True},
        4: {'name': 'white_box', 'in_box': False}
    }
    
    goal_state = {
        0: {'name': 'red_3D_polyhedron', 'in_box': True},
        1: {'name': 'yellow_3D_cylinder', 'in_box': True},
        2: {'name': 'green_3D_cylinder', 'in_box': True},
        3: {'name': 'white_2D_loop', 'in_box': True},
        4: {'name': 'white_box', 'in_box': False, 'in_bin_objects': [0, 1, 2, 3]}
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

    # c) Action sequence
    # Place the soft object first
    robot.pick(object0)
    robot.place(object0, box)
    
    # Place the rigid object next
    robot.pick(object1)
    robot.place(object1, box)
    
    # Place the fragile object next
    robot.pick(object2)
    robot.place(object2, box)
    
    # The white_2D_loop is already in the box, no need to move it

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The red_3D_polyhedron (soft) is placed first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # 2. The yellow_3D_cylinder (rigid) is placed next.
    # 3. The green_3D_cylinder (fragile) is placed last.
    # 4. The white_2D_loop is already in the box, so no action is needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
