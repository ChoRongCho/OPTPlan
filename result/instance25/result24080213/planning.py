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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'is_soft' and 'is_elastic' predicates are set according to the input data.
# The 'in_box' and 'out_box' predicates are set according to the 'init_pose' from the input data.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2], is_soft=False, is_elastic=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place: Before placing a fragile or rigid object, a soft object should be in the box if there is any soft object.
    # 2. Pick: None
    # 3. Fold: Fold objects only if they are foldable.
    # 4. Push: Only push soft objects after placing items in the bin.
    # 5. Out: None

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place the soft object first
    robot.place(object0, box)
    # Place the rigid objects
    robot.place(object1, box)
    robot.place(object2, box)
    # Push the soft object into the box
    robot.push(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object0) first as per the rule before placing any rigid objects.
    # 2. Placed the rigid objects (object1 and object2) after the soft object.
    # 3. Pushed the soft object (object0) into the box after placing all items.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
