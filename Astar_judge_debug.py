import re
import numpy as np
import copy
import sys


def read_file(road_file_name):
    fi = open("{}".format(road_file_name), "r", encoding="utf-8")
    information_txt = fi.read()
    p1 = r"(.+)"
    pattern1 = re.compile(p1)
    information = pattern1.findall(information_txt)
    information.pop(0)
    return information

def information_list_transform_dict(information_list):
    information_dict = {}
    for i in range(len(information_list)):
        information_dict['{}'.format(eval(information_list[i])[0])] =list(eval(information_list[i]))
    return information_dict

def creat_dict_sideweight_oritation(road_information_dict,cross_information_dict):
    cross_sideweight_dict={}
    cross_oritation_dict={}
    for key in cross_information_dict.keys():
        cross_sideweight_list = [0, 0, 0, 0, 0]
        cross_oritation_list = [0, 0, 0, 0, 0]
        cross_sideweight_list[0]=int(key)
        cross_oritation_list[0]=int(key)
        for i in range(1,5):
            cross_road_id = cross_information_dict['{}'.format(key)][i]
            if cross_road_id != -1:
                cross_road_information = road_information_dict['{}'.format(cross_road_id)]
                cross_road_information_length = cross_road_information[1]
                cross_road_information_isDuplex = cross_road_information[6]
                cross_road_information_from=cross_road_information[4]
                cross_road_information_to=cross_road_information[5]
                if cross_road_information_isDuplex == 1 :
                    cross_sideweight_list[i] = cross_road_information_length
                    if cross_road_information_from == int(key):
                        cross_oritation_list[i] =cross_road_information_to
                    else:
                        cross_oritation_list[i] = cross_road_information_from



                else:
                    if cross_road_information_from == int(key):
                        cross_sideweight_list[i] = cross_road_information_length
                        cross_oritation_list[i] = cross_road_information_to

        cross_sideweight_dict['{}'.format(key)]=cross_sideweight_list
        cross_oritation_dict['{}'.format(key)]=cross_oritation_list
    return cross_sideweight_dict,cross_oritation_dict

def orientational_x_y_dict(road_information_dict,cross_information_list,cross_information_dict ):
    m = []
    point_site = {}
    flg_cross_information_dict = copy.deepcopy(cross_information_dict)
    close_flag_cross_information_dict = copy.deepcopy(cross_information_dict)
    first_cross =eval(cross_information_list[0])[0]
    point_site['{}'.format(first_cross)] = (0, 0)
    close_flag_cross_information_dict['{}'.format(first_cross)][0] =0
    m.append(cross_information_dict['{}'.format(first_cross)])

    while len(m) != 0:
        first_item = m.pop(0)
        flg_cross_information_dict['{}'.format(first_item[0])][0] = 0
        for i in range(1, 5):
            slect_road = first_item[i]
            if slect_road != -1:                                             #int(slect_road % 5000 + 1)
                point1 = road_information_dict['{}'.format(slect_road)][4]
                point2 = road_information_dict['{}'.format(slect_road)][5]
                if point1 == first_item[0]:
                    if flg_cross_information_dict['{}'.format(point2)][0] != 0:
                        m.append(cross_information_dict['{}'.format(point2)])
                        x = point_site['{}'.format(first_item[0])][0]
                        y = point_site['{}'.format(first_item[0])][1]
                        road_lenght = road_information_dict['{}'.format(slect_road)][1]
                        if i == 1:
                            if close_flag_cross_information_dict['{}'.format(point2)][0] != 0:
                                point_site['{}'.format(point2)] = (x, y + road_lenght)
                                close_flag_cross_information_dict['{}'.format(point2)][0] = 0
                        if i == 2:
                            if close_flag_cross_information_dict['{}'.format(point2)][0] != 0:
                                point_site['{}'.format(point2)] = (x + road_lenght, y)
                                close_flag_cross_information_dict['{}'.format(point2)][0] = 0
                        if i == 3:
                            if close_flag_cross_information_dict['{}'.format(point2)][0] != 0:
                                point_site['{}'.format(point2)] = (x, y - road_lenght)
                                close_flag_cross_information_dict['{}'.format(point2)][0] = 0
                        if i == 4:
                            if close_flag_cross_information_dict['{}'.format(point2)][0] != 0:
                                point_site['{}'.format(point2)] = (x - road_lenght, y)
                                close_flag_cross_information_dict['{}'.format(point2)][0] = 0
                else:
                    if flg_cross_information_dict['{}'.format(point1) ][0] != 0:
                        m.append(cross_information_dict['{}'.format(point1)])
                        x = point_site['{}'.format(first_item[0])][0]
                        y = point_site['{}'.format(first_item[0])][1]
                        if i == 1:
                            if close_flag_cross_information_dict['{}'.format(point1)][0] != 0:
                                point_site['{}'.format(point1)] = (x, y + road_lenght)
                                close_flag_cross_information_dict['{}'.format(point1)][0] = 0
                        if i == 2:
                            if close_flag_cross_information_dict['{}'.format(point1)][0] != 0:
                                point_site['{}'.format(point1)] = (x + road_lenght, y)
                                close_flag_cross_information_dict['{}'.format(point1)][0] = 0
                        if i == 3:
                            if close_flag_cross_information_dict['{}'.format(point1)][0] != 0:
                                point_site['{}'.format(point1)] = (x, y - road_lenght)
                                close_flag_cross_information_dict['{}'.format(point1)][0] = 0
                        if i == 4:
                            if close_flag_cross_information_dict['{}'.format(point1)][0] != 0:
                                point_site['{}'.format(point1)] = (x - road_lenght, y)
                                close_flag_cross_information_dict['{}'.format(point1)][0] = 0
    return point_site

def car_current_limiting(road_path_limit_time,fo):
    time=1
    flag =0
    while len(road_path_limit_time) !=0:
        path = road_path_limit_time.pop(0)
        if path[1] ==time:
            path =tuple(path)
            fo.write(str(path))
            fo.write('\n')
            flag += 1
            while flag==20:
                time +=1
                flag =0
        elif path[1] >time:
            path =tuple(path)
            fo.write(str(path))
            fo.write('\n')
            time +=1
        else:
            path[1]= time
            path =tuple(path)
            fo.write(str(path))
            fo.write('\n')
            flag += 1
            while flag==20:
                time +=1
                flag =0

