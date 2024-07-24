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
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_fragile: bool = False


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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != 'box':
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")

Reason:
The robot actions are designed to follow the given rules strictly. The preconditions ensure that actions are only performed when the robot is in the correct state and the objects meet the necessary criteria. For example, the robot cannot pick a box or place an object if it is not holding it. The effects update the state of the robot and objects to reflect the changes caused by the actions. This ensures that the robot's behavior is predictable and consistent with the rules provided

    def dummy(self):
        pass


object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=False, is_foldable=False, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_soft=False, is_elastic=False, is_foldable=True, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_soft=False, is_elastic=True, is_foldable=False, is_in_box=False, is_fragile=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_elastic=False, is_foldable=False, is_in_box=True, is_fragile=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_soft=False, is_elastic=False, is_foldable=False, is_in_box=False, is_fragile=False)

if __name__ == "__main__":
    # Initialize the robot and objects
    robot = Robot()
    bin = object4  # The white box

    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (brown_3D_cuboid) -> in_box
    # object1 (yellow_2D_rectangle) -> out_box
    # object2 (blue_1D_ring) -> in_box
    # object3 (red_3D_polyhedron) -> in_box
    # object4 (white_box) -> box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. You should never pick and place a box.
    # 2. If there is a foldable object, you must fold the object neither it is packed or not.
    # 3. When a rigid object in the bin at the initial state, out of the rigid object and replace it into the bin.
    # 4. You must push a soft object in the bin.

    # Step-by-step action sequence:
    # 1. Fold the yellow_2D_rectangle (object1) since it is foldable.
    robot.fold(object1, bin)

    # 2. Pick out the red_3D_polyhedron (object3) from the bin since it is a rigid object in the bin at the initial state.
    robot.pick_out(object3, bin)

    # 3. Place the red_3D_polyhedron (object3) back into the bin.
    robot.place(object3, bin)

    # 4. Pick the brown_3D_cuboid (object0) and place it in the bin.
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 5. Pick the blue_1D_ring (object2) and place it in the bin.
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # 6. Push the brown_3D_cuboid (object0) in the bin since it is a soft object.
    robot.push(object0, bin)

    # 7. Push the red_3D_polyhedron (object3) in the bin since it is a soft object.
    robot.push(object3, bin)

    # after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Folded the yellow_2D_rectangle (object1) because it is foldable.
    # 2. Picked out and replaced the red_3D_polyhedron (object3) because it is a rigid object in the bin at the initial state.
    # 3. Picked and placed the brown_3D_cuboid (object0) and blue_1D_ring (object2) to achieve the goal state.
    # 4. Pushed the brown_3D_cuboid (object0) and red_3D_polyhedron (object3) because they are soft objects in the bin.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == False

    print("All objects are in their goal states.")
