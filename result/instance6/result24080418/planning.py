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
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    can_be_packed: bool


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.can_be_packed:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, is_soft=False,
    in_box=False, can_be_packed=True
)

object1 = Object(
    index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_foldable=False, is_soft=False,
    in_box=False, can_be_packed=True
)

object2 = Object(
    index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=False, is_soft=True,
    in_box=True, can_be_packed=True
)

object3 = Object(
    index=3, name='orange_2D_rectangle', color='orange', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, is_soft=False,
    in_box=True, can_be_packed=True
)

object4 = Object(
    index=4, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_foldable=True, is_soft=False,
    in_box=True, can_be_packed=True
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3, object4], is_elastic=False, is_foldable=False, is_soft=False,
    in_box=False, can_be_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the provided code

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold all foldable objects that are not yet folded.
    # 2. Pick and place all objects that are not yet in the box.
    # 3. Push the soft object after placing all other objects in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box

    # Fold all foldable objects that are not yet folded
    robot.fold(object0, box)  # Fold yellow_2D_rectangle
    robot.fold(object3, box)  # Fold orange_2D_rectangle
    robot.fold(object4, box)  # Fold green_2D_rectangle

    # Pick and place all objects that are not yet in the box
    robot.pick(object0, box)  # Pick yellow_2D_rectangle
    robot.place(object0, box)  # Place yellow_2D_rectangle in white_box

    robot.pick(object1, box)  # Pick transparent_3D_cylinder
    robot.place(object1, box)  # Place transparent_3D_cylinder in white_box

    # Push the soft object after placing all other objects in the box
    robot.push(object2, box)  # Push red_3D_polyhedron

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Folded all foldable objects before placing them in the box.
    # - Placed all objects in the box.
    # - Pushed the soft object after placing all other objects in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object0.folded == True
    assert object3.folded == True
    assert object4.folded == True
    assert object2.pushed == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3, object4}

    print("All task planning is done")