def creat_run_car_dict(list_car_time,time,path_dict,cross_information_dict):
    run_car_dict = {}

    while not run_car_dict:
        print(time)
        while eval(list_car_time[0])[4] == time:
            # for i in range(len(list_car_time)):
            # if eval(list_car_time[i])[4] == time:
            item = str(eval(list_car_time[0])[0])
            car_orientation_1 = path_dict[item][1][1]
            car_orientation_2 = path_dict[item][2][1]
            car_speed = eval(list_car_time[0])[3]
            start_cross_id = path_dict[item][0][0]
            if len(path_dict[item]) <= 2:
                cross_id_information =cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_dict[item] = [go_straight, car_speed, wait_select,road_position_id]
                run_car_dict.update()
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            else:
                if car_orientation_1 == 1 and car_orientation_2 == 1:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [go_straight, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 1 and car_orientation_2 == 2:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_right, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 1 and car_orientation_2 == 4:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_left, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 2 and car_orientation_2 == 1:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    run_car_dict[item] = [turn_left, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 2 and car_orientation_2 == 2:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [go_straight, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 2 and car_orientation_2 == 3:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_right, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 3 and car_orientation_2 == 2:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_left, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 3 and car_orientation_2 == 3:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [go_straight, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 3 and car_orientation_2 == 4:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_right, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 4 and car_orientation_2 == 1:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_right, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 4 and car_orientation_2 == 3:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [turn_left, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue
                if car_orientation_1 == 4 and car_orientation_2 == 4:
                    cross_id_information = cross_information_dict[str(start_cross_id)]
                    road_position_id = cross_id_information[car_orientation_1]
                    run_car_dict[item] = [go_straight, car_speed, wait_select,road_position_id]
                    list_car_time.pop(0)
                    if len(list_car_time) == 0:
                        break
                    else:
                        continue

        time += 1
    return run_car_dict,time

def calculate_car_orientation(car_id,present_cross_id,path_dict):
    car_path = path_dict['{}'.format(car_id)]
    for i in range(len(car_path)):
        if car_path[i][0] == present_cross_id:
            if i+1 >= len(car_path)-1:
                return 1
            else:
                car_orientation_1 = car_path[i+1][1]
                car_orientation_2 = car_path[i+2][1]
                if car_orientation_1 == 1 and car_orientation_2 == 1:
                    return go_straight
                if car_orientation_1 == 1 and car_orientation_2 == 2:
                    return  turn_right
                if car_orientation_1 == 1 and car_orientation_2 == 4:
                    return turn_left
                if car_orientation_1 == 2 and car_orientation_2 == 1:
                    return turn_left
                if car_orientation_1 == 2 and car_orientation_2 == 2:
                    return  go_straight
                if car_orientation_1 == 2 and car_orientation_2 == 3:
                   return  turn_right
                if car_orientation_1 == 3 and car_orientation_2 == 2:
                    return  turn_left
                if car_orientation_1 == 3 and car_orientation_2 == 3:
                    return  go_straight
                if car_orientation_1 == 3 and car_orientation_2 == 4:
                    return turn_right
                if car_orientation_1 == 4 and car_orientation_2 == 1:
                    return  turn_right
                if car_orientation_1 == 4 and car_orientation_2 == 3:
                    return  turn_left
                if car_orientation_1 == 4 and car_orientation_2 == 4:
                    return  go_straight

def creat_new_run_car_dict(list_car_time,time,path_dict):
    run_car_new_dict = {}
    if len(list_car_time) == 0:
        return run_car_new_dict

    while eval(list_car_time[0])[4] == time:

        item = str(eval(list_car_time[0])[0])
        car_orientation_1 = path_dict[item][1][1]
        car_orientation_2 = path_dict[item][2][1]
        car_speed = eval(list_car_time[0])[3]
        start_cross_id = path_dict[item][0][0]
        if len(path_dict[item]) <= 2:
            cross_id_information =cross_information_dict[str(start_cross_id)]
            road_position_id = cross_id_information[car_orientation_1]
            run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select,road_position_id]
            list_car_time.pop(0)
            if len(list_car_time) == 0:
                break
            else:
                continue
        else:
            if car_orientation_1 == 1 and car_orientation_2 == 1:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 1 and car_orientation_2 == 2:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 1 and car_orientation_2 == 4:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 2 and car_orientation_2 == 1:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 2 and car_orientation_2 == 2:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 2 and car_orientation_2 == 3:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 3 and car_orientation_2 == 2:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 3 and car_orientation_2 == 3:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 3 and car_orientation_2 == 4:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 4 and car_orientation_2 == 1:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 4 and car_orientation_2 == 3:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
            if car_orientation_1 == 4 and car_orientation_2 == 4:
                cross_id_information = cross_information_dict[str(start_cross_id)]
                road_position_id = cross_id_information[car_orientation_1]
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select,road_position_id]
                list_car_time.pop(0)
                if len(list_car_time)==0:
                    break
                else:
                    continue
    return run_car_new_dict

class AStar(object):
    """
    创建一个A*算法类
    """

    def __init__(self, road_information_dict, cross_information_dict, car, cross_sideweight_dict, cross_oritation_dict,cross_site_position ):
        """
        初始化
        """
        # self.g = 0  # g初始化为0
        self.start_point = car[1]  # 起点坐标
        self.goal_point = car[2]  # 终点坐标
        self.car_speed =car[3]
        self.open_table = []  # 先创建一个空的open表, ID,方向，g值，f值
        self.closed_table = []  # 先创建一个空的closed表
        # self.best_path_array = numpy.array([[], []])  # 回溯路径表
        self.cross_information =cross_information_dict
        self.road_information = road_information_dict
        self.array_orientational =cross_oritation_dict
        self.array_sideweight = cross_sideweight_dict
        self.dictionary_position = cross_site_position
        self.car = car


    def h_value_tem(self, son_point):
        """
        计算拓展节点和终点的h值
        :param son_p:子搜索节点坐标
        :return:
        """
        # print(self.dictionary_position['node_num{}'.format(son_point[0])][0])

        h = (self.dictionary_position['{}'.format(son_point[0])][0] -
             self.dictionary_position['{}'.format(self.goal_point)][0]) ** 2 + (
                        self.dictionary_position['{}'.format(son_point[0])][1] -
                        self.dictionary_position['{}'.format(self.goal_point)][1]) ** 2
        h = np.sqrt(h)  # 计算h
        return h

    def g_accumulation(self, son_point, father_point):
        item_father = self.cross_information['{}'.format(father_point[0])]  # 读取父、子节点信息
        item_son = self.cross_information['{}'.format(son_point[0])]
        for i in range(1, 5):
            if item_father[i] != -1:
                for j in range(1, 5):
                    if item_father[i] == item_son[j]:
                        g1=self.road_information['{}'.format(item_father[i])][1]
                        break

        g = g1 + father_point[2]  # 加上累计的g值
        return g

    def f_value_tem(self, son_point, father_point):
        """
        求出的是临时g值和h值加上累计g值得到全局f值
        :param father_p: 父节点坐标
        :param son_p: 子节点坐标
        :return:f
        """
        f = self.g_accumulation(son_point, father_point) + self.h_value_tem(son_point)
        return f

    def child_point(self, father_point):

        for i in range(1, 5):
            father_point_ID = father_point[0]
            father_point_orientation_list = self.array_orientational['{}'.format(father_point_ID)]
            # print(father_point_orientation_list)
            if father_point_orientation_list[i]!=0:
                # pdb.set_trace();
                child_cross_ID = father_point_orientation_list[i]

                road_id_two_point = self.cross_information['{}'.format(father_point_ID)][i]                       #找到子父节点间的道路信息
                road_information_two_point = self.road_information['{}'.format(road_id_two_point)]
                road_information_two_point_id=road_information_two_point[0]
                road_information_two_point_speed=road_information_two_point[2]
                road_information_two_point_channel =road_information_two_point[3]
                if road_information_two_point[6] ==0:    #判断所在道路是否为单向
                    if road_information_two_point_channel !=1:
                        if road_information_two_point[4] == father_point_ID:
                            child_cross_point = [child_cross_ID, i, 0, 0, 0, road_information_two_point_id]

                            record_g = self.g_accumulation(child_cross_point, father_point)
                            record_f = self.f_value_tem(child_cross_point, father_point)

                            child_cross_point = [child_cross_ID, i, record_g, record_f, father_point_ID,
                                                 road_information_two_point_id]

                            find_close_Flag = 0
                            for j in range(0, len(self.closed_table)):  # 判断CLOSE表是否含有此节点
                                if child_cross_point[0] == self.closed_table[j][0]:
                                    find_close_Flag = 1
                                    break

                            if find_close_Flag == 1:
                                continue

                            find_open_Flag = 0
                            for k in range(0, len(self.open_table)):  # 判断OPEN表是否含有此节点
                                if child_cross_point[0] == self.open_table[k][0]:
                                    find_open_Flag = 1
                                    if child_cross_point[3] < self.open_table[k][3]:
                                        self.open_table[k][1] = child_cross_point[1]
                                        self.open_table[k][2] = child_cross_point[2]
                                        self.open_table[k][3] = child_cross_point[3]
                                        self.open_table[k][4] = child_cross_point[4]
                                        self.open_table[k][5] = child_cross_point[5]
                                        break

                            if find_open_Flag == 0:  # 若以上两个判断都通过，则将此节点加入open表
                                self.open_table.append(child_cross_point)
                        if road_information_two_point[4] == child_cross_ID:
                           continue
                    else:
                        if self.car_speed >= road_information_two_point_speed:
                            if road_information_two_point[4] == father_point_ID:
                                child_cross_point = [child_cross_ID, i, 0, 0, 0, road_information_two_point_id]

                                record_g = self.g_accumulation(child_cross_point, father_point)
                                record_f = self.f_value_tem(child_cross_point, father_point)

                                child_cross_point = [child_cross_ID, i, record_g, record_f, father_point_ID,
                                                     road_information_two_point_id]

                                find_close_Flag = 0
                                for j in range(0, len(self.closed_table)):  # 判断CLOSE表是否含有此节点
                                    if child_cross_point[0] == self.closed_table[j][0]:
                                        find_close_Flag = 1
                                        break

                                if find_close_Flag == 1:
                                    continue

                                find_open_Flag = 0
                                for k in range(0, len(self.open_table)):  # 判断OPEN表是否含有此节点
                                    if child_cross_point[0] == self.open_table[k][0]:
                                        find_open_Flag = 1
                                        if child_cross_point[3] < self.open_table[k][3]:
                                            self.open_table[k][1] = child_cross_point[1]
                                            self.open_table[k][2] = child_cross_point[2]
                                            self.open_table[k][3] = child_cross_point[3]
                                            self.open_table[k][4] = child_cross_point[4]
                                            self.open_table[k][5] = child_cross_point[5]
                                            break

                                if find_open_Flag == 0:  # 若以上两个判断都通过，则将此节点加入open表
                                    self.open_table.append(child_cross_point)
                            if road_information_two_point[4] == child_cross_ID:
                                continue
                        else:
                            continue


                else:
                    if road_information_two_point_channel != 1:
                        child_cross_point = [child_cross_ID, i, 0, 0, 0, road_information_two_point_id]

                        record_g = self.g_accumulation(child_cross_point, father_point)
                        record_f = self.f_value_tem(child_cross_point, father_point)

                        child_cross_point = [child_cross_ID, i, record_g, record_f, father_point_ID,
                                             road_information_two_point_id]

                        find_close_Flag = 0
                        for j in range(0, len(self.closed_table)):  # 判断CLOSE表是否含有此节点
                            if child_cross_point[0] == self.closed_table[j][0]:
                                find_close_Flag = 1
                                break

                        if find_close_Flag == 1:
                            continue

                        find_open_Flag = 0
                        for k in range(0, len(self.open_table)):  # 判断OPEN表是否含有此节点
                            if child_cross_point[0] == self.open_table[k][0]:
                                find_open_Flag = 1
                                if child_cross_point[3] < self.open_table[k][3]:
                                    self.open_table[k][1] = child_cross_point[1]
                                    self.open_table[k][2] = child_cross_point[2]
                                    self.open_table[k][3] = child_cross_point[3]
                                    self.open_table[k][4] = child_cross_point[4]
                                    self.open_table[k][5] = child_cross_point[5]
                                    break

                        if find_open_Flag == 0:  # 若以上两个判断都通过，则将此节点加入open表
                            self.open_table.append(child_cross_point)
                    else:
                        if self.car_speed >= road_information_two_point_speed:
                            child_cross_point = [child_cross_ID, i, 0, 0, 0, road_information_two_point_id]

                            record_g = self.g_accumulation(child_cross_point, father_point)
                            record_f = self.f_value_tem(child_cross_point, father_point)

                            child_cross_point = [child_cross_ID, i, record_g, record_f, father_point_ID,
                                                 road_information_two_point_id]

                            find_close_Flag = 0
                            for j in range(0, len(self.closed_table)):  # 判断CLOSE表是否含有此节点
                                if child_cross_point[0] == self.closed_table[j][0]:
                                    find_close_Flag = 1
                                    break

                            if find_close_Flag == 1:
                                continue

                            find_open_Flag = 0
                            for k in range(0, len(self.open_table)):  # 判断OPEN表是否含有此节点
                                if child_cross_point[0] == self.open_table[k][0]:
                                    find_open_Flag = 1
                                    if child_cross_point[3] < self.open_table[k][3]:
                                        self.open_table[k][1] = child_cross_point[1]
                                        self.open_table[k][2] = child_cross_point[2]
                                        self.open_table[k][3] = child_cross_point[3]
                                        self.open_table[k][4] = child_cross_point[4]
                                        self.open_table[k][5] = child_cross_point[5]
                                        break
                        else:
                            continue



    def main(self):
        best = self.start_point
        h0 = self.h_value_tem([best, 0, 0, 0])
        init_open = [best, 0, 0, h0]
        self.open_table.append(init_open)

        ite = 1  # 设置迭代次数小于1000，防止程序出错无限循环
        while ite <= 1000:
            if len(self.open_table) == 0:
                print('{}'.format(self.car[0]) + '没有搜索到路径！')
                return

            ls = self.open_table
            ls = sorted(ls, key=lambda ls: ls[3])
            self.open_table = ls
            first_item = self.open_table.pop(0)
            self.closed_table.append(first_item)

            if first_item[0] == self.goal_point:
                car_path = {}
                path_list = []
                tow_point_road_id_list=[]
                now_father_point_id = first_item[0]
                while now_father_point_id != best:
                    for i in range(0,len(self.closed_table)):
                        if now_father_point_id == self.closed_table[i][0]:
                            path_list.append([self.closed_table[i][0], self.closed_table[i][1]])
                            now_father_point_id = self.closed_table[i][4]
                            tow_point_road_id_list.append( self.closed_table[i][5])
                            break
                path_list.append([best,0])
                path_list.reverse()
                tow_point_road_id_list.append(self.car[4])
                tow_point_road_id_list.append(self.car[0])
                tow_point_road_id_list.reverse()
                return  path_list,tow_point_road_id_list

            self.child_point(first_item)

            ite = ite + 1
            # return  car_path

class road():                           #raod类

    def __init__(self,road_information):
    #def __init__(self,road_length,road_width,road_from,road_to,isDuplex):
        self.road_length =road_information[1]
        self.road_width = road_information[3]
        self.one_both = road_information[6]
        self.road_from =road_information[4]
        self.road_to = road_information[5]

    def create_road_model(self):
        if self.one_both == 1:
            road_model = np.zeros((self.road_width*2, self.road_length+2 ), dtype=int)
        else:
            road_model = np.zeros((self.road_width*1, self.road_length +2), dtype=int)
        return  road_model

    def create_road_orientation(self,road_model):
        k = self.road_length + 1
        if self.one_both ==1:
            for i in range(0, self.road_width):
                road_model[i][0] = self.road_from
                road_model[i][k] = self.road_to
            for i in range(self.road_width,self.road_width*2):
                road_model[i][0] = self.road_to
                road_model[i][k] = self.road_from
        else:
            for i in range(0, self.road_width):
                road_model[i][0] = self.road_from
                road_model[i][k] = self.road_to


        return road_model

    def main_creat_road(self):
        one_model = self.create_road_model()
        road_model = self.create_road_orientation(one_model)
        return road_model





car_num_arrived = 0                    #参数定义
car_num_waitting = 0


wait_select = 0                                  #定义状态
wait_run = 1
finish_run = 2

go_straight = 1                   #定义方向
turn_left = 2
turn_right =3
time =1

road_information_list = read_file('road.txt')                         #生成地图模型、车静态信息
cross_information_list = read_file('cross.txt')
car_information_list = read_file('small_car.txt')
road_information_dict = information_list_transform_dict(road_information_list)
cross_information_dict = information_list_transform_dict(cross_information_list)
car_information_dict = information_list_transform_dict(car_information_list)
cross_sideweight_dict,cross_oritation_dict=creat_dict_sideweight_oritation(road_information_dict,cross_information_dict)
cross_site_position=orientational_x_y_dict(road_information_dict,cross_information_list,cross_information_dict )




path_dict = {}
road_dict ={}

fo =open('anwser.txt','w',encoding='utf-8')
s='#(car_id,star_time,path)'
fo.write(s)
fo.write('\n')
road_path_limit_time = []



#生成道路模型
for i in range(0,len(road_information_list)):
    road_information_1 = eval(road_information_list[i])
    road_model = road(road_information_1)
    road_model=road_model.main_creat_road()

    road_dict['{}'.format(road_information_1[0])]=road_model

'''
fo =open('anwser.txt','w',encoding='utf-8')
s='#(car_id,star_time,path)'
fo.write(s)
fo.write('\n')
road_path_limit_time = []
'''

for i in range(0,len(car_information_list)):                                #生成车辆行驶路径
    car_in_all = eval(car_information_list[i])
    k = AStar(road_information_dict, cross_information_dict, car_in_all, cross_sideweight_dict, cross_oritation_dict,cross_site_position )
    cross_path,road_path = k.main()
    path_dict['{}'.format(car_in_all[0])] = cross_path
   # fo.write(str(road_path))
    #fo.write('\n')
    road_path_limit_time.append(road_path)

print(path_dict['10030'])



#road_path_limit_time.sort(key=lambda x:x[1])                        #静态程序生成路径所需要的排序
#car_current_limiting(road_path_limit_time,fo)

#生成车辆按出发时间排序列表
list_car_time_1 = car_information_list[:]
list_car_time = sorted(list_car_time_1,key=lambda list_car_time_1:eval(list_car_time_1)[4])


run_car_dict,time = creat_run_car_dict(list_car_time,time,path_dict,cross_information_dict)            #初始化车辆出发字典
run_car_list = sorted(run_car_dict.items(),key=lambda item:item[0])

time = time -1         #重置时间

#第一次将车派上路
for i in range(len(run_car_list)):                                            #遍历run_car_dict,将车辆安排上路
    car_initial_id=run_car_list[i][0]
    car_initial_information =car_information_dict [car_initial_id]          #获取派车上路所需信息
    start_point = car_initial_information[1]
    car_initial_speed = car_initial_information[3]
    car_initial_orientation = path_dict[car_initial_id][1][1]
    car_start_road =cross_information_dict['{}'.format(start_point)][car_initial_orientation]
    road_model=road_dict['{}'.format(car_start_road)]
    car_road_information = road_information_dict['{}'.format(car_start_road)]
    car_road_length = car_road_information[1]
    road_speed = car_road_information[2]
    car_initial_speed = min(car_initial_speed,road_speed)

    if road_model[0,0] == start_point:                             #如果所派车辆，所在道路为正向道路
        flag_no_free_channel = 1
        flag_car_front_find = 0
        for channel in range(car_road_information[3]):            #如果车进入的车道有空位，将车安排上去
            if road_model[channel, 1] == 0:
                flag_no_free_channel = 0
                if flag_car_front_find == 1:
                    break
                for go_ahead_length in range(1, car_initial_speed + 1):
                    if road_model[channel, 1] !=0:
                        break
                    if road_model[channel, go_ahead_length] != 0:
                        road_model[channel, go_ahead_length - 1] = car_initial_id
                        road_dict['{}'.format(car_start_road)] = road_model
                        flag_car_front_find = 1
                        break

                if flag_car_front_find == 0:
                    road_model[channel, car_initial_speed] = car_initial_id        #若进入车道没车，车辆进入最大空位处
                    road_dict['{}'.format(car_start_road)] = road_model
                    break
        if flag_no_free_channel ==1:                                             #若车道无空位，车辆信息重新进入list_car_time
            run_car_dict.pop('{}'.format(car_initial_id))
            car_initial_information_list = list(car_initial_information)
            car_initial_information_list[4] = time + 1
            print(car_initial_information_list)
            car_initial_information_list = [str((car_initial_information_list[0],
                                                 car_initial_information_list[1],
                                                 car_initial_information_list[2],
                                                 car_initial_information_list[3],
                                                 car_initial_information_list[4]))]
            list_car_time = car_initial_information_list + list_car_time

    else:                                                                      #如果所派车辆，所在道路为反向道路
        flag_no_free_channel = 1
        flag_car_front_find = 0
        for channel in range(car_road_information[3]*2-1,car_road_information[3]-1,-1):
            if road_model[channel, car_road_length] == 0:
                flag_no_free_channel = 0
                if flag_car_front_find == 1:
                    break
                for go_ahead_length in range(car_road_length, car_road_length-car_initial_speed,-1):
                    if road_model[channel, go_ahead_length] != 0:
                        road_model[channel, go_ahead_length + 1] = car_initial_id
                        road_dict['{}'.format(car_start_road)] = road_model
                        flag_car_front_find = 1
                        break

                if flag_car_front_find == 0:
                    road_model[channel, car_road_length-car_initial_speed+1] = car_initial_id   #车的坐标需要检查，+1还是减1
                    road_dict['{}'.format(car_start_road)] = road_model
                    break

        if flag_no_free_channel == 1:
            run_car_dict.pop('{}'.format(car_initial_id))
            car_initial_information_list = list(car_initial_information)
            car_initial_information_list[4] = time + 1
            print(car_initial_information_list)
            car_initial_information_list = [str((car_initial_information_list[0],
                                                 car_initial_information_list[1],
                                                 car_initial_information_list[2],
                                                 car_initial_information_list[3],
                                                 car_initial_information_list[4]))]
            list_car_time = car_initial_information_list + list_car_time

list_car_time = sorted(list_car_time,key=lambda list_car_time:(eval(list_car_time)[4],eval(list_car_time)[0]))

#通过当前车辆信息，查询是否其他道路有跟这辆车起冲突的车
def conflict_judgment(j,k,l,car_orientation_state,cross_model,run_car_dict,road_dict):  #通过当前车辆信息，查询是否其他道路有跟这辆车起冲突的车
    cross_model_id = cross_model[0]
    cross_road_id = cross_model[j]
    road_model = road_dict['{}'.format(cross_road_id)]
    road_model_information = road_information_dict[str(cross_road_id)]
    road_model_length = road_model_information[1]
    road_model_wight = road_model_information[3]
    road_model_speed = road_model_information[2]

    item_car_in_road_id = road_model[l, k]
    item_car_in_road_information = run_car_dict['{}'.format(item_car_in_road_id)]
    item_car_in_road_speed = item_car_in_road_information[1]
    item_car_in_road_speed_max = min(item_car_in_road_speed, road_model_speed)
    item_car_in_road_state = item_car_in_road_information[2]
    item_car_in_road_orientation = item_car_in_road_information[0]

    find_car_conflict_flag = 0  #是否存在冲突车辆的标志

    if car_orientation_state ==1:
        return  find_car_conflict_flag   #车辆直行，优先级最高，没有冲突
    if car_orientation_state ==2:        #车辆左转，检测是否有直行车辆冲突
        if j==1:
            conflict_road_id_1 = cross_model[4]
            if conflict_road_id_1==-1:   #这条路不存在，没冲突
                return find_car_conflict_flag
            else:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model,conflict_road_id_1,run_car_dict,road_dict)
                return find_car_conflict_flag
        if j==2:
            conflict_road_id_1 = cross_model[1]
            if conflict_road_id_1 == -1:  # 这条路不存在，没冲突
                return find_car_conflict_flag
            else:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                return find_car_conflict_flag
        if j==3:
            conflict_road_id_1 = cross_model[2]
            if conflict_road_id_1 == -1:  # 这条路不存在，没冲突
                return find_car_conflict_flag
            else:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                return find_car_conflict_flag
        if j==4:
            conflict_road_id_1 = cross_model[3]
            if conflict_road_id_1 == -1:  # 这条路不存在，没冲突
                return find_car_conflict_flag
            else:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                return find_car_conflict_flag     #车辆直行，优先级最高，没有冲突
    if car_orientation_state==3:     #车辆右转，检测是否有直行车辆和左转冲突
        if j==1:
            conflict_road_id_1 = cross_model[2]
            conflict_road_id_2 = cross_model[3]
            if conflict_road_id_1==-1 and conflict_road_id_2==-1:   #这条路不存在，没冲突
                return find_car_conflict_flag
            elif conflict_road_id_1==-1:
                find_car_conflict_flag = turn_left_car_conflict_find(cross_model,conflict_road_id_2,run_car_dict,road_dict)
                return find_car_conflict_flag
            elif conflict_road_id_2==-1:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model,conflict_road_id_1,run_car_dict,road_dict)
                return find_car_conflict_flag
            else:
                find_car_conflict_flag1 = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                find_car_conflict_flag2 = turn_left_car_conflict_find(cross_model, conflict_road_id_2, run_car_dict,road_dict)
                return  (find_car_conflict_flag1 or find_car_conflict_flag2)
        if j==2:
            conflict_road_id_1 = cross_model[3]
            conflict_road_id_2 = cross_model[4]
            if conflict_road_id_1==-1 and conflict_road_id_2==-1:   #这条路不存在，没冲突
                return find_car_conflict_flag
            elif conflict_road_id_1==-1:
                find_car_conflict_flag = turn_left_car_conflict_find(cross_model,conflict_road_id_2,run_car_dict,road_dict)
                return find_car_conflict_flag
            elif conflict_road_id_2==-1:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model,conflict_road_id_1,run_car_dict,road_dict)
                return find_car_conflict_flag
            else:
                find_car_conflict_flag1 = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                find_car_conflict_flag2 = turn_left_car_conflict_find(cross_model, conflict_road_id_2, run_car_dict,road_dict)
                return  (find_car_conflict_flag1 or find_car_conflict_flag2)
        if j==3:
            conflict_road_id_1 = cross_model[4]
            conflict_road_id_2 = cross_model[1]
            if conflict_road_id_1==-1 and conflict_road_id_2==-1:   #这条路不存在，没冲突
                return find_car_conflict_flag
            elif conflict_road_id_1==-1:
                find_car_conflict_flag = turn_left_car_conflict_find(cross_model,conflict_road_id_2,run_car_dict,road_dict)
                return find_car_conflict_flag
            elif conflict_road_id_2==-1:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model,conflict_road_id_1,run_car_dict,road_dict)
                return find_car_conflict_flag
            else:
                find_car_conflict_flag1 = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                find_car_conflict_flag2 = turn_left_car_conflict_find(cross_model, conflict_road_id_2, run_car_dict,road_dict)
                return  (find_car_conflict_flag1 or find_car_conflict_flag2)
        if j==4:
            conflict_road_id_1 = cross_model[1]
            conflict_road_id_2 = cross_model[2]
            if conflict_road_id_1==-1 and conflict_road_id_2==-1:   #这条路不存在，没冲突
                return find_car_conflict_flag
            elif conflict_road_id_1==-1:
                find_car_conflict_flag = turn_left_car_conflict_find(cross_model,conflict_road_id_2,run_car_dict,road_dict)
                return find_car_conflict_flag
            elif conflict_road_id_2==-1:
                find_car_conflict_flag = go_straigh_car_conflict_find(cross_model,conflict_road_id_1,run_car_dict,road_dict)
                return find_car_conflict_flag
            else:
                find_car_conflict_flag1 = go_straigh_car_conflict_find(cross_model, conflict_road_id_1, run_car_dict,road_dict)
                find_car_conflict_flag2 = turn_left_car_conflict_find(cross_model, conflict_road_id_2, run_car_dict,road_dict)
                return  (find_car_conflict_flag1 or find_car_conflict_flag2)

