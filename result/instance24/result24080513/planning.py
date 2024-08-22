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
    is_foldable: bool = False
    is_rigid: bool = False
    is_elastic: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the bin for the bin_packing task.
# The 'in_bin_objects' attribute for the box is initialized as None, indicating that no objects are currently in the box.
# The 'pushed' and 'folded' attributes are set to False for all objects, as no actions have been performed yet.
# The 'in_box' and 'out_box' attributes are set according to the initial positions of the objects as specified in the input data.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False, in_bin_objects=[])

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (transparent_2D_circle) in the box first.
    # 2. Place the foldable object (yellow_2D_rectangle) in the box.
    # 3. Place the rigid object (yellow_3D_cylinder) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3

    # c) Action sequence
    # Place the soft object (transparent_2D_circle) in the box
    robot.pick(object1)
    robot.place(object1, box)
    
    # Place the foldable object (yellow_2D_rectangle) in the box
    robot.pick(object0)
    robot.fold(object0)
    robot.place(object0, box)
    
    # Place the rigid object (yellow_3D_cylinder) in the box
    robot.pick(object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (transparent_2D_circle) is placed first as per the rule.
    # 2. The foldable object (yellow_2D_rectangle) is folded and then placed.
    # 3. The rigid object (yellow_3D_cylinder) is placed last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
