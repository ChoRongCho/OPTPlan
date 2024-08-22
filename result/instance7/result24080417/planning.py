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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




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
    is_foldable=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
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
    is_foldable=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='blue_2D_loop', 
    color='blue', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
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
    is_foldable=False, 
    is_elastic=False, 
    is_soft=True, 
    in_box=True, 
    out_box=False
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        'object0': {'in_box': False, 'out_box': True},
        'object1': {'in_box': False, 'out_box': True},
        'object2': {'in_box': False, 'out_box': True},
        'object3': {'in_box': True, 'out_box': False},
        'object4': {'in_box': False, 'out_box': False}  # box
    }

    goal_state = {
        'object0': {'in_box': True, 'out_box': False},
        'object1': {'in_box': True, 'out_box': False},
        'object2': {'in_box': True, 'out_box': False},
        'object3': {'in_box': True, 'out_box': False},
        'object4': {'in_box': False, 'out_box': False}  # box
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects first if there are any soft objects.
    # 2. Fold objects only if they are foldable.
    # 3. Push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place the soft object (object1) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1)

    # 2. Fold the foldable object (object0)
    robot.fold(object0)
    object0.folded = True

    # 3. Place the folded object (object0) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0)

    # 4. Place the non-foldable, non-soft object (object2) in the box
    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False
    box.in_bin_objects.append(object2)

    # 5. The red_3D_polyhedron (object3) is already in the box, no action needed

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object1) first as per the rule.
    # - Folded the foldable object (object0) before placing it in the box.
    # - Placed the non-foldable, non-soft object (object2) after the soft object.
    # - The red_3D_polyhedron (object3) was already in the box, so no action was needed.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
