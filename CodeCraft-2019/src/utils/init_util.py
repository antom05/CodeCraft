from ..abstracts import *


def create_object_from_file(path, class_name, global_exit_queue):
    """
    从文件中读取数据并创建相应对象

    @param path: str 文件路径
    @param class_name: str 类名，取值Car、Cross、Road
    @param global_exit_queue: dict 存储某tick所有从道路中出来的车辆
    @return: dict，id to 对象
    """
    id_2_objects = {}
    target_class = eval(class_name)
    with open(path, 'r') as f:
        next(f)
        for line in f:
            args = [int(ch) for ch in line.strip("()\n").split(",")]
            if class_name == 'Road':
                args.append(global_exit_queue)
            id_2_objects[args[0]] = target_class(*args)
    return id_2_objects


def build_objects_from_files(car_path, road_path, cross_path):
    # to read input file
    global_exit_queue = {}
    id_2_cars = create_object_from_file(car_path, 'Car', global_exit_queue)
    id_2_roads = create_object_from_file(road_path, 'Road', global_exit_queue)
    id_2_cross = create_object_from_file(cross_path, 'Cross', global_exit_queue)
    # 为所有的car设置source和destination
    for car_id, car in id_2_cars.items():
        source_id = car.get_source_id()
        destination_id = car.get_destination_id()
        car.set_source(id_2_cross[source_id])
        car.set_destination(id_2_cross[destination_id])

    # 为所有的road设置source和destination
    for road_id, road in id_2_roads.items():
        source_id = road.get_source_id()
        destination_id = road.get_destination_id()
        road.set_source(id_2_cross[source_id])
        road.set_destination(id_2_cross[destination_id])

    # 为所有的cross设置对应的road
    for cross_id, cross in id_2_cross.items():
        road_id_list = cross.get_road_id_list()
        roads = [id_2_roads[id] if id != -1 else None for id in road_id_list]
        cross.set_road_list(roads)
    return id_2_cars, id_2_roads, id_2_cross, global_exit_queue