#查询这条道路是否有直行冲突车辆
def go_straigh_car_conflict_find(cross_model,conflict_road_id,run_car_dict,road_dict): #检测这条路第一优先级是否有直行并且能过路口的车辆（冲突车辆），给予路口以及道路信息
    conflict_road_model = road_dict['{}'.format(conflict_road_id)]  # 找到要检测这条路的信息
    conflict_road_information = road_information_dict[str(conflict_road_id)]
    conflict_road_length = conflict_road_information[1]
    conflict_road_width = conflict_road_information[3]
    conflict_road_speed = conflict_road_information[2]
    find_go_straight_conflict_flag = 0
    if conflict_road_information[6] == 0:  # 此路是单行道的情况
        if conflict_road_model[0, conflict_road_length + 1] == cross_model_id:  # 单行道的话，看这条路是不是通往路口，是的话，该条道路可能存在冲突车
            for channels in range(conflict_road_width):
                if find_go_straight_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                    break
                for index in range(conflict_road_length, 0, -1):
                    if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                        car_in_conflict_road_id = conflict_road_model[channels, index]
                        car_in_conflict_road_information = run_car_dict['{}'.format(car_in_conflict_road_id)]
                        car_in_conflict_road_speed = car_in_conflict_road_information[1]
                        if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                            break
                        else:  # 这两车是等待的情况
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 1:  # 直行,看能不能出路口
                                conflict_car_can_move_distance = min(conflict_road_speed, car_in_conflict_road_speed)
                                if conflict_car_can_move_distance + index < conflict_road_length + 1:  # 如果无法通过路口，则不会起冲突
                                    break
                                else:  # 等待车辆是直行，且通过路口，则会起冲突
                                    find_go_straight_conflict_flag = 1
                                    break
                            else:
                                break
    else:
        if conflict_road_model[0, conflict_road_length + 1] == cross_model_id:  # 双行道，则此时用的上半部分路
            for channels in range(conflict_road_width):
                if find_go_straight_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                    break
                for index in range(conflict_road_length, 0, -1):
                    if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                        car_in_conflict_road_id = conflict_road_model[channels, index]
                        car_in_conflict_road_information = run_car_dict['{}'.format(car_in_conflict_road_id)]
                        car_in_conflict_road_speed = car_in_conflict_road_information[1]
                        if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                            break
                        else:  # 这两车是等待的情况
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 1:  # 直行,看能不能出路口
                                conflict_car_can_move_distance = min(conflict_road_speed,
                                                                     car_in_conflict_road_speed)
                                if conflict_car_can_move_distance + index < conflict_road_length + 1:  # 如果无法通过路口，则不会起冲突
                                    break
                                else:  # 等待车辆是直行，且通过路口，则会起冲突
                                    find_go_straight_conflict_flag = 1
                                    break
                            else:
                                break
        else:
            for channels in range(conflict_road_width * 2 - 1, conflict_road_width - 1, -1):
                if find_go_straight_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                    break
                for index in range(1, conflict_road_length + 1):
                    if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                        car_in_conflict_road_id = conflict_road_model[channels, index]
                        car_in_conflict_road_information = run_car_dict[ '{}'.format(car_in_conflict_road_id)]
                        car_in_conflict_road_speed = car_in_conflict_road_information[1]
                        if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                            break
                        else:  # 这两车是等待的情况
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 1:  # 直行,看能不能出路口
                                conflict_car_can_move_distance = min(conflict_road_speed,
                                                                     car_in_conflict_road_speed)
                                if index - conflict_car_can_move_distance >= 1:  # 如果无法通过路口，则不会起冲突
                                    break
                                else:  # 等待车辆是直行，且通过路口，则会起冲突
                                    find_go_straight_conflict_flag = 1
                                    break
                            else:
                                break
    return  find_go_straight_conflict_flag

