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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The initial state is defined based on the input images.
# Each object has specific properties and predicates that determine its behavior in the bin_packing task.
# The 'white_box' is the only object that starts in the box, while all other objects start out of the box.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', is_soft=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

    # Goal state
    goal_state = {
        object0: True,
        object1: True,
        object2: True,
        object3: True,
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object0) in the box first.
    # 2. Fold the foldable object (object1) and place it in the box.
    # 3. Place the elastic objects (object2 and object3) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(object0, box)
    # 2. Fold the foldable object (object1)
    robot.fold(object1)
    # 3. Place the folded object (object1) in the box
    robot.place(object1, box)
    # 4. Place the elastic object (object2) in the box
    robot.place(object2, box)
    # 5. Place the elastic object (object3) in the box
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed first as per the rule.
    # 2. The foldable object (object1) is folded before placing it in the box.
    # 3. The elastic objects (object2 and object3) are placed in the box after the soft object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    
    print("All task planning is done")
