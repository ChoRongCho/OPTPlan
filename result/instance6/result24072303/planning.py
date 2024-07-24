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
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_in_box: bool
    is_out_box: bool
    
    # Object physical properties
    is_elastic: bool
    is_soft: bool
    is_foldable: bool


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
        self.robot_now_holding = None
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
        if self.robot_handempty and obj.is_out_box:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_soft or all(o.is_soft for o in bin.in_bin_objects):
                # Effects
                self.state_handempty()
                obj.is_in_box = True
                obj.is_out_box = False
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} in {bin.name} due to rule 2")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable and obj.is_out_box:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_elastic=False, is_soft=False, is_foldable=True
)

object1 = Object(
    index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=False, is_out_box=True,
    is_elastic=True, is_soft=False, is_foldable=False
)

object2 = Object(
    index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_out_box=False,
    is_elastic=False, is_soft=True, is_foldable=False
)

object3 = Object(
    index=3, name='orange_2D_rectangle', color='orange', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_out_box=False,
    is_elastic=False, is_soft=False, is_foldable=True
)

object4 = Object(
    index=4, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_in_box=True, is_out_box=False,
    is_elastic=True, is_soft=False, is_foldable=True
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3, object4], is_in_box=False, is_out_box=False,
    is_elastic=False, is_soft=False, is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given data

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. It is prohibited to lift and relocate a container.
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before.
    # 4. If there is a foldable object, fold the object on the platform not in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Fold yellow_2D_rectangle
    robot.fold(object0, box)
    # Place yellow_2D_rectangle in the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fold orange_2D_rectangle
    robot.out(object3, box)
    robot.fold(object3, box)
    # Place orange_2D_rectangle in the box
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fold green_2D_rectangle
    robot.out(object4, box)
    robot.fold(object4, box)
    # Place green_2D_rectangle in the box
    robot.pick(object4, box)
    robot.place(object4, box)

    # Place transparent_3D_cylinder in the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Foldable objects (yellow_2D_rectangle, orange_2D_rectangle, green_2D_rectangle) are folded on the platform.
    # - Soft object (red_3D_polyhedron) is already in the box.
    # - Rigid object (transparent_3D_cylinder) is placed in the box after the soft object.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    assert object0.folded == True
    assert object3.folded == True
    assert object4.folded == True
    print("All task planning is done")
