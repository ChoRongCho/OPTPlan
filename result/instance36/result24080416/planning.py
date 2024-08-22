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
    is_fragile: bool
    is_soft: bool
    is_foldable: bool
    is_elastic: bool
    is_rigid: bool
    
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
        if self.robot_now_holding == obj:
            # Check if there are any soft objects in the bin
            soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
            if obj.is_fragile or obj.is_rigid:
                if soft_objects_in_bin:
                    # Effects
                    self.state_handempty()
                    obj.in_box = True
                    obj.is_packed = True
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot place {obj.name} in {bin.name} without soft objects")
            else:
                # Effects
                self.state_handempty()
                obj.in_box = True
                obj.is_packed = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
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
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_foldable=False,
    is_elastic=False, is_rigid=True, in_box=False, is_packed=False
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_foldable=False,
    is_elastic=False, is_rigid=True, in_box=False, is_packed=False
)

object2 = Object(
    index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_foldable=False,
    is_elastic=True, is_rigid=False, in_box=False, is_packed=False
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_foldable=False,
    is_elastic=True, is_rigid=True, in_box=False, is_packed=False
)

object4 = Object(
    index=4, name='black_3D_cuboid', color='black', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_foldable=True,
    is_elastic=False, is_rigid=False, in_box=False, is_packed=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_foldable=False,
    is_elastic=False, is_rigid=False, in_box=True, is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given table.
    # Final state is described in the goal table.

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (white_3D_cylinder) first.
    # 2. Place the foldable object (black_3D_cuboid) after folding it.
    # 3. Place the fragile object (green_3D_cylinder) after ensuring a soft object is in the box.
    # 4. Place the remaining rigid objects (black_3D_cylinder and white_2D_circle).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    # 1. Place the soft object (white_3D_cylinder)
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.push(object2, box)  # Push the soft object to make space

    # 2. Fold the foldable object (black_3D_cuboid)
    robot.fold(object4, box)
    robot.pick(object4, box)
    robot.place(object4, box)

    # 3. Place the fragile object (green_3D_cylinder)
    robot.pick(object1, box)
    robot.place(object1, box)

    # 4. Place the remaining rigid objects (black_3D_cylinder and white_2D_circle)
    robot.pick(object0, box)
    robot.place(object0, box)

    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # - Placed the soft object first to satisfy the rule for placing fragile and rigid objects.
    # - Folded the foldable object before placing it.
    # - Ensured a soft object was in the box before placing the fragile object.
    # - Placed the remaining rigid objects last.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.pushed == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object4.folded == True
    assert object5.in_bin_objects == [object2, object4, object1, object0, object3]
    print("All task planning is done")
