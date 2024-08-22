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
    is_foldable: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_rigid=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, is_rigid=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, is_rigid=False,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, is_rigid=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }
    
    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (white_2D_loop) in the box first.
    # 2. Place the rigid object (black_3D_cylinder) in the box.
    # 3. Ensure the foldable object (black_2D_loop) remains in the box.
    # 4. Ensure all objects are in the white_box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3

    # c) Action sequence
    # Place the soft object (white_2D_loop) in the box
    robot.pick(object0)
    robot.place(object0, box)
    
    # Place the rigid object (black_3D_cylinder) in the box
    robot.pick(object1)
    robot.place(object1, box)
    
    # Ensure the foldable object (black_2D_loop) remains in the box (already in the box)
    # No action needed for object2 as it is already in the box
    
    # Ensure all objects are in the white_box
    box.in_bin_objects.extend([object0.index, object1.index, object2.index])

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (white_2D_loop) first as per the rule.
    # 2. Placed the rigid object (black_3D_cylinder) after the soft object.
    # 3. The foldable object (black_2D_loop) was already in the box, so no action was needed.
    # 4. Ensured all objects are in the white_box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
