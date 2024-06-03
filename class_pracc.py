import os
import json


def main():
    base_goal_list = [
        "packing all objects into the bin",
        "Packing all items into the box.",
        "Storing all objects in the container.",
        "Fitting all belongings into the bin",
    ]
    goal_list = [
        "if there is a black object, don't pack it into the box",
        "if there is a elastic object, don't pack it into the box",
        "if there is a yellow object, don't pack it into the box",
        "if there is a rigid object, don't pack it into the box",
        "if there is a 1D object, don't pack it into the box",
        "if there is a red object, don't pack it into the box",
        "if there is a white and soft object, don't pack it into the box",
        "if there are foldable object and soft object together, don't pack a foldable object into the box",
        "if there are yellow object and black object together, don't pack a black object into the box",
        "if there is a fragile object, don't pack it into the box",
    ]

    base_rule = [
        "you should never pick and place a box",
        "don't pick and place a box called bin",
        "it is prohibited to lift and relocate a container",
        "avoid handling and moving any box",
        "never attempt to pick up and set down an object named box",
    ]
    rule_list = [
        "when fold a object, the object must be foldable",
        "when place a rigid objects in the bin, the soft objects must be in the bin before",
        "when fold a foldable object, the fragile object must be in the bin ",
        "before place a elastic object, push a elastic object first",
    ]
    sim_rule1 = [
        "do not place a fragile object if there is no elastic object in the bin",
        "when place a fragile objects, the soft objects must be in the bin",
    ]
    sim_rule2 = [
        "when a rigid object in the bin at the initial state, out of the rigid object and replace it into the bin ",
        "when a soft object in the bin at the initial state, out of the soft object and replace it into the bin ",
    ]
    sim_rule3 = [
        "when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted",
        "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object"
        "when push a object, neither fragile and rigid objects are permitted"
    ]

    # JSON 데이터
    data = {
        "task": "bin_packing",
        "goals": {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
        },
        "rules": {
            "1": "",
            "2": "",
            "3": "",
            "4": ""
        }
    }

    # 루트 폴더 경로
    root_folder = '/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/task_planning'

    # 폴더 생성 및 JSON 파일 저장
    for i in range(1, 31):
        folder_name = f"instance{i}"
        folder_path = os.path.join(root_folder, folder_name)

        # 폴더 생성
        # os.makedirs(folder_path, exist_ok=True)

        # JSON 파일 경로
        json_file_path = os.path.join(folder_path, "instructions.json")

        # JSON 파일 저장
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"폴더 '{folder_name}'에 'data.json' 저장 완료")

    print("모든 JSON 파일 저장 완료")


if __name__ == '__main__':
    main()