#查询这条道路是否有左转冲突车辆
def turn_left_car_conflict_find(cross_model,conflict_road_id,run_car_dict,road_dict): #检测这条路第一优先级是否有直行并且能过路口的车辆
    conflict_road_model = road_dict['{}'.format(conflict_road_id)]  # 找到要检测这条路的信息
    conflict_road_information = road_information_dict[str(conflict_road_id)]
    conflict_road_length = conflict_road_information[1]
    conflict_road_width = conflict_road_information[3]
    conflict_road_speed = conflict_road_information[2]
    find_turn_left_conflict_flag = 0
    if conflict_road_information[6] == 0:  # 此路是单行道的情况
        if conflict_road_model[0, conflict_road_length + 1] == cross_model_id:  # 单行道的话，看这条路是不是通往路口，是的话，该条道路可能存在冲突车
            for channels in range(conflict_road_width):
                if find_turn_left_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                    break
                for index in range(conflict_road_length, 0, -1):
                    if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                        car_in_conflict_road_id = conflict_road_model[channels, index]
                        car_in_conflict_road_information = run_car_dict['{}'.format(car_in_conflict_road_id)]
                        car_in_conflict_road_speed = car_in_conflict_road_information[1]
                        if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                            break
                        else:  # 这两车是等待的情况
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 2:  # 左转,看能不能出路口
                                conflict_car_can_move_distance = min(conflict_road_speed, car_in_conflict_road_speed)
                                if conflict_car_can_move_distance + index < conflict_road_length + 1:  # 如果无法通过路口，则不会起冲突
                                    break
                                else:  # 等待车辆是直行，且通过路口，则会起冲突
                                    find_turn_left_conflict_flag = 1
                                    break
                            else:
                                break
    else:
        if conflict_road_model[0, conflict_road_length + 1] == cross_model_id:  # 双行道，则此时用的上半部分路
            for channels in range(conflict_road_width):
                if find_turn_left_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                    break
                for index in range(conflict_road_length, 0, -1):
                    if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                        car_in_conflict_road_id = conflict_road_model[channels, index]
                        car_in_conflict_road_information = run_car_dict['{}'.format(car_in_conflict_road_id)]
                        car_in_conflict_road_speed = car_in_conflict_road_information[1]
                        if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                            break
                        else:  # 这两车是等待的情况
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 2:  # 左转,看能不能出路口
                                conflict_car_can_move_distance = min(conflict_road_speed,
                                                                     car_in_conflict_road_speed)
                                if conflict_car_can_move_distance + index < conflict_road_length + 1:  # 如果无法通过路口，则不会起冲突
                                    break
                                else:  # 等待车辆是直行，且通过路口，则会起冲突
                                    find_turn_left_conflict_flag = 1
                                    break
        else:
            if conflict_road_model[0, conflict_road_length + 1] == cross_model_id:  # 双行道，则此时用的上半部分路
                for channels in range(conflict_road_width):
                    if find_turn_left_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                        break
                    for index in range(conflict_road_length, 0, -1):
                        if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                            car_in_conflict_road_id = conflict_road_model[channels, index]
                            car_in_conflict_road_information = run_car_dict['{}'.format(car_in_conflict_road_id)]
                            car_in_conflict_road_speed = car_in_conflict_road_information[1]
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                                break
                            else:  # 这两车是等待的情况
                                if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 1:  # 直行,看能不能出路口
                                    conflict_car_can_move_distance = min(conflict_road_speed,
                                                                         car_in_conflict_road_speed)
                                    if conflict_car_can_move_distance + index < conflict_road_length + 1:  # 如果无法通过路口，则不会起冲突
                                        break
                                    else:  # 等待车辆是直行，且通过路口，则会起冲突
                                        find_turn_left_conflict_flag = 1
                                        break
                                else:
                                    break
            else:
                for channels in range(conflict_road_width * 2 - 1, conflict_road_width - 1, -1):
                    if find_turn_left_conflict_flag == 1:  # 已经找到冲突车辆了，不再进行循环寻找了
                        break
                    for index in range(1, conflict_road_length + 1):
                        if conflict_road_model[channels, index] != 0:  # 假如这个位置存在车辆的话，则是第一优先级车辆
                            car_in_conflict_road_id = conflict_road_model[channels, index]
                            car_in_conflict_road_information = run_car_dict['{}'.format(car_in_conflict_road_id)]
                            car_in_conflict_road_speed = car_in_conflict_road_information[1]
                            if run_car_dict['{}'.format(car_in_conflict_road_id)][2] == 2:  # 如果这辆车已经终止，则不管了
                                break
                            else:  # 这两车是等待的情况
                                if run_car_dict['{}'.format(car_in_conflict_road_id)][0] == 1:  # 直行,看能不能出路口
                                    conflict_car_can_move_distance = min(conflict_road_speed,car_in_conflict_road_speed)
                                    if index - conflict_car_can_move_distance >= 1:  # 如果无法通过路口，则不会起冲突
                                        break
                                    else:  # 等待车辆是直行，且通过路口，则会起冲突
                                        find_turn_left_conflict_flag = 1
                                        break
                                else:
                                    break
        return find_turn_left_conflict_flag

