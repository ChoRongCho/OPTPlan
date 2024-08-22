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
    is_elastic: bool
    is_soft: bool
    is_rigid: bool
    is_foldable: bool
    is_fragile: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        if obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.out_box == False:
            # Check if there are any soft objects in the bin
            soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
            if obj.is_fragile or obj.is_rigid:
                if soft_objects_in_bin:
                    # Effects
                    self.state_handempty()
                    obj.in_box = True
                    obj.out_box = False
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot place {obj.name} in {bin.name} without soft objects")
            else:
                # Effects
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and obj.in_box and self.robot_handempty:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_foldable and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_soft=True, 
    is_rigid=False, 
    is_foldable=False, 
    is_fragile=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=True, 
    is_foldable=False, 
    is_fragile=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=False, 
    is_foldable=True, 
    is_fragile=False, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=False, 
    is_foldable=False, 
    is_fragile=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=False, in_box=True, folded=False
    # object3: out_box=False, in_box=False, in_bin_objects=[]

    # Goal State
    # object0: out_box=False, in_box=True
    # object1: out_box=False, in_box=True
    # object2: out_box=False, in_box=True, folded=True
    # object3: out_box=False, in_box=False, in_bin_objects=[object0, object1, object2]

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object2) since it is foldable and already in the box.
    # 2. Pick and place the white_3D_cylinder (object0) into the box.
    # 3. Pick and place the green_3D_cylinder (object1) into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    # 1. Fold the yellow_2D_rectangle (object2)
    robot.fold(object2, box)
    
    # 2. Pick and place the white_3D_cylinder (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 3. Pick and place the green_3D_cylinder (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Fold: Fold objects only if they are foldable.
    # - Place: Before placing a fragile or rigid object, a soft object should be in the box if there are any soft objects.
    # - Pick: No specific preconditions other than the object being out of the box and the robot's hand being empty.
    # - Push: Only push soft objects after placing items in the bin.
    # - Out: No specific preconditions other than the object being in the box and the robot's hand being empty.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object2.folded == True
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
