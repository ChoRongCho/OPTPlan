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
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty and not obj.is_rigid and not obj.is_elastic:
            # Effects
            obj.is_in_box = True
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable:
            # Effects
            obj.is_packable = False
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=False, is_packable=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_packable=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, is_in_box=False, is_packable=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_packable=False)

if __name__ == '__main__':
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal: 
    # object0 (red_3D_polyhedron) -> in_box
    # object1 (black_3D_cylinder) -> out_box
    # object2 (white_3D_cylinder) -> in_box
    # object3 (white_box) -> box (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. Never attempt to pick up and set down an object named box.
    # 2. When fold a foldable object, the fragile object must be in the bin.
    # 3. Do not place a fragile object if there is no elastic object in the bin.
    # 4. You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object when push an object, neither fragile and rigid objects are permitted.

    # Step-by-step action sequence:
    # 1. Push the red_3D_polyhedron (soft object) into the box to make space.
    robot.push(object0, object3)

    # 2. Pick the white_3D_cylinder (soft and elastic) and place it in the box.
    robot.pick(object2, object3)
    robot.place(object2, object3)

    # 3. Pick the red_3D_polyhedron (soft object) and place it in the box.
    robot.pick(object0, object3)
    robot.place(object0, object3)

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Pushed the red_3D_polyhedron first to make space in the box as it is soft.
    # - Picked and placed the white_3D_cylinder next because it is soft and elastic, and it needs to be in the box before placing any fragile objects.
    # - Finally, picked and placed the red_3D_polyhedron in the box.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True, "red_3D_polyhedron should be in the box"
    assert object1.is_in_box == False, "black_3D_cylinder should be out of the box"
    assert object2.is_in_box == True, "white_3D_cylinder should be in the box"
    assert object3.is_in_box == True, "white_box should be in the box"

    print("All objects are in their goal states.")
