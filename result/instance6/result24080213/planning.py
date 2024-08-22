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
    is_soft: bool
    is_elastic: bool
    is_foldable: bool
    
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
    is_soft=False, 
    is_elastic=False, 
    is_foldable=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=True, 
    is_foldable=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_elastic=False, 
    is_foldable=False, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=False, 
    is_foldable=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'folded': False},
        1: {'in_box': False, 'folded': False},
        2: {'in_box': True, 'folded': False},
        3: {'in_box': False, 'folded': False, 'in_bin_objects': []}
    }
    
    goal_state = {
        0: {'in_box': True, 'folded': True},
        1: {'in_box': True, 'folded': False},
        2: {'in_box': True, 'folded': False},
        3: {'in_box': False, 'folded': False, 'in_bin_objects': [0, 1, 2]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the yellow_2D_rectangle (object0) since it is foldable.
    # 2. Place the red_3D_polyhedron (object2) in the box first since it is soft.
    # 3. Place the yellow_2D_rectangle (object0) in the box.
    # 4. Place the transparent_3D_cylinder (object1) in the box.
    # 5. Ensure all objects are in the white_box (object3).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3

    # c) Perform actions
    # Fold the yellow_2D_rectangle
    robot.fold(object0)
    assert object0.folded == True
    
    # Place the red_3D_polyhedron in the box (already in the box)
    assert object2.in_box == True
    
    # Place the yellow_2D_rectangle in the box
    robot.place(object0, box)
    assert object0.in_box == True
    
    # Place the transparent_3D_cylinder in the box
    robot.place(object1, box)
    assert object1.in_box == True
    
    # Ensure all objects are in the white_box
    box.in_bin_objects = [object0.index, object1.index, object2.index]
    assert box.in_bin_objects == [0, 1, 2]

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Folded the yellow_2D_rectangle because it is foldable.
    # - Placed the red_3D_polyhedron first because it is soft.
    # - Placed the yellow_2D_rectangle and transparent_3D_cylinder in the box following the rules.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.folded == False
    assert object2.in_box == True
    assert object2.folded == False
    assert box.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
