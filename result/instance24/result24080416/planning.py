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
    is_foldable: bool
    is_rigid: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.is_rigid:
            # Check if there are any soft objects in the bin
            soft_objects_in_bin = any(o.is_elastic for o in bin.in_bin_objects)
            if soft_objects_in_bin:
                print(f"Cannot Place {obj.name} because soft objects are in the bin")
                return
        
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_elastic and obj.in_box:
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
    index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_elastic=True,
    in_box=False, is_packed=False
)

object1 = Object(
    index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_rigid=False, is_elastic=True,
    in_box=False, is_packed=False
)

object2 = Object(
    index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=True, is_elastic=False,
    in_box=False, is_packed=False
)

object3 = Object(
    index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_rigid=False, is_elastic=False,
    in_box=False, is_packed=False
)

object4 = Object(
    index=4, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_elastic=True,
    in_box=False, is_packed=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_rigid=False, is_elastic=False,
    in_box=True, is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_box,
        object5.name: object5.in_box,
    }
    
    # Final state
    final_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        object4.name: True,
        object5.name: True,
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place all soft objects first (black_3D_cuboid, white_3D_cuboid, transparent_2D_circle)
    # 2. Fold foldable objects (white_3D_cuboid, yellow_2D_rectangle)
    # 3. Pick and place rigid objects (yellow_3D_cylinder)
    # 4. Push soft objects if needed (black_3D_cuboid, white_3D_cuboid, transparent_2D_circle)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5
    
    # Action sequence
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object1, box)
    robot.fold(object1, box)
    robot.place(object1, box)
    
    robot.pick(object4, box)
    robot.place(object4, box)
    
    robot.pick(object3, box)
    robot.fold(object3, box)
    robot.place(object3, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place soft objects first to ensure they are in the box before placing rigid objects.
    # 2. Fold foldable objects before placing them to save space.
    # 3. Place rigid objects after ensuring all soft objects are in the box.
    # 4. Push soft objects if needed after placing all items in the bin.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_box == True
    
    assert object1.folded == True
    assert object3.folded == True
    
    print("All task planning is done")
