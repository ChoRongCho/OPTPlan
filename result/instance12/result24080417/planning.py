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
    is_fragile: bool = False
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
object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_fragile=True, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The 'in_bin_objects' attribute is set to None for both objects as there is no information provided about objects inside the box.
# The 'pushed' and 'folded' attributes are set to False by default as there is no information provided about these states.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_fragile=True, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False, in_bin_objects=[])

    # Goal state
    goal_object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_fragile=True, is_rigid=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False, in_bin_objects=[goal_object0])

    # Second, using given rules and object's states, make a task planning strategy
    # According to the rules, we need to place the green_3D_cylinder into the white_box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object1

    # c) Action sequence
    # 1. Pick the green_3D_cylinder
    robot.pick(object0)
    # 2. Place the green_3D_cylinder into the white_box
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: The green_3D_cylinder is a rigid and fragile object, and there are no soft objects to place first. Therefore, we can directly place it into the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object1.in_bin_objects == [object0]
    
    print("All task planning is done")
