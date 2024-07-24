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
    is_heavy: bool
    
    # Object physical properties 
    is_soft: bool
    is_foldable: bool
    is_elastic: bool
    is_fragile: bool
    is_rigid: bool


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
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
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
        if self.robot_handempty and obj.is_foldable and not obj.folded:
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
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

Reason:
The robot actions are designed to follow the given rules for bin packing. The preconditions ensure that actions are only performed when they are logically possible and safe, such as not picking up a box or ensuring a soft object is in the bin before placing a rigid one. The effects update the state of the robot and objects to reflect the changes made by the actions, ensuring consistency in the task planning process. This approach ensures that the robot's actions are both efficient and compliant with the specified rules

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_soft=True, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=True, is_rigid=True
)

object2 = Object(
    index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False,
    is_soft=False, is_foldable=True, is_elastic=False, is_fragile=False, is_rigid=False
)

object3 = Object(
    index=3, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False,
    is_soft=False, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=True
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], in_box=True, is_heavy=False,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=False, is_rigid=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given objects

    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4
    
    # c) Make an action sequence
    # Rule 4: Out the rigid object (green_2D_rectangle) and replace it into the bin
    robot.out(object3, box)
    robot.fold(object2, box)
    robot.place(object2, box)
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Rule 5: Pick, place, and push the soft object (white_3D_cylinder) into the bin
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)
    
    # Rule 2: Place the rigid object (green_3D_cylinder) into the bin after the soft object is in the bin
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: Followed the rules to ensure correct bin packing
    # 1. Never attempted to pick up and set down an object named box
    # 2. Placed the rigid object (green_3D_cylinder) after the soft object (white_3D_cylinder) was in the bin
    # 3. Folded the foldable object (yellow_2D_rectangle) and replaced it into the bin
    # 4. Out the rigid object (green_2D_rectangle) and replaced it into the bin
    # 5. Picked, placed, and pushed the soft object (white_3D_cylinder) into the bin
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object0.pushed == True
    assert object2.folded == True
    print("All task planning is done")
