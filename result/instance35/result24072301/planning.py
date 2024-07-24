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
    is_elastic: bool
    is_rigid: bool
    is_soft: bool
    
    # Object physical properties
    init_pose: str
    in_box: bool


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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, object must not be a box
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be soft
        if self.robot_handempty and obj.is_soft:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_elastic:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_rigid=False, is_soft=True,
    init_pose='out_box', in_box=False
)

object1 = Object(
    index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_rigid=False, is_soft=True,
    init_pose='out_box', in_box=False
)

object2 = Object(
    index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_rigid=True, is_soft=False,
    init_pose='in_box', in_box=True
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_rigid=False, is_soft=False,
    init_pose='in_box', in_box=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], is_elastic=False, is_rigid=False, is_soft=False,
    init_pose='box', in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given data

    # Second, using given rules and object's states, make a task planning strategy
    # We need to place all objects (yellow_3D_cuboid, red_3D_polyhedron, black_2D_ring, white_2D_ring) into the white_box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Make an action sequence
    # 1. Out black_2D_ring and white_2D_ring from the box
    robot.out(object2, box)
    robot.out(object3, box)

    # 2. Pick and place yellow_3D_cuboid into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # 3. Pick and place red_3D_polyhedron into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # 4. Place black_2D_ring back into the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # 5. Place white_2D_ring back into the box
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - We cannot pick and place a box (Rule 1)
    # - We did not fold any object (Rule 2)
    # - We did not push any object (Rule 4)
    # - We ensured that the fragile object (black_2D_ring) was handled properly

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object0, object1, object2, object3]
    print("All task planning is done")
