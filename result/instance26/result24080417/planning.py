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
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=False, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'object_type' is set to 'obj' for all objects except the box, which is set to 'box'.
# The 'in_box' and 'out_box' predicates are mutually exclusive for each object.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

    # Goal state
    goal_object0_in_box = True
    goal_object1_in_box = True
    goal_object2_in_box = True
    goal_object3_in_bin_objects = [0, 1, 2]

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

    # Action sequence
    # 1. Place the red_3D_polyhedron (soft object) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    # 2. Place the yellow_3D_cuboid (already in the box, no action needed)
    # 3. Place the transparent_3D_cylinder (rigid object) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the red_3D_polyhedron first because it is a soft object.
    # - The yellow_3D_cuboid is already in the box.
    # - Placed the transparent_3D_cylinder after the soft objects were in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert box.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
