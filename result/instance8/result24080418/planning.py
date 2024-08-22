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
    is_foldable: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        if obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.out_box:
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_elastic and obj.in_box and self.robot_handempty:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_foldable and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_foldable=False, is_elastic=True,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_foldable=False, is_elastic=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_foldable=True, is_elastic=True,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_foldable=True, is_elastic=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_foldable=True, is_elastic=False,
    in_box=True, out_box=False
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_foldable=False, is_elastic=False,
    in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given table.
    # Final state:
    # object0: in_box=True, out_box=False
    # object1: in_box=True, out_box=False
    # object2: in_box=True, out_box=False, folded=True
    # object3: in_box=True, out_box=False, folded=True
    # object4: in_box=True, out_box=False, folded=True
    # white_box: in_bin_objects=[object0, object1, object2, object3, object4]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold all foldable objects that are not already in the box.
    # 2. Place all soft objects in the box.
    # 3. Place all rigid objects in the box.
    # 4. Push soft objects if necessary.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box

    # Fold foldable objects
    robot.fold(object2, box)  # Fold blue_1D_linear
    robot.fold(object3, box)  # Fold yellow_2D_rectangle
    robot.fold(object4, box)  # Fold green_2D_rectangle

    # Place soft objects in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.pick(object0, box)
    robot.place(object0, box)

    # Place rigid objects in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Push soft objects if necessary
    robot.push(object0, box)
    robot.push(object2, box)

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_box == True
    assert object3.folded == True
    assert object4.in_box == True
    assert object4.folded == True
    assert white_box.in_bin_objects == [object2, object0, object1]

    print("All task planning is done")
