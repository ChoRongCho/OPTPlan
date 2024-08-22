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
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_foldable=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[0, 1, 2], in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object2) in the box first.
    # 2. Fold the foldable object (object1).
    # 3. Place the foldable object (object1) in the box.
    # 4. Place the rigid object (object0) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform actions
    # Place the soft object (object2) in the box
    robot.place(object2, box)
    # Fold the foldable object (object1)
    robot.fold(object1)
    # Place the foldable object (object1) in the box
    robot.place(object1, box)
    # Place the rigid object (object0) in the box
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object2) is placed in the box first to satisfy the rule that soft objects should be placed before rigid objects.
    # 2. The foldable object (object1) is folded before placing it in the box to satisfy the rule that foldable objects should be folded.
    # 3. The rigid object (object0) is placed in the box last to satisfy the rule that soft objects should be placed before rigid objects.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