#将车行驶到下一条路，up_or_down_flag为1代表前一条路我们使用的上半部分矩阵，0代表前一条路使用的下半部分矩阵
def car_run_next_road(j,k,l,car_orientation_state,cross_model,car_num_waitting,car_num_arrived,run_car_dict,road_dict,up_or_down_flag,car_num_stopped):

    move_flag = 0  #判别这辆车是否发生了移动
    cross_model_id = cross_model[0]
    cross_road_id = cross_model[j]

    road_model = road_dict['{}'.format(cross_road_id)]
    road_model_information = road_information_dict[str(cross_road_id)]
    road_model_length = road_model_information[1]
    road_model_wight = road_model_information[3]
    road_model_speed = road_model_information[2]

    item_car_in_road_id = road_model[l, k]
    item_car_in_road_information = run_car_dict['{}'.format(item_car_in_road_id)]
    item_car_in_road_speed = item_car_in_road_information[1]
    item_car_in_road_speed_max = min(item_car_in_road_speed, road_model_speed)
    item_car_in_road_state = item_car_in_road_information[2]
    item_car_in_road_orientation = item_car_in_road_information[0]

    car_end_point = car_information_dict[str(item_car_in_road_id)][2]


    if car_end_point == cross_model_id:  # 车辆到达终点   ##这里要添加锁死flag
        car_num_waitting -= 1
        car_num_arrived += 1
        system_dead_flag = 0
        print('车：', item_car_in_road_id, '+','到达终点',car_end_point)
        run_car_dict.pop('{}'.format(item_car_in_road_id))
        road_model[l, k] = 0
        road_dict['{}'.format(cross_road_id)] = road_model
        move_flag = 1
        return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped

    #冲突检测
    find_conflict_flag = conflict_judgment(j,k,l,car_orientation_state,cross_model,run_car_dict,road_dict)
    if find_conflict_flag ==1:  #如果找到了冲突车辆，则什么也不执行，等待,退出本程序
        return car_num_waitting, car_num_arrived, run_car_dict, road_dict, move_flag, car_num_stopped

    if car_orientation_state==1 and j==1 :
        road_model_next_id = cross_model[3]  # 直行
    if car_orientation_state==1 and j==2 :
        road_model_next_id = cross_model[4]  # 直行
    if car_orientation_state==1 and j==3 :
        road_model_next_id = cross_model[1]  # 直行
    if car_orientation_state==1 and j==4 :
        road_model_next_id = cross_model[2]  # 直行
    if car_orientation_state==2 and j==1 :
        road_model_next_id = cross_model[2]  # 左转
    if car_orientation_state==2 and j==2 :
        road_model_next_id = cross_model[3]  # 左转
    if car_orientation_state==2 and j==3 :
        road_model_next_id = cross_model[4]  # 左转
    if car_orientation_state==2 and j==4 :
        road_model_next_id = cross_model[1]  # 左转
    if car_orientation_state==3 and j==1 :
        road_model_next_id = cross_model[4]  # 右转
    if car_orientation_state==3 and j==2 :
        road_model_next_id = cross_model[1]  # 右转
    if car_orientation_state==3 and j==3 :
        road_model_next_id = cross_model[2]  # 右转
    if car_orientation_state==3 and j==4 :
        road_model_next_id = cross_model[3]  # 右转


    road_model_next = road_dict['{}'.format(road_model_next_id)]  # 找到下一条路的信息
    road_model_next_information = road_information_dict[str(road_model_next_id)]
    road_model_next_length = road_model_next_information[1]
    road_model_next_wight = road_model_next_information[3]
    road_model_next_speed = road_model_next_information[2]
    first_free_channel = 0  # 找打的第一个空位，在这里初始化为0，后面重新被赋值

    if road_model_next[0, 0] == cross_model_id:  # 判断要进入的这条路的道路矩阵，看是上半部分还是下半部分，if成立则是上半部分
        flag_crowded = 1
        for present_road_width in range(road_model_next_wight):  # 看要进入的下一路有没有空位能进入
            if road_model_next[present_road_width, 1] == 0:  # 找到一个空位则退出，当前空位为第一优先级进入空位
                first_free_channel = present_road_width
                flag_crowded = 0
                break
        if flag_crowded == 1:  # 没有空位，看下堵塞的车辆是不是全为停止状态，若是，则当前车辆也停止，否则继续等待
            crowded_car_stop_number=0
            for present_road_width in range(road_model_next_wight):  # 看要进入的下一路口的堵塞车辆是否为等待车辆
                if run_car_dict['{}'.format(road_model_next[present_road_width, 1])][2]==2:  # 堵塞车辆为停止状态
                    crowded_car_stop_number+=1
            if crowded_car_stop_number==road_model_next_wight:
                position_change = road_model[l, k]
                road_model[l, k] = 0
                if up_or_down_flag == 0:  # 原先那条路是上部分路口
                    road_model[l, road_model_length] = position_change
                else:  # 原先那条路是下部分路口
                    road_model[l, 1] = position_change
                road_dict['{}'.format(cross_road_id)] = road_model
                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                car_num_stopped += 1
                car_num_waitting -= 1
                move_flag = 1
                return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped
            else:
                return car_num_waitting, car_num_arrived, run_car_dict, road_dict, move_flag, car_num_stopped
        else:  # 有空位，继续分析看能否进入下一条路
            if up_or_down_flag==0:      #原先那条路是上部分路口
               rest_distance = road_model_length - k
            else:                       #原先那条路是下部分路口
               rest_distance = k-1
            next_road_max_speed = min(item_car_in_road_speed, road_model_next_speed)
            next_rest_distance = next_road_max_speed - rest_distance  # 找到进入下一条路后该车辆能行驶的最大距离
            if next_rest_distance <= 0:  # 最大距离小于0时，当前车辆行驶到路口尽头，无法通过路口
                change_position = road_model[l, k]
                road_model[l, k] = 0
                if up_or_down_flag == 0:  # 原先那条路是上部分路口
                    road_model[l, road_model_length] = change_position
                else:  # 原先那条路是下部分路口
                    road_model[l, 1] = change_position
                road_dict['{}'.format(cross_road_id)] = road_model
                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                car_num_stopped += 1
                car_num_waitting -= 1
                move_flag = 1
                return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped
            else:  # 最大距离大于0时，继续分析看能否进入下一条路
                flag_if_crowded_car = 0  # 看进入下一条路后，是否有阻挡车辆
                for oneof_next_rest_distance in range(1, next_rest_distance + 1):

                    if road_model_next[first_free_channel, oneof_next_rest_distance] != 0:  # 进入下一条路后，有阻挡车辆
                        flag_if_crowded_car = 1
                        last_crowded_car_id = road_model_next[first_free_channel, oneof_next_rest_distance]
                        if run_car_dict['{}'.format(last_crowded_car_id)][2] == 2:  # 有阻挡车辆，状态为终止行驶状态，则当前选择车辆能进入路口，排到阻挡车辆屁股后面
                            change_position = road_model[l, k]
                            road_model[l, k] = 0
                            road_model_next[first_free_channel, oneof_next_rest_distance - 1] = change_position
                            road_dict['{}'.format(cross_road_id)] = road_model
                            road_dict['{}'.format(road_model_next_id)] = road_model_next

                            run_car_dict['{}'.format(item_car_in_road_id)][3] = road_model_next_id  #移动到下一条路后，更新该车所在道路信息
                            run_car_dict['{}'.format(item_car_in_road_id)][2] = 2                   #移动到下一条路后，更新该车状态为停止状态
                            run_car_dict['{}'.format(item_car_in_road_id)][0] = calculate_car_orientation(item_car_in_road_id, cross_model_id, path_dict)  #更新方向

                            car_num_waitting -= 1
                            car_num_stopped += 1
                            move_flag = 1
                            print('车：', item_car_in_road_id, '+', '经过', cross_model_id)
                            break

                        else:  # 进入下一条路后，有阻挡车辆，但该车辆为等待行驶状态，则当前选择车辆无法行驶
                            break
                if flag_if_crowded_car == 1:  # 进入下一条路后，有阻挡车辆，且当前车辆已经被处理，直接遍历下一辆车
                    return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped
                else:  # 进入下一条路后，没有阻挡车辆，当前车辆进入下一个路口，移动该车
                    change_position = road_model[l, k]
                    road_model[l, k] = 0
                    road_model_next[first_free_channel, next_rest_distance] = change_position
                    road_dict['{}'.format(cross_road_id)] = road_model
                    road_dict['{}'.format(road_model_next_id)] = road_model_next

                    run_car_dict['{}'.format(item_car_in_road_id)][3] = road_model_next_id  # 移动到下一条路后，更新该车所在道路信息
                    run_car_dict['{}'.format(item_car_in_road_id)][0] = calculate_car_orientation(item_car_in_road_id,cross_model_id,path_dict)
                    run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                    car_num_waitting -= 1
                    car_num_stopped += 1
                    print('车：',item_car_in_road_id,'+','经过',cross_model_id)
                    move_flag = 1
                    return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped
    # 这里取的是下半部分
    else:
        flag_crowded = 1
        for present_road_width in range(road_model_next_wight * 2 - 1, road_model_next_wight - 1,-1):  # 看要进入的这条路有没有空位能进入
            if road_model_next[present_road_width, road_model_next_length] == 0:  # 找到一个空位则退出，当前空位为第一优先级进入空位
                first_free_channel = present_road_width
                flag_crowded = 0
                break
        if flag_crowded == 1:  # 没有空位，看下堵塞的车辆是不是全为停止状态，若是，则当前车辆也停止，否则继续等待
            crowded_car_stop_number = 0
            for present_road_width in range(road_model_next_wight * 2 - 1, road_model_next_wight - 1, -1):
                if run_car_dict['{}'.format(road_model_next[present_road_width, road_model_next_length])][2] == 2:
                     crowded_car_stop_number+=1
            if crowded_car_stop_number==road_model_next_wight:
                position_change = road_model[l, k]
                road_model[l, k] = 0
                if up_or_down_flag == 0:  # 原先那条路是上部分路口
                    road_model[l, road_model_length] = position_change
                else:  # 原先那条路是下部分路口
                    road_model[l, 1] = position_change
                road_dict['{}'.format(cross_road_id)] = road_model
                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                car_num_stopped += 1
                car_num_waitting -= 1
                move_flag = 1
                return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped
            else:
                return car_num_waitting, car_num_arrived, run_car_dict, road_dict, move_flag, car_num_stopped

        else:  # 有空位，继续分析看能否进入下一条路
            if up_or_down_flag == 0:    #原先那条路是上部分路口
                rest_distance = road_model_length - k
            else:                      #原先那条路是下部分路口
                rest_distance = k - 1
            next_road_max_speed = min(item_car_in_road_speed,road_model_next_speed)
            next_rest_distance = next_road_max_speed - rest_distance  # 找到进入下一条路后该车辆能行驶的最大距离
            if next_rest_distance <= 0:  # 最大距离小于0时，当前车辆行驶到路口尽头，无法通过路口
                change_position = road_model[l, k]
                road_model[l, k] = 0
                if up_or_down_flag == 0:  # 原先那条路是上部分路口
                    road_model[l, road_model_length] = change_position
                else:  # 原先那条路是下部分路口
                    road_model[l, 1] = change_position
                road_dict['{}'.format(cross_road_id)] = road_model
                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                car_num_waitting -= 1
                car_num_stopped += 1
                move_flag = 1
                return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped

            else:  # 最大距离大于0时，继续分析看能否进入下一条路
                flag_if_crowded_car = 0  # 看进入下一条路后，是否有阻挡车辆
                for oneof_next_rest_distance in range(road_model_next_length, road_model_next_length - next_rest_distance,-1):
                    if road_model_next[ first_free_channel, oneof_next_rest_distance] != 0:  # 进入下一条路后，有阻挡车辆
                        flag_if_crowded_car = 1
                        last_crowded_car_id = road_model_next[first_free_channel, oneof_next_rest_distance]
                        if run_car_dict['{}'.format(last_crowded_car_id)][2] == 2:  # 有阻挡车辆，状态为终止行驶状态，则当前选择车辆能进入路口，排到阻挡车辆屁股后面
                            change_position = road_model[l, k]
                            road_model[l, k] = 0
                            road_model_next[first_free_channel, oneof_next_rest_distance + 1] = change_position
                            road_dict[ '{}'.format(cross_road_id)] = road_model
                            road_dict['{}'.format( road_model_next_id)] = road_model_next

                            run_car_dict['{}'.format(item_car_in_road_id)][3] = road_model_next_id  # 移动到下一条路后，更新该车所在道路信息
                            run_car_dict[ '{}'.format(item_car_in_road_id)][2] = 2
                            run_car_dict['{}'.format(item_car_in_road_id)][0] = calculate_car_orientation(item_car_in_road_id, cross_model_id, path_dict)

                            car_num_waitting -= 1
                            car_num_stopped += 1
                            move_flag = 1
                            print('车：', item_car_in_road_id, '+', '经过', cross_model_id)
                            break

                        else:  # 进入下一条路后，有阻挡车辆，但该车辆为等待行驶状态，则当前选择车辆无法行驶
                            break
                if flag_if_crowded_car == 1:  # 进入下一条路后，有阻挡车辆，且当前车辆已经被处理，直接遍历下一辆车
                    return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped
                else:  # 进入下一条路后，没有阻挡车辆，当前车辆进入下一个路口，移动该车
                    change_position = road_model[l, k]
                    road_model[l, k] = 0
                    road_model_next[first_free_channel, road_model_next_length - next_rest_distance + 1] = change_position
                    road_dict['{}'.format(cross_road_id)] = road_model
                    road_dict['{}'.format(road_model_next_id)] = road_model_next

                    run_car_dict['{}'.format(item_car_in_road_id)][3] = road_model_next_id  # 移动到下一条路后，更新该车所在道路信息
                    run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                    run_car_dict['{}'.format(item_car_in_road_id)][0] = calculate_car_orientation(item_car_in_road_id, cross_model_id, path_dict)

                    car_num_waitting -= 1
                    car_num_stopped += 1
                    move_flag = 1
                    print('车：', item_car_in_road_id, '+', '经过', cross_model_id)
                    return car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped

