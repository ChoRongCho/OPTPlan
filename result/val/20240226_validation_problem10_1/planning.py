from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    location: tuple
    size: tuple
    color: str or bool
    object_type: str

    # Object physical properties predicates
    is_foldable: bool = False
    is_rigid: bool = False
    is_elastic: bool = False

    # bin_packing Predicates (max 4)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False

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
        self.robot_now_holding = False
        self.robot_base_pose = True

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False

    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    # bin_packing
    def pick(self, obj):
        if obj.in_bin or obj.object_type == 'box':
            print(f"Cannot pick a {obj.name} in the bin or a box.")
        else:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_bin = True
            obj.in_bin = False

    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj or obj.object_type == 'box':
            print(f"Cannot place a {obj.name} not in hand or a box.")
        else:
            print(f"Place {obj.name} in {bins.name}")
            self.state_handempty()
            obj.in_bin = True
            obj.out_bin = False

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or obj.is_rigid:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is rigid.")
        else:
            print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty or not obj.is_foldable:
            print(f"Cannot fold a {obj.name} when hand is not empty or the object is not foldable.")
        else:
            print(f"Fold {obj.name}")

    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True


# Object 1
bin1 = Object(
    index=0,
    name='white box',
    location=(513, 200),
    size=(240, 343),
    color='white',
    object_type='box',
    is_elastic=True,
    in_bin=True
)

# Object 2
object1 = Object(
    index=1,
    name='red object',
    location=(115, 239),
    size=(66, 61),
    color='red',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

# Object 3
object2 = Object(
    index=2,
    name='yellow object',
    location=(485, 194),
    size=(143, 228),
    color='yellow',
    object_type='object',
    is_rigid=True,
    is_foldable=True,
    in_bin=True
)

# Object 4
object3 = Object(
    index=3,
    name='blue object',
    location=(83, 218),
    size=(138, 295),
    color='blue',
    object_type='object',
    is_rigid=True,
    out_bin=True
)

# Object 5
object4 = Object(
    index=4,
    name='black object',
    location=(259, 190),
    size=(94, 156),
    color='black',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

if __name__ == '__main__':
    """
    bin 
    elastic but we don't have to consider this predicates.

    objects
    1 foldable objects: object2
    2 rigid objects: object2, object3
    2 elastic objects: object1, object4
    
    objects in the bin: object2
    objects out the bin: object1, object3, object4

    Available action
    object1: [elastic, out_bin]: pick, place
    object2: [rigid, foldable, in_bin]: out, place, fold
    object3: [rigid, out_bin]: pick, place
    object4: [elastic, out_bin]: pick, place
    
    Goal: packing all objects in the bin: make all objects state to in_bin = True
    """
    # Initialize robot
    robot = Robot()

    # Pick and place object1 in the bin
    robot.pick(object1)
    robot.place(object1, bin1)

    # Pick and place object3 in the bin
    robot.pick(object3)
    robot.place(object3, bin1)

    # Pick and place object4 in the bin
    robot.pick(object4)
    robot.place(object4, bin1)

    # Fold object2 and place it in the bin
    robot.fold(object2)

