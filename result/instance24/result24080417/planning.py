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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        'object0': {'in_box': False, 'out_box': True, 'is_rigid': True},
        'object1': {'in_box': False, 'out_box': True, 'is_foldable': True},
        'object2': {'in_bin_objects': [], 'in_box': True, 'out_box': False}
    }
    
    goal_state = {
        'object0': {'in_box': True, 'out_box': False, 'is_rigid': True},
        'object1': {'in_box': True, 'out_box': False, 'is_foldable': True},
        'object2': {'in_bin_objects': ['object0', 'object1'], 'in_box': True, 'out_box': False}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object1) since it is foldable.
    # 2. Place the yellow_2D_rectangle (object1) in the white_box (object2).
    # 3. Place the yellow_3D_cylinder (object0) in the white_box (object2).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the objects
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)
    
    # c) Perform actions
    # Fold the yellow_2D_rectangle (object1)
    robot.fold(object1)
    
    # Place the yellow_2D_rectangle (object1) in the white_box (object2)
    robot.pick(object1)
    robot.place(object1, object2)
    
    # Place the yellow_3D_cylinder (object0) in the white_box (object2)
    robot.pick(object0)
    robot.place(object0, object2)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold action is valid because object1 is foldable.
    # 2. Place action for object1 is valid because it is foldable and should be placed before rigid objects.
    # 3. Place action for object0 is valid because it is rigid and follows the placement of the foldable object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [object0, object1]
    
    print("All task planning is done")
