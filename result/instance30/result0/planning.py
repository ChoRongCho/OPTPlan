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
    is_foldable: bool = False

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
        if obj.object_type != 'box' and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty and not obj.is_rigid and not obj.is_foldable:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_foldable and self.robot_handempty:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_rigid=False, is_soft=True, is_foldable=False, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', is_rigid=False, is_soft=False, is_foldable=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='black_1D_ring', color='black', shape='1D_ring', object_type='obj', is_rigid=True, is_soft=False, is_foldable=True, is_in_box=True, is_out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_soft=False, is_foldable=False, is_in_box=False, is_out_box=False)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (red_3D_polyhedron): out_box
    # object1 (yellow_2D_rectangle): in_box
    # object2 (black_1D_ring): in_box
    # object3 (white_box): box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. Don't pick and place a box called bin.
    # 2. When fold an object, the object must be foldable.
    # 3. When a rigid object is in the bin at the initial state, take it out and replace it into the bin.
    # 4. You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object. When pushing an object, neither fragile nor rigid objects are permitted.

    # Step-by-step action sequence:
    # 1. Pick out the black_1D_ring (object2) from the box (since it's rigid and already in the box)
    robot.pick_out(object2, object3)

    # 2. Push the red_3D_polyhedron (object0) to make more space in the box
    robot.push(object0, object3)

    # 3. Fold the yellow_2D_rectangle (object1) since it's foldable
    robot.fold(object1, object3)

    # 4. Pick the yellow_2D_rectangle (object1)
    robot.pick(object1, object3)

    # 5. Place the yellow_2D_rectangle (object1) in the box
    robot.place(object1, object3)

    # 6. Pick the black_1D_ring (object2)
    robot.pick(object2, object3)

    # 7. Place the black_1D_ring (object2) back in the box
    robot.place(object2, object3)

    # after making all actions, fill your reasons according to the rules
    # 1. Pick out the black_1D_ring (object2) because it's rigid and already in the box (Rule 3).
    # 2. Push the red_3D_polyhedron (object0) to make more space in the box (Rule 4).
    # 3. Fold the yellow_2D_rectangle (object1) because it's foldable (Rule 2).
    # 4. Pick and place the yellow_2D_rectangle (object1) in the box to achieve the goal state.
    # 5. Pick and place the black_1D_ring (object2) back in the box to achieve the goal state.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == False and object0.is_out_box == True
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == True and object2.is_out_box == False
    assert object3.is_in_box == False and object3.is_out_box == False

    print("Goal state achieved successfully!")
