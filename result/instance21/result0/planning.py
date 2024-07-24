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
    is_soft: bool = False
    is_elastic: bool = False
    is_fragile: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = True


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
    
    def pick(self, obj, bin):
        # Preconditions
        if obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty:
            # Effects
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")
            self.state_handempty()

    def dummy(self):
        pass


object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=False, is_out_box=True)
object3 = Object(index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # | Index | Name              | Shape       | Color  | Type | is_rigid | is_soft | is_elastic | is_fragile | is_in_box | is_out_box |
    # |-------|-------------------|-------------|--------|------|----------|---------|------------|------------|-----------|------------|
    # | 0     | brown_3D_cuboid   | 3D_cuboid   | brown  | obj  | False    | True    | False      | False      | True      | False      |
    # | 1     | white_3D_cylinder | 3D_cylinder | white  | obj  | False    | True    | True       | False      | True      | False      |
    # | 2     | green_3D_cylinder | 3D_cylinder | green  | obj  | True     | False   | False      | True       | True      | False      |
    # | 3     | yellow_3D_cylinder| 3D_cylinder | yellow | obj  | True     | False   | False      | False      | True      | False      |
    # | 4     | white_box         | box         | white  | box  | False    | False   | False      | False      | True      | False      |

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    robot = Robot()
    bin = object4  # The box where objects will be placed

    # Step 1: Push the brown_3D_cuboid (soft object) into the box
    robot.push(object0, bin)

    # Step 2: Push the white_3D_cylinder (soft and elastic object) into the box
    robot.push(object1, bin)

    # Step 3: Pick and place the green_3D_cylinder (rigid and fragile object) into the box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Step 4: The yellow_3D_cylinder is already in the box, no action needed

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. It is prohibited to lift and relocate a container: We did not move the box.
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before: The brown_3D_cuboid and white_3D_cylinder (soft objects) were placed before the green_3D_cylinder (rigid object).
    # 3. Do not place a fragile object if there is no elastic object in the bin: The white_3D_cylinder (elastic object) was placed before the green_3D_cylinder (fragile object).
    # 4. When pushing an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted: Only soft objects (brown_3D_cuboid and white_3D_cylinder) were pushed.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box and not object0.is_out_box
    assert object1.is_in_box and not object1.is_out_box
    assert object2.is_in_box and not object2.is_out_box
    assert object3.is_in_box and not object3.is_out_box
    assert object4.is_in_box and not object4.is_out_box

    print("All objects are correctly placed in the box according to the goal state.")
