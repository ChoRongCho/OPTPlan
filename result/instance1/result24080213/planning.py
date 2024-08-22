from dataclasses import dataclass, field

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
    in_bin_objects: list = field(default_factory=list)
    
    # Object physical properties 
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_2D_circle', 
    color='black', 
    shape='2D_circle', 
    object_type='obj', 
    is_foldable=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='blue_2D_loop', 
    color='blue', 
    shape='2D_loop', 
    object_type='obj', 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box=True, 
    out_box=False
)

from dataclasses import dataclass, field

@dataclass
class Object:
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    pushed: bool = False
    folded: bool = False
    in_bin_objects: list = field(default_factory=list)
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    in_box: bool = False
    out_box: bool = True

class Robot:
    def place(self, obj, box):
        if obj.is_soft or obj.in_box:
            obj.in_box = True
            obj.out_box = False
            box.in_bin_objects.append(obj)
        else:
            raise Exception("Cannot place a rigid or fragile object before a soft object is placed.")

    def pick(self, obj):
        obj.in_box = False
        obj.out_box = True

    def fold(self, obj):
        if obj.is_foldable:
            obj.folded = True
        else:
            raise Exception("Cannot fold a non-foldable object.")

    def push(self, obj):
        if obj.is_soft:
            obj.pushed = True
        else:
            raise Exception("Cannot push a non-soft object.")

    def out(self, obj):
        obj.in_box = False
        obj.out_box = True

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(
        index=0, 
        name='brown_3D_cuboid', 
        color='brown', 
        shape='3D_cuboid', 
        object_type='obj', 
        is_soft=True, 
        is_elastic=True, 
        in_box=False, 
        out_box=True
    )

    object1 = Object(
        index=1, 
        name='black_2D_circle', 
        color='black', 
        shape='2D_circle', 
        object_type='obj', 
        is_foldable=True, 
        in_box=False, 
        out_box=True
    )

    object2 = Object(
        index=2, 
        name='blue_2D_loop', 
        color='blue', 
        shape='2D_loop', 
        object_type='obj', 
        in_box=False, 
        out_box=True
    )

    object3 = Object(
        index=3, 
        name='white_box', 
        color='white', 
        shape='box', 
        object_type='box', 
        in_box=True, 
        out_box=False
    )

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place the soft object (object0) in the box first.
    # 2. Fold the foldable object (object1).
    # 3. Place the folded object (object1) in the box.
    # 4. Place the remaining object (object2) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.place(object0, box)  # Place the soft object first
    robot.fold(object1)        # Fold the foldable object
    robot.place(object1, box)  # Place the folded object
    robot.place(object2, box)  # Place the remaining object

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed first to satisfy the rule that soft objects should be placed before rigid or fragile objects.
    # 2. The foldable object (object1) is folded before placing it in the box.
    # 3. The remaining object (object2) is placed in the box after the soft object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    
    print("All task planning is done")
