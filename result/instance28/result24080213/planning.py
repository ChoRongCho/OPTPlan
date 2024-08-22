from dataclasses import dataclass, field

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
    in_bin_objects: list = field(default_factory=list)
    
    # Object physical properties 
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_elastic=True, is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_box=False, out_box=False)

### 3. Notes:
# The initial state table provides a clear overview of the objects and their properties.
# The Python code initializes the objects with their respective properties and initial states.
# The 'object_type' field differentiates between regular objects and the box.
# The 'in_box' and 'out_box' fields are used to track the position of the objects relative to the box.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_elastic=True, is_foldable=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_box=False, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object0) in the box first.
    # 2. Fold the foldable object (object1) if necessary.
    # 3. Place the foldable object (object1) in the box.
    # 4. Ensure the rigid object (object2) is already in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(object0, box)
    # 2. Fold the foldable object (object1)
    robot.fold(object1)
    # 3. Place the foldable object (object1) in the box
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The soft object (object0) is placed in the box first to satisfy the rule that soft objects should be placed before rigid objects.
    # - The foldable object (object1) is folded before placing it in the box to satisfy the rule that foldable objects should be folded if they are foldable.
    # - The rigid object (object2) is already in the box, so no action is needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True

    print("All task planning is done")