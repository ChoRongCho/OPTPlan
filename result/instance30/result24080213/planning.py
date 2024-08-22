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
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    is_foldable=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    is_elastic=True, 
    is_soft=True, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_bin_objects=[], 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(
        index=0, 
        name='red_3D_polyhedron', 
        color='red', 
        shape='3D_polyhedron', 
        object_type='obj', 
        is_soft=True, 
        in_box=False, 
        out_box=True
    )

    object1 = Object(
        index=1, 
        name='yellow_2D_rectangle', 
        color='yellow', 
        shape='2D_rectangle', 
        object_type='obj', 
        is_foldable=True, 
        in_box=False, 
        out_box=True
    )

    object2 = Object(
        index=2, 
        name='black_2D_loop', 
        color='black', 
        shape='2D_loop', 
        object_type='obj', 
        is_elastic=True, 
        is_soft=True, 
        in_box=True, 
        out_box=False
    )

    object3 = Object(
        index=3, 
        name='white_box', 
        color='white', 
        shape='box', 
        object_type='box', 
        in_bin_objects=[], 
        in_box=True, 
        out_box=False
    )

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False}  # Box state is not included in the goal check
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the red_3D_polyhedron (soft object) in the box first.
    # 2. Fold the yellow_2D_rectangle (foldable object).
    # 3. Place the yellow_2D_rectangle in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place the red_3D_polyhedron in the box
    robot.pick(object0)
    robot.place(object0, box)

    # Fold the yellow_2D_rectangle
    robot.fold(object1)

    # Place the yellow_2D_rectangle in the box
    robot.pick(object1)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The red_3D_polyhedron is soft, so it should be placed in the box first.
    # 2. The yellow_2D_rectangle is foldable, so it should be folded before placing it in the box.
    # 3. The black_2D_loop is already in the box, so no action is needed for it.
    # 4. The white_box is already in the box, so no action is needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True  # Box state is not included in the goal check

    print("All task planning is done")
