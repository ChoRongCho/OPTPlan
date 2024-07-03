from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates
    is_rigid: bool = False
    is_flexible: bool = False
    is_elastic: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_packable: bool = True

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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_flexible and not obj.is_rigid and not obj.is_elastic:
            # Effects
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_flexible:
            # Effects
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name}")
    def dummy(self):
        pass


object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_flexible=False, is_elastic=False, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_rigid=False, is_flexible=True, is_elastic=True, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_rigid=False, is_flexible=True, is_elastic=True, is_in_box=True, is_packable=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_flexible=False, is_elastic=False, is_in_box=True, is_packable=False)

if __name__ == '__main__':
    # Initialize the robot
    robot = Robot()

    # Define the bin (white_box)
    bin = object3

    # Plan to pack all objects in the box
    # Step 1: Pick the black_3D_cylinder and place it in the white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 2: Push the blue_1D_ring to make more space in the bin
    robot.push(object1, bin)

    # Step 3: Pick the blue_1D_ring and place it in the white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 4: Out the white_1D_ring from the white_box
    robot.out(object2, bin)

    # Step 5: Push the blue_1D_ring to make more space in the bin
    robot.push(object1, bin)

    # Step 6: Place the white_1D_ring back in the white_box
    robot.place(object2, bin)

    # Final state of each object
    # | Index | Name              | Shape       | Color | Object Type | Is Rigid | Is Flexible | Is Elastic | Is In Box | Is Packable |
    # |-------|-------------------|-------------|-------|-------------|----------|-------------|------------|-----------|-------------|
    # | 0     | black_3D_cylinder | 3D_cylinder | black | obj         | True     | False       | False      | True      | True        |
    # | 1     | blue_1D_ring      | 1D_ring     | blue  | obj         | False    | True        | True       | True      | True        |
    # | 2     | white_1D_ring     | 1D_ring     | white | obj         | False    | True        | True       | True      | True        |
    # | 3     | white_box         | box         | white | box         | False    | False       | False      | True      | False       |

    # Reasons according to the rules:
    # 1. Don't pick and place a box called bin: The robot never picks or places the white_box.
    # 2. When fold an object, the object must be foldable: No folding action is performed.
    # 3. You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object when push an object, neither fragile and rigid objects are permitted: The robot pushes the blue_1D_ring (soft object) to make more space in the bin.

    # Check if the goal state is satisfied using the goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True  # The box itself is always in the box