print(time)
#主调度循环

time = time +1
while car_num_arrived !=(len(car_information_list)):

    car_num_waitting = 0
    car_num_stopped = 0  #记录此时间片停止的车辆数
    car_num_handed = 0
    system_dead_flag = 1  #检测系统锁死的变量，假如时间片内调度完后，一辆车都没有动，全是等待形势状态，则判断为锁死
    for i in run_car_dict.keys():    #一开始所有车辆都为等待选择状态，都没有被处理过
        run_car_dict[format(i)][2] = 0

    #此段代码跑完将有部分车将转换为终止状态，其他车为等待行驶状态
    for i in range(len(road_information_list)):  # 遍历所有道路模型
        if car_num_handed == len(run_car_dict):
            break
        road_information_1 = eval(road_information_list[i])
        road_model = road_dict['{}'.format(road_information_1[0])]
        # (id,length,speed,channel,from,to,isDuplex)
        road_id = road_information_1[0]
        road_length = road_information_1[1]
        road_speed = road_information_1[2]
        road_width = road_information_1[3]
        for j in range(0, road_width):  # 遍历正向道路
            if car_num_handed == len(run_car_dict):
                break
            for k in range(road_length ,0,-1):                  #从最前面的车开始遍历,road_length+1报错
                if car_num_handed==len(run_car_dict):
                    break
                if road_model[j, k] !=0:
                    item_car_in_road_id = road_model[j, k]
                    front_car_find_flag = 0
                    item_car_in_road_speed =car_information_dict[str(item_car_in_road_id)][3]
                    item_car_in_road_speed_max =min(item_car_in_road_speed,road_speed)
                    for p in range(k + 1,min(k + 1 + item_car_in_road_speed_max, road_length + 1)):  # 看当前道路有没有车挡在当前处理的车辆的前方
                        if road_model[j, p] != 0:  # 有阻挡车辆
                            item_front_car_in_road_id = road_model[j, p]
                            item_front_car_in_road_information = run_car_dict[
                                '{}'.format(item_front_car_in_road_id)]
                            item_front_car_in_road_state = item_front_car_in_road_information[2]
                            if item_front_car_in_road_state == 2:  # 阻挡车辆类型已经到达终止状态
                                change_position = road_model[j, k]
                                road_model[j, k] = 0
                                road_model[j, p - 1] = change_position
                                road_dict['{}'.format(road_id)] = road_model  # 当前处理车辆排到阻挡车辆的屁股后面
                                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                                front_car_find_flag = 1
                                car_num_handed +=1
                                car_num_stopped += 1
                                system_dead_flag = 0
                                break
                            else:  # 阻挡车辆类型为等待行驶状态，则这辆车也为等待行驶状态
                                front_car_find_flag = 1
                                run_car_dict['{}'.format(item_car_in_road_id)][2] = 1
                                car_num_waitting +=1
                                car_num_handed += 1
                                break

                    if front_car_find_flag == 1:  # 证明找到阻挡车辆了，当前选择车辆已经被处理，直接遍历下一辆车
                        continue
                    else:  # 没有找到阻挡车辆了，当前选择车辆没有被处理，移动该车辆
                        if item_car_in_road_speed_max + k < road_length + 1:  # 该车辆无法出路口，移动该车辆
                            change_position=road_model[j, k]
                            road_model[j, k] = 0
                            road_model[j, item_car_in_road_speed_max + k] = change_position
                            road_dict['{}'.format(road_id)] = road_model
                            run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                            car_num_handed += 1
                            car_num_stopped += 1
                            system_dead_flag = 0
                            continue
                        else:  # 该车辆能出路口，有可能到达终点，到不了则等待
                                car_end_point =car_information_dict[str(item_car_in_road_id)][2]

                                if car_end_point == road_model[0,road_length+1]:  # 车辆到达终点
                                    car_num_arrived += 1
                                    road_model[j, k] = 0
                                    run_car_dict.pop('{}'.format(item_car_in_road_id))
                                    road_dict['{}'.format(road_id)] = road_model
                                    system_dead_flag = 0
                                    print('车：', item_car_in_road_id, '+', '到达终点',car_end_point)
                                else:
                                    run_car_dict['{}'.format(item_car_in_road_id)][2] = 1    # 车辆设为等待行驶状态
                                    car_num_waitting += 1
                                    car_num_handed += 1
        # 遍历反向道路
        if road_information_1[6] != 0:   # 遍历反向道路
            for j in range(road_width * 2-1, road_width-1,-1):
                if car_num_handed==len(run_car_dict):
                    break
                for k in range(1, road_length + 1):
                    if car_num_handed == len(run_car_dict):
                        break
                    if road_model[j, k] != 0:
                        item_car_in_road_id = road_model[j, k]
                        front_car_find_flag = 0
                        item_car_in_road_speed = car_information_dict[str(item_car_in_road_id)][3]
                        item_car_in_road_speed_max = min(item_car_in_road_speed, road_speed)
                        for p in range(k -1, max(k - 1 -item_car_in_road_speed_max,0),-1):  # 看当前道路有没有车挡在当前处理的车辆的前方
                            if road_model[j, p] != 0:  # 有阻挡车辆
                                item_front_car_in_road_id = road_model[j, p]
                                item_front_car_in_road_information = run_car_dict[
                                    '{}'.format(item_front_car_in_road_id)]
                                item_front_car_in_road_state = item_front_car_in_road_information[2]
                                if item_front_car_in_road_state == 2:  # 阻挡车辆类型已经到达终止状态
                                    change_position = road_model[j, k]
                                    road_model[j, k] = 0
                                    road_model[j, p + 1] = change_position
                                    road_dict['{}'.format(road_id)] = road_model  # 当前处理车辆排到阻挡车辆的屁股后面
                                    run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                                    front_car_find_flag = 1
                                    car_num_handed += 1
                                    car_num_stopped += 1
                                    system_dead_flag = 0
                                    break
                                else:  # 阻挡车辆类型为等待行驶状态，则这辆车也为等待行驶状态
                                    front_car_find_flag = 1
                                    run_car_dict['{}'.format(item_car_in_road_id)][2] = 1
                                    car_num_waitting += 1
                                    car_num_handed += 1
                                    break

                        if front_car_find_flag == 1:  # 证明找到阻挡车辆了，当前选择车辆已经被处理，直接遍历下一辆车
                            continue
                        else:  # 没有找到阻挡车辆了，当前选择车辆没有被处理，移动该车辆
                            if  k - item_car_in_road_speed_max > 0:  # 该车辆无法出路口，移动该车辆
                                change_position = road_model[j, k]
                                road_model[j, k] = 0
                                road_model[j, k-item_car_in_road_speed_max] = change_position
                                road_dict['{}'.format(road_id)] = road_model
                                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                                car_num_handed += 1
                                car_num_stopped += 1
                                system_dead_flag = 0
                                continue
                            else:  # 该车辆能出路口，有可能到达终点，到不了则等待
                                car_end_point = car_information_dict[str(item_car_in_road_id)][2]

                                if car_end_point == road_model[0, 0]:  # 车辆到达终点
                                    car_num_arrived += 1
                                    road_model[j, k] = 0
                                    run_car_dict.pop('{}'.format(item_car_in_road_id))
                                    road_dict['{}'.format(road_id)] = road_model
                                    system_dead_flag = 0
                                    print('车：', item_car_in_road_id, '+', '到达终点',car_end_point)
                                else:
                                    run_car_dict['{}'.format(item_car_in_road_id)][2] = 1  # 车辆设为等待行驶状态
                                    car_num_waitting += 1
                                    car_num_handed += 1

    while car_num_waitting !=0:                      #再次以节点为顺序，遍历道路
        system_dead_flag2 = 1 #检测系统锁死的变量2，变量1设置有问题，先不管。假如时间片内调度完后，一辆车都没有动，全是等待形势状态，则判断为锁死
        for i in range(len(cross_information_list)):
            if car_num_waitting == 0:
                break
            cross_model = eval(cross_information_list[i])
            cross_model_id = cross_model[0]
            for j in range (1,5):
                if car_num_waitting == 0:
                    break
                cross_road_id = cross_model[j]
                if cross_road_id  == -1 :
                    continue
                road_model = road_dict['{}'.format(cross_road_id)]
                road_model_information =road_information_dict[str(cross_road_id)]
                road_model_length = road_model_information[1]
                road_model_wight = road_model_information[3]
                road_model_speed =road_model_information[2]
                test=road_model[0,road_model_length+1]
                if road_model[0,road_model_length+1] == cross_model_id:  #看当前道路是上半部分还是下半部分，这里是上半部分  判断出错？
                    for k in range(road_model_length,0,-1):
                        if car_num_waitting == 0:
                            break
                        for l in range(0,road_model_wight):
                            if car_num_waitting==0:
                                break
                            if road_model[l,k] !=0:
                                item_car_in_road_id = road_model[l,k]
                                item_car_in_road_information =run_car_dict['{}'.format(item_car_in_road_id)]
                                item_car_in_road_speed = item_car_in_road_information[1]
                                item_car_in_road_speed_max = min(item_car_in_road_speed,road_model_speed)
                                item_car_in_road_state =item_car_in_road_information[2]
                                item_car_in_road_orientation =item_car_in_road_information[0]

                                if  item_car_in_road_state ==2:     #如果这辆车已经到达终止状态，则不管它
                                    continue
                                else:                               #如果这辆车是等待行驶状态，则进行处理
                                    front_car_find_flag = 0
                                    for p in range(k+1,min(k+1+item_car_in_road_speed_max,road_model_length+1)):    #看当前道路有没有车挡在当前处理的车辆的前方
                                        if road_model[l,p] != 0 :                               #有阻挡车辆
                                            item_front_car_in_road_id=road_model[l,p]
                                            item_front_car_in_road_information = run_car_dict[
                                                '{}'.format(item_front_car_in_road_id)]
                                            item_front_car_in_road_state = item_front_car_in_road_information[2]
                                            if item_front_car_in_road_state == 2:              #阻挡车辆类型已经到达终止状态
                                                change_position = road_model[l,k]
                                                road_model[l, k] = 0
                                                road_model[l,p-1]=change_position
                                                road_dict['{}'.format(cross_road_id)]=road_model          #当前处理车辆排到阻挡车辆的屁股后面
                                                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                                                front_car_find_flag = 1
                                                car_num_waitting -=1
                                                car_num_stopped += 1
                                                system_dead_flag = 0
                                                system_dead_flag2 = 0
                                                break
                                            else:                              #阻挡车辆类型为等待行驶状态，则这辆车也为等待行驶状态
                                                front_car_find_flag = 1
                                                break

                                    if front_car_find_flag == 1:     #证明找到阻挡车辆了，当前选择车辆已经被处理，直接遍历下一辆车
                                        continue

                                    else:                           #没有找到阻挡车辆了，当前选择车辆没有被处理，移动该车辆
                                        if item_car_in_road_speed_max+k<road_model_length+1:       #该车辆无法出路口，移动该车辆
                                            change_position = road_model[l, k]
                                            road_model[l, k] = 0
                                            road_model[l, item_car_in_road_speed_max+k] = change_position
                                            road_dict['{}'.format(cross_road_id)] = road_model
                                            run_car_dict['{}'.format(item_car_in_road_id)][2]=2
                                            car_num_waitting -=1
                                            car_num_stopped += 1
                                            system_dead_flag = 0
                                            system_dead_flag2 = 0
                                            continue
                                        else:                          #该车辆能出路口，此时根据车辆是直行、左转还是右转分情况讨论
                                            car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped=car_run_next_road(j, k, l, item_car_in_road_orientation, cross_model,car_num_waitting,car_num_arrived,run_car_dict,road_dict,0,car_num_stopped)
                                            if move_flag==1:
                                                system_dead_flag=0
                                                system_dead_flag2 = 0

                else:  #看当前道路是上半部分还是下半部分，这里是下半部分
                    if road_model_information[6]==0:
                        continue
                    for k in range(1,road_model_length +1):
                        if car_num_waitting == 0:
                            break
                        for l in range(road_model_wight*2-1,road_model_wight-1,-1):
                            if car_num_waitting==0:
                                break
                            if road_model[l,k] !=0:
                                item_car_in_road_id = road_model[l,k]
                                item_car_in_road_information =run_car_dict['{}'.format(item_car_in_road_id)]
                                item_car_in_road_speed = item_car_in_road_information[1]
                                item_car_in_road_speed_max = min(item_car_in_road_speed,road_model_speed)
                                item_car_in_road_state =item_car_in_road_information[2]
                                item_car_in_road_orientation =item_car_in_road_information[0]

                                if  item_car_in_road_state ==2:     #如果这辆车已经到达终止状态，则不管它
                                    continue
                                else:                               #如果这辆车是等待行驶状态，则进行处理
                                    front_car_find_flag = 0
                                    for p in range(k-1,max(k-item_car_in_road_speed_max-1,0),-1):    #看当前道路有没有车挡在当前处理的车辆的前方
                                        if road_model[l,p] != 0 :                               #有阻挡车辆
                                            item_front_car_in_road_id=road_model[l,p]
                                            item_front_car_in_road_information = run_car_dict[
                                                '{}'.format(item_front_car_in_road_id)]
                                            item_front_car_in_road_state = item_front_car_in_road_information[2]
                                            if item_front_car_in_road_state == 2:              #阻挡车辆类型已经到达终止状态
                                                change_position = road_model[l,k]
                                                road_model[l, k] = 0
                                                road_model[l,p+1]=change_position
                                                road_dict['{}'.format(cross_road_id)]=road_model          #当前处理车辆排到阻挡车辆的屁股后面
                                                run_car_dict['{}'.format(item_car_in_road_id)][2] = 2
                                                front_car_find_flag = 1
                                                car_num_waitting -=1
                                                car_num_stopped += 1
                                                system_dead_flag = 0
                                                system_dead_flag2 = 0
                                                break
                                            else:                              #阻挡车辆类型为等待行驶状态，则这辆车也为等待行驶状态
                                                front_car_find_flag = 1
                                                break

                                    if front_car_find_flag == 1:     #证明找到阻挡车辆了，当前选择车辆已经被处理，直接遍历下一辆车
                                        continue

                                    else:                           #没有找到阻挡车辆了，当前选择车辆没有被处理，移动该车辆
                                        if k-item_car_in_road_speed_max>=1:       #该车辆无法出路口，移动该车辆
                                            change_position = road_model[l, k]
                                            road_model[l, k] = 0
                                            road_model[l,k-item_car_in_road_speed_max] = change_position
                                            road_dict['{}'.format(cross_road_id)] = road_model
                                            run_car_dict['{}'.format(item_car_in_road_id)][2]=2
                                            car_num_waitting -=1
                                            car_num_stopped += 1
                                            system_dead_flag = 0
                                            system_dead_flag2 = 0
                                            continue
                                        else:                          #该车辆能出路口，此时根据车辆是直行、左转还是右转分情况讨论
                                            car_num_waitting,car_num_arrived,run_car_dict,road_dict,move_flag,car_num_stopped=car_run_next_road(j, k, l, item_car_in_road_orientation, cross_model,car_num_waitting, car_num_arrived,run_car_dict,road_dict,1,car_num_stopped)
                                            if move_flag==1:
                                                system_dead_flag=0
                                                system_dead_flag2 = 0
        if system_dead_flag2 == 1:
            print('系统锁死')
            sys.exit()

    if system_dead_flag==1:
        print('系统锁死')
        sys.exit()

    list_car_time = sorted(list_car_time, key=lambda list_car_time: eval(list_car_time)[4])
    run_car_new_dict =creat_new_run_car_dict(list_car_time,time,path_dict)
    run_car_new_list = sorted(run_car_new_dict.items(), key=lambda item: item[0])

    if len(run_car_new_dict)!=0:
        for i in range(len(run_car_new_list)):  # 遍历run_car_dict,将车辆安排上路
            car_initial_id = int(run_car_new_list[i][0])

            car_initial_information = car_information_dict[str(car_initial_id)]  # 获取派车上路所需信息
            start_point = car_initial_information[1]
            car_initial_speed = car_initial_information[3]
            car_initial_orientation = path_dict['{}'.format(car_initial_id)][1][1]
            car_start_road = cross_information_dict[str(start_point)][car_initial_orientation]
            road_model = road_dict['{}'.format(car_start_road)]
            car_road_information = road_information_dict[str(car_start_road)]
            car_road_length = car_road_information[1]
            road_speed = car_road_information[2]
            car_initial_speed = min(car_initial_speed, road_speed)

            if road_model[0, 0] == start_point:  # 如果所派车辆，所在道路为正向道路
                flag_no_free_channel = 1
                flag_car_front_find = 0
                for channel in range(car_road_information[3]):  # 如果车进入的车道有空位，将车安排上去
                    if road_model[channel, 1] == 0:
                        flag_no_free_channel = 0
                        if flag_car_front_find==1:
                            break
                        for go_ahead_length in range(1, car_initial_speed + 1):
                            if road_model[channel, go_ahead_length] != 0:
                                road_model[channel, go_ahead_length - 1] = car_initial_id
                                road_dict['{}'.format(car_start_road)] = road_model
                                flag_car_front_find = 1
                                break

                        if flag_car_front_find == 0:
                            road_model[channel, car_initial_speed] = car_initial_id  # 若进入车道没车，车辆进入最大空位处
                            road_dict['{}'.format(car_start_road)] = road_model
                            break
                if flag_no_free_channel == 1:  # 若车道无空位，车辆信息重新进入list_car_time
                    run_car_new_dict.pop('{}'.format(car_initial_id))
                    car_initial_information_list = list(car_initial_information)
                    car_initial_information_list[4] = time + 1
                    #print(car_initial_information_list)
                    car_initial_information_list = [str((car_initial_information_list[0],
                                                         car_initial_information_list[1],
                                                         car_initial_information_list[2],
                                                         car_initial_information_list[3],
                                                         car_initial_information_list[4]))]
                    list_car_time = car_initial_information_list + list_car_time

            else:  # 如果所派车辆，所在道路为反向道路
                flag_no_free_channel = 1
                flag_car_front_find = 0
                for channel in range(car_road_information[3] * 2 - 1, car_road_information[3] - 1, -1):
                    if road_model[channel, car_road_length] == 0:
                        flag_no_free_channel = 0
                        if flag_car_front_find==1:
                            break
                        for go_ahead_length in range(car_road_length, car_road_length - car_initial_speed,-1):
                            if road_model[channel, go_ahead_length] != 0:
                                road_model[channel, go_ahead_length + 1] = car_initial_id
                                road_dict['{}'.format(car_start_road)] = road_model
                                flag_car_front_find = 1
                                break

                        if flag_car_front_find == 0:
                            road_model[channel, car_road_length - car_initial_speed + 1] = car_initial_id  # 车的坐标需要检查，+1还是减1
                            road_dict['{}'.format(car_start_road)] = road_model
                            break

                if flag_no_free_channel == 1:
                    run_car_new_dict.pop('{}'.format(car_initial_id))
                    car_initial_information_list = list(car_initial_information)
                    car_initial_information_list[4] = time+1
                    #print(car_initial_information_list)
                    car_initial_information_list = [str((car_initial_information_list[0],car_initial_information_list[1],car_initial_information_list[2],car_initial_information_list[3],car_initial_information_list[4]))]
                    list_car_time = car_initial_information_list + list_car_time
        run_car_dict.update(run_car_new_dict)

    list_car_time = sorted(list_car_time,key=lambda list_car_time: (eval(list_car_time)[4], eval(list_car_time)[0]))
    time +=1
    print(time)
    if time>1000:
        break

print("全国第一")
