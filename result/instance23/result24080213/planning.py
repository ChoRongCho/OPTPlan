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
    is_fragile: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_rigid=False, in_box=False, out_box=True)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects in the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'in_box' and 'out_box' predicates are mutually exclusive and set according to the initial positions of the objects.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_rigid=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_rigid=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_rigid=False, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_rigid=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1], is_soft=False, is_fragile=False, is_rigid=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # According to the rules:
    # 1. Place the soft object (object0) in the box first.
    # 2. Then place the fragile and rigid object (object1) in the box.
    # 3. Finally, update the box's in_bin_objects list to include both objects.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Place the soft object (object0) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # Place the fragile and rigid object (object1) in the box
    robot.pick(object1)
    robot.place(object1, box)

    # Update the box's in_bin_objects list
    box.in_bin_objects.append(object0.index)
    box.in_bin_objects.append(object1.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed in the box first to satisfy the rule that soft objects should be placed before fragile or rigid objects.
    # 2. The fragile and rigid object (object1) is placed in the box after the soft object.
    # 3. The box's in_bin_objects list is updated to reflect the objects inside it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [0, 1]

    print("All task planning is done")
