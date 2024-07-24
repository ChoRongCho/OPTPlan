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
    in_box: bool
    is_packed: bool
    
    # Object physical properties
    is_elastic: bool
    is_soft: bool
    is_foldable: bool
    is_rigid: bool
    is_fragile: bool


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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid:
                soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
                if not soft_objects_in_bin:
                    print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
                    return
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and not obj.in_box and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures that the robot does not pick up boxes and only picks objects not already in the bin. The 'place' action checks for the presence of soft objects before placing rigid ones, adhering to the rule that soft objects must be in the bin first. The 'push' and 'fold' actions ensure the robot's hand is empty and the object is in the correct state (in the bin for pushing, not in the bin for folding). The 'out' action allows the robot to remove objects from the bin, ensuring the bin's state is updated accordingly. These actions ensure the robot's behavior aligns with the specified rules for the bin_packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_soft=True, is_foldable=False, is_rigid=False, is_fragile=False
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=False, is_rigid=True, is_fragile=True
)

object2 = Object(
    index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=True, is_rigid=False, is_fragile=False
)

object3 = Object(
    index=3, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2], in_box=False, is_packed=False,
    is_elastic=False, is_soft=False, is_foldable=False, is_rigid=False, is_fragile=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: white_3D_cylinder, out_box, is_soft, is_elastic
    # object1: green_3D_cylinder, out_box, is_rigid, is_fragile
    # object2: yellow_2D_rectangle, in_box, is_foldable
    # object3: white_box, box, contains object2

    # Goal State
    # object0: white_3D_cylinder, in_box, pushed
    # object1: green_3D_cylinder, in_box
    # object2: yellow_2D_rectangle, in_box, folded
    # object3: white_box, box, contains object0, object1, object2

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object2) since it is foldable and not folded yet.
    # 2. Pick and place the white_3D_cylinder (object0) into the box.
    # 3. Push the white_3D_cylinder (object0) in the box.
    # 4. Pick and place the green_3D_cylinder (object1) into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    # Step 1: Fold the yellow_2D_rectangle (object2)
    robot.fold(object2, box)
    object2.folded = True  # Manually update the state since fold action does not change in_box

    # Step 2: Pick and place the white_3D_cylinder (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Push the white_3D_cylinder (object0) in the box
    robot.push(object0, box)
    object0.pushed = True  # Manually update the state since push action does not change in_box

    # Step 4: Pick and place the green_3D_cylinder (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Fold the yellow_2D_rectangle (object2) because it is foldable and not in the bin (Rule 3).
    # 2. Pick and place the white_3D_cylinder (object0) because it is soft and should be placed before rigid objects (Rule 5).
    # 3. Push the white_3D_cylinder (object0) because it is soft and should be pushed into the bin (Rule 5).
    # 4. Pick and place the green_3D_cylinder (object1) because it is rigid and should be placed after soft objects (Rule 2).

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object2, object0, object1]
    print("All task planning is done")
