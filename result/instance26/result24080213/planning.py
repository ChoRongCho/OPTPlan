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
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

### 3. Notes:
# The initial state is defined based on the given input images.
# The 'in_bin_objects' list for the box is initialized as an empty list.
# The 'is_rigid' and 'is_elastic' properties are set based on the predicates provided.
# The 'in_box' and 'out_box' properties are set according to the 'init_pose' values.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', is_rigid=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_rigid=True, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[0, 1, 2], in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # According to the rules:
    # 1. Place soft objects first if there are any.
    # 2. Then place rigid objects.
    # 3. Fold objects only if they are foldable.
    # 4. Push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place the soft object first
    robot.pick(object1)
    robot.place(object1, box)
    
    # Place the rigid objects
    robot.pick(object0)
    robot.place(object0, box)
    
    robot.pick(object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The transparent_3D_cylinder (soft object) is placed first in the box.
    # 2. The red_3D_cuboid and white_2D_circle (rigid objects) are placed after the soft object.
    # 3. No objects are foldable, so no folding actions are needed.
    # 4. No pushing actions are needed as all objects are placed directly in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
