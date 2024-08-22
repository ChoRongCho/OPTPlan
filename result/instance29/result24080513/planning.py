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
    is_fragile: bool
    is_soft: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'red_3D_polyhedron', 'in_box': False, 'out_box': True, 'is_soft': True, 'is_fragile': False},
        1: {'name': 'black_2D_loop', 'in_box': False, 'out_box': True, 'is_soft': False, 'is_fragile': True},
        2: {'name': 'white_2D_circle', 'in_box': False, 'out_box': True, 'is_soft': False, 'is_fragile': True},
        3: {'name': 'white_box', 'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }

    goal_state = {
        0: {'name': 'red_3D_polyhedron', 'in_box': True, 'out_box': False},
        1: {'name': 'black_2D_loop', 'in_box': True, 'out_box': False},
        2: {'name': 'white_2D_circle', 'in_box': True, 'out_box': False},
        3: {'name': 'white_box', 'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (red_3D_polyhedron) in the box first.
    # 2. Place the fragile objects (black_2D_loop and white_2D_circle) in the box.
    # 3. Ensure all objects are in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    # 1. Place the soft object (red_3D_polyhedron) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    # 2. Place the fragile object (black_2D_loop) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    # 3. Place the fragile object (white_2D_circle) in the box
    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False
    box.in_bin_objects.append(object2.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The soft object (red_3D_polyhedron) was placed first as per the rule.
    # - The fragile objects (black_2D_loop and white_2D_circle) were placed after the soft object.
    # - All objects are now in the box, satisfying the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
