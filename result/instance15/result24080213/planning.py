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
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: list = None
    
    # Object physical properties 
    is_fragile: bool = False
    is_rigid: bool = False
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = False




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    is_soft=True, is_elastic=True, out_box=True
)

object1 = Object(
    index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj',
    is_soft=True, is_foldable=True, out_box=True
)

object2 = Object(
    index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    is_soft=True, is_elastic=True, out_box=True
)

object3 = Object(
    index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj',
    is_rigid=True, is_fragile=True, in_box=True
)

object4 = Object(
    index=4, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    is_elastic=True, in_box=True
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box'
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        0: {'name': 'brown_3D_cuboid', 'shape': '3D_cuboid', 'color': 'brown', 'predicates': ['is_soft', 'is_elastic'], 'pose': 'out_box'},
        1: {'name': 'black_2D_loop', 'shape': '2D_loop', 'color': 'black', 'predicates': ['is_soft', 'is_foldable'], 'pose': 'out_box'},
        2: {'name': 'white_3D_cylinder', 'shape': '3D_cylinder', 'color': 'white', 'predicates': ['is_soft', 'is_elastic'], 'pose': 'out_box'},
        3: {'name': 'green_3D_sphere', 'shape': '3D_sphere', 'color': 'green', 'predicates': ['is_rigid', 'is_fragile'], 'pose': 'in_box'},
        4: {'name': 'white_2D_loop', 'shape': '2D_loop', 'color': 'white', 'predicates': ['is_elastic'], 'pose': 'in_box'},
        5: {'name': 'white_box', 'shape': 'box', 'color': 'white', 'predicates': [], 'pose': 'box'}
    }

    # Goal State
    goal_state = {
        0: {'name': 'brown_3D_cuboid', 'shape': '3D_cuboid', 'color': 'brown', 'predicates': ['is_soft', 'is_elastic'], 'pose': 'in_box'},
        1: {'name': 'black_2D_loop', 'shape': '2D_loop', 'color': 'black', 'predicates': ['is_soft', 'is_foldable'], 'pose': 'in_box'},
        2: {'name': 'white_3D_cylinder', 'shape': '3D_cylinder', 'color': 'white', 'predicates': ['is_soft', 'is_elastic'], 'pose': 'in_box'},
        3: {'name': 'green_3D_sphere', 'shape': '3D_sphere', 'color': 'green', 'predicates': ['is_rigid', 'is_fragile'], 'pose': 'in_box'},
        4: {'name': 'white_2D_loop', 'shape': '2D_loop', 'color': 'white', 'predicates': ['is_elastic'], 'pose': 'in_box'},
        5: {'name': 'white_box', 'shape': 'box', 'color': 'white', 'predicates': [], 'pose': 'box'}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place all soft objects in the box first.
    # 2. Fold the foldable object before placing it in the box.
    # 3. Place the rigid and fragile object last.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    # 1. Place brown_3D_cuboid (soft) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # 2. Fold black_2D_loop (foldable) and place it in the box
    robot.fold(object1)
    robot.pick(object1)
    robot.place(object1, box)

    # 3. Place white_3D_cylinder (soft) in the box
    robot.pick(object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed all soft objects first as per the rule.
    # - Folded the foldable object before placing it in the box.
    # - The rigid and fragile object was already in the box, so no action was needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True

    print("All task planning is done")
