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
    is_rigid: bool
    is_fragile: bool
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
object0 = Object(
    index=0, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=True, 
    is_elastic=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='transparent_3D_cuboid', 
    color='transparent', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_fragile=True, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=False, 
    out_box=True
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
    is_rigid=False, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=True, 
    out_box=False
)

### 3. Notes:
# The initial state is defined based on the given input images.
# Each object has been assigned properties and initial states as per the provided data.
# The 'object_type' field differentiates between 'box' and 'obj'.
# The 'in_bin_objects' list is empty initially for all objects.
# The 'pushed' and 'folded' predicates are set to False initially for all objects.
# The 'in_box' and 'out_box' predicates are set based on the 'init_pose' field from the input data.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    object0 = Object(
        index=0, 
        name='green_3D_cylinder', 
        color='green', 
        shape='3D_cylinder', 
        object_type='obj', 
        pushed=False, 
        folded=False, 
        in_bin_objects=[], 
        is_rigid=True, 
        is_fragile=True, 
        is_elastic=False, 
        in_box=False, 
        out_box=True
    )

    object1 = Object(
        index=1, 
        name='transparent_3D_cuboid', 
        color='transparent', 
        shape='3D_cuboid', 
        object_type='obj', 
        pushed=False, 
        folded=False, 
        in_bin_objects=[], 
        is_rigid=False, 
        is_fragile=True, 
        is_elastic=True, 
        in_box=False, 
        out_box=True
    )

    object2 = Object(
        index=2, 
        name='white_2D_circle', 
        color='white', 
        shape='2D_circle', 
        object_type='obj', 
        pushed=False, 
        folded=False, 
        in_bin_objects=[], 
        is_rigid=True, 
        is_fragile=False, 
        is_elastic=False, 
        in_box=False, 
        out_box=True
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
        is_rigid=False, 
        is_fragile=False, 
        is_elastic=False, 
        in_box=True, 
        out_box=False
    )

    # Goal State
    goal_state = {
        0: True,  # green_3D_cylinder in_box
        1: True,  # transparent_3D_cuboid in_box
        2: True,  # white_2D_circle in_box
        3: True   # white_box in_box
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (transparent_3D_cuboid) first.
    # 2. Place the rigid and fragile object (green_3D_cylinder) next.
    # 3. Place the rigid object (white_2D_circle) last.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place transparent_3D_cuboid (soft object) first
    robot.pick(object1)
    robot.place(object1, box)

    # Place green_3D_cylinder (rigid and fragile object) next
    robot.pick(object0)
    robot.place(object0, box)

    # Place white_2D_circle (rigid object) last
    robot.pick(object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (transparent_3D_cuboid) first as per the rule.
    # 2. Placed the rigid and fragile object (green_3D_cylinder) after the soft object.
    # 3. Placed the rigid object (white_2D_circle) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True  # The box itself should be in_box

    print("All task planning is done")
