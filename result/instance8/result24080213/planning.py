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
    is_elastic: bool
    is_foldable: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, in_box=False, out_box=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': False, 'out_box': True},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False}
    }
    
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before rigid or fragile objects.
    # 2. Fold objects only if they are foldable.
    # 3. Push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # c) Action sequence
    # 1. Place the soft object (transparent_3D_cylinder) first
    robot.place(object0, box)
    
    # 2. Fold the foldable objects (black_2D_circle and yellow_2D_rectangle)
    robot.fold(object1)
    robot.fold(object3)
    
    # 3. Place the foldable objects (black_2D_circle and yellow_2D_rectangle)
    robot.place(object1, box)
    robot.place(object3, box)
    
    # 4. Place the rigid object (blue_2D_loop)
    robot.place(object2, box)
    
    # 5. Push the soft object (transparent_3D_cylinder) into the box
    robot.push(object0, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (transparent_3D_cylinder) first as per the rule.
    # - Folded the foldable objects (black_2D_circle and yellow_2D_rectangle) before placing them.
    # - Placed the rigid object (blue_2D_loop) after the soft and foldable objects.
    # - Pushed the soft object (transparent_3D_cylinder) into the box after placing all items.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
