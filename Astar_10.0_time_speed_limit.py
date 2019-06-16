import re
import numpy as np
import copy

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

def creat_new_run_car_dict(list_car_time,time,path_dict):
    run_car_new_dict = {}
    while eval(list_car_time[0])[4] == time:

        item = str(eval(list_car_time[0])[0])
        if len(path_dict[item]) <= 2:
            run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select]
            list_car_time.pop(0)
            continue
        else:
            car_orientation_1 = path_dict[item][1][1]
            car_orientation_2 = path_dict[item][2][1]
            car_speed = eval(list_car_time[0])[3]
            if car_orientation_1 == 1 and car_orientation_2 == 1:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 1 and car_orientation_2 == 2:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 1 and car_orientation_2 == 4:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 2 and car_orientation_2 == 1:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 2 and car_orientation_2 == 2:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 2 and car_orientation_2 == 3:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 3 and car_orientation_2 == 2:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 3 and car_orientation_2 == 3:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 3 and car_orientation_2 == 4:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 4 and car_orientation_2 == 1:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_right, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 4 and car_orientation_2 == 3:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [turn_left, car_speed, wait_select]
                list_car_time.pop(0)
                continue
            if car_orientation_1 == 4 and car_orientation_2 == 4:
                run_car_new_dict['{}'.format(eval(list_car_time[0])[0])] = [go_straight, car_speed, wait_select]
                list_car_time.pop(0)
                continue
    return run_car_new_dict

def calculate_car_orientation(car_id,present_cross_id,path_dict):
    car_path = path_dict['{}'.format(car_id)]
    for i in range(len(car_path)):
        if car_path[i][0] == present_cross_id:
            if i+1 >= len(car_path)-1:
                return 1
            else:
                car_orientation_1 = car_path[i+1][1]
                car_orientation_2 = car_path[i +2][1]
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

def car_current_limiting(road_path_limit_time,fo):

    time=1
    flag =0
    first_road_path=[]
    final_road_path =[]
    road_path_limit_time_copy=road_path_limit_time[:]             #生成一个新的road_path_list_time
    for i in range(len(road_path_limit_time)):                             #遍历新表
        if len(road_path_limit_time_copy) == 0:                           #当我新表不存在元素时退出
            break
        if  road_path_limit_time[min(i+1,len(road_path_limit_time)-1)][1] != time :          #在i+1位的车的出发时间与当前时间不符，表明已经找到所以当前时间出发的车
            for j in range(i+1):                                                #将当前时间点出发的车提取出来
                if len(road_path_limit_time_copy) == 0:
                    break
                first_road_path.append(road_path_limit_time_copy.pop(0))
            first_road_path=sorted(first_road_path,key=lambda x:x[2],reverse=True)           #对当前时间点能出发的车进行速度排序
            for k in range(min(15,len(first_road_path))):          #选取速度在前“”的车，进入最终表，余下的车进入下一time，与下一time的车进行速度比较
                final_road_path.append(first_road_path.pop(0))
            if len(road_path_limit_time_copy) == 0:      #当road_path_limit_time_copy没有元素时，first_road_path里的元素全都加人final_road_path表
                for p in range(len(first_road_path)):
                    final_road_path.append(first_road_path.pop(0))

            time+=1


    time =1            #时间重置

    while len(final_road_path) !=0:
        path = final_road_path.pop(0)
        path.pop(2)
        if path[1] ==time:
            path =tuple(path)
            print(path)
            fo.write(str(path))
            fo.write('\n')
            flag += 1
            while flag==14:
                time +=1
                flag =0
        elif path[1] >time:
            path =tuple(path)
            print(path)
            fo.write(str(path))
            fo.write('\n')
            time +=1
        else:
            path[1]= time
            path =tuple(path)
            print(path)
            fo.write(str(path))
            fo.write('\n')
            flag += 1
            while flag==14:
                time +=1
                flag =0
    fo.close()

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
        h0 = self.f_value_tem([best, 0, 0, 0,0,0])
        init_open = [best, 0, 0, h0,0,0]
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
                tow_point_road_id_list.append(self.car[3])
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
car_information_list = read_file('car.txt')
road_information_dict = information_list_transform_dict(road_information_list)
cross_information_dict = information_list_transform_dict(cross_information_list)
car_information_dict = information_list_transform_dict(car_information_list)
cross_sideweight_dict,cross_oritation_dict=creat_dict_sideweight_oritation(road_information_dict,cross_information_dict)
cross_site_position=orientational_x_y_dict(road_information_dict,cross_information_list,cross_information_dict )




path_dict = {}
road_dict ={}

fo =open('anwser_2.txt','w',encoding='utf-8')
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

road_path_limit_time = []


for i in range(0,len(car_information_list)):                                #生成车辆行驶路径
    car_in_all = eval(car_information_list[i])
    k = AStar(road_information_dict, cross_information_dict, car_in_all, cross_sideweight_dict, cross_oritation_dict,cross_site_position )
    cross_path,road_path = k.main()
    path_dict['{}'.format(car_in_all[0])] = cross_path
   # fo.write(str(road_path))
    #fo.write('\n')
    road_path_limit_time.append(road_path)

road_path_limit_time.sort(key=lambda x:x[1])

car_current_limiting(road_path_limit_time,fo)



