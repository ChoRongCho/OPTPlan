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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and bin for the bin_packing task.
# The 'in_bin_objects' list is empty for all objects initially, indicating no objects are inside any bin.
# The 'pushed' and 'folded' properties are set to False for all objects initially.
# The 'in_box' and 'out_box' properties are mutually exclusive and indicate the initial position of the objects.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1], is_rigid=False, is_fragile=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # - Place the soft object (if any) first
    # - Place the rigid and fragile objects next
    # - Push the soft object after placing items in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Place the yellow_3D_cylinder (rigid, non-fragile) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # Place the black_2D_loop (rigid, fragile) in the box
    robot.pick(object1)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - The yellow_3D_cylinder is rigid and non-fragile, so it can be placed directly.
    # - The black_2D_loop is rigid and fragile, and it can be placed after the yellow_3D_cylinder.
    # - The white_box is already in the box, so no action is needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [0, 1]

    print("All task planning is done")
