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
    is_soft: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    is_foldable=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    is_rigid=True, 
    is_fragile=True, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_bin_objects=[], 
    in_box=False, 
    out_box=False
)

from dataclasses import dataclass

@dataclass
class Object:
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    pushed: bool = False
    folded: bool = False
    in_bin_objects: list = None
    is_foldable: bool = False
    is_soft: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    in_box: bool = False
    out_box: bool = True

class Robot:
    def pick(self, obj: Object):
        if obj.out_box:
            obj.out_box = False
            print(f"Picked {obj.name}")
        else:
            print(f"Cannot pick {obj.name}, already in box")

    def place(self, obj: Object, box: Object):
        if obj.out_box == False and obj.in_box == False:
            obj.in_box = True
            box.in_bin_objects.append(obj)
            print(f"Placed {obj.name} in {box.name}")
        else:
            print(f"Cannot place {obj.name}, already in box or not picked")

    def fold(self, obj: Object):
        if obj.is_foldable and not obj.folded:
            obj.folded = True
            print(f"Folded {obj.name}")
        else:
            print(f"Cannot fold {obj.name}, not foldable or already folded")

    def push(self, obj: Object):
        if obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Pushed {obj.name}")
        else:
            print(f"Cannot push {obj.name}, not soft or not in box")

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(
        index=0, 
        name='yellow_2D_rectangle', 
        color='yellow', 
        shape='2D_rectangle', 
        object_type='obj', 
        is_foldable=True, 
        in_box=False, 
        out_box=True
    )

    object1 = Object(
        index=1, 
        name='red_3D_polyhedron', 
        color='red', 
        shape='3D_polyhedron', 
        object_type='obj', 
        is_soft=True, 
        in_box=False, 
        out_box=True
    )

    object2 = Object(
        index=2, 
        name='black_2D_loop', 
        color='black', 
        shape='2D_loop', 
        object_type='obj', 
        is_rigid=True, 
        is_fragile=True, 
        in_box=True, 
        out_box=False
    )

    object3 = Object(
        index=3, 
        name='white_box', 
        color='white', 
        shape='box', 
        object_type='box', 
        in_bin_objects=[], 
        in_box=False, 
        out_box=False
    )

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the red_3D_polyhedron (soft object) into the box first.
    # 2. Pick and fold the yellow_2D_rectangle (foldable object).
    # 3. Place the folded yellow_2D_rectangle into the box.
    # 4. Ensure the black_2D_loop (already in the box) remains in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object1)  # Pick red_3D_polyhedron
    robot.place(object1, box)  # Place red_3D_polyhedron in the box

    robot.pick(object0)  # Pick yellow_2D_rectangle
    robot.fold(object0)  # Fold yellow_2D_rectangle
    robot.place(object0, box)  # Place yellow_2D_rectangle in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (red_3D_polyhedron) first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # 2. Folded the foldable object (yellow_2D_rectangle) before placing it in the box.
    # 3. Ensured that the black_2D_loop (already in the box) remains in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
