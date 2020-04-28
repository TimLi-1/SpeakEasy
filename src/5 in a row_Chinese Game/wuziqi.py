# -*- coding: utf-8 -*-
from math import sin, cos, pi

class Wuziqi:
    def __init__(self, size):
        self.size = size
        self.max_value = 0
        self.next_point = [7, 7]
        self.list_qi = [] # list_qi[r][c]表示r行，c列的值：0无棋，2白棋（AI）,1黑棋（玩家）
        self.list_v = [] # 表示该点的权值
        for i in range(self.size):
            list_11 = [0] * self.size
            list_22 = [0] * self.size
            self.list_qi.append(list_11)
            self.list_v.append(list_22)
            
        # 各种棋型对应的权值 1：玩家，2：AI，进攻为主
        self.value_dic = {"": 1, "0": 1, "1": 10, "2": 60, "02": 20, "21": 6, "12": 3, "221": 200, "112": 30,
                          "202": 300, "101": 30, "22": 600, "11": 100, "2_2": 300,
                          "111": 7000, "222": 20000, "22_22" : 3000, "11_11": 1000,
                          "1112": 300, "2221": 2000, "0111": 200, "0222": 1500,
                          "1111": 40000, "2222": 90000, "12221": 0, "21112": 0}
        
    def reset(self):
        for r in range(self.size):
            for c in range(self.size):
                self.list_qi[r][c] = 0
                self.list_v[r][c] = 0

    # AI获得每一个点下子的价值并选择最大价值处下子
    def get_value(self):
        self.max_value = 0
        list_1 = ['101', '011', '01101', '01102', '011011', '011012']
        list_2 = ['202', '022', '02202', '02201', '022022', '022021']
        list_3 = ['0111', '1011', '1101', '1110']
        list_4 = ['0222', '2022', '2202', '2220']
        
        
        for r in range(self.size):
            for c in range(self.size):
                self.list_v[r][c] = 0 
                # 如果该点没有下子，则考察其八个方向的已有棋子的情况
                if self.list_qi[r][c] == 0:
                    code = [''] * 8
                    # 对每个空位点遍历8个方向，查找棋子分布代码
                    for j in range(8):
                        x = int(1.5 * cos(j* pi/4))
                        y = int(1.5 * sin(j* pi/4))
                        last_qi = 0
                        number_of_0 = 0
                        before_0 = 0
                        # 每个方向取4个邻居，形成代码
                        for i in range(1,6):
                            rr = r+ x*i
                            cc = c+ y*i
                            if rr in range(self.size) and cc in range(self.size):
                                # 计算0的个数，有两个0就截止
                                if self.list_qi[rr][cc] == 0:
                                    number_of_0 += 1
                                    if code[j]:
                                        before_0 = last_qi
                                if number_of_0 == 2  or self.list_qi[rr][cc] + before_0 == 3: # 102，1012截止
                                    break
                                
                                code[j] += str(self.list_qi[rr][cc])

                                # 112截止
                                if self.list_qi[rr][cc] + last_qi == 3:
                                    break
                                last_qi = self.list_qi[rr][cc]
                                
                            # 碰到边界则当做此处有对方棋子
                            else:
                                if last_qi == 1:
                                    code[j] += '2'
                                elif last_qi == 2:
                                    code[j] += '1'
                                break
                        # 边界问题
                        if not code[j]:
                            code[j] = '3'
                            
                        # 去掉末尾的0
                        if code[j]:
                            if code[j][-1] == '0':
                                code[j] = code[j][:-1]

                    # 考虑边界
                    for j in range(8):
                        if code[j] == '3':
                            if j < 4:
                                if code[j+4][:0] == '1':
                                    code[j] = '2'
                                if code[j+4][:0] == '2':
                                    code[j] = '1'
                            else:
                                if code[j-4][:0] == '1':
                                    code[j] = '2'
                                if code[j-4][:0] == '2':
                                    code[j] = '1'

                    # 考虑连接两边的情况
                    for j in range(4,8):
                        if code[j] + code[j-4] == '22':
                            code[j] = '22'
                            code[j-4] = ''
                        elif code[j] + code[j-4] == '11':
                            code[j] = '11'
                            code[j-4] = ''
                            
                        elif code[j] + code[j-4] == '221' or code[j-4] + code[j] == '221':
                            code[j] = '221'
                            code[j-4] = ''

                        elif code[j] + code[j-4] == '112' or code[j-4] + code[j] == '112':
                            code[j] = '112'
                            code[j-4] = ''

                        elif code[j] + code[j-4] == '222':
                            code[j] = '222'
                            code[j-4] = ''
                        elif code[j] + code[j-4] == '111':
                            code[j] = '111'
                            code[j-4] = ''

                        elif (code[j] + code[j-4]) in list_1 or (code[j-4] + code[j]) in list_1:
                            code[j] = '101'
                            code[j-4] = ''
                        elif (code[j] + code[j-4]) in list_2 or (code[j-4] + code[j]) in list_2:
                            code[j] = '202'
                            code[j-4] = ''

                        elif code[j] + code[j-4] == '2221' or code[j-4] + code[j] == '2221':
                            code[j] = '2221'
                            code[j-4] = ''
                        elif code[j] + code[j-4] == '1112' or code[j-4] + code[j] == '1112':
                            code[j] = '1112'
                            code[j-4] = ''

                        else:
                            for k in range(5):
                                if code[j][:k] + code[j-4][:(4-k)] == '1111':
                                    code[j] = '1111'
                                    code[j-4] = ''
                                elif code[j][:k] + code[j-4][:(4-k)] == '2222':
                                    code[j] = '2222'
                                    code[j-4] = ''
                                    
                                elif (code[j][:k] + code[j-4][:(4-k)]) in list_3:
                                    code[j] = '0111'
                                    code[j-4] = ''
                                elif (code[j][:k] + code[j-4][:(4-k)]) in list_4:
                                    code[j] = '0222'
                                    code[j-4] = ''
                                              
                            for k in range(4):
                                try:
                                    if (code[j][k] + code[j-4][3-k]) == '11' or (code[j][k] + code[j-4][2-k]) == '11':
                                        code[j] = '12221'
                                        code[j-4] = ''
                                    if (code[j][k] + code[j-4][3-k]) == '22' or (code[j][k] + code[j-4][2-k]) == '22':
                                        code[j] = '21112'
                                        code[j-4] = ''
                                except:
                                    pass

         
                    # 判断不在一条直线上的两个11,11和22，22 以及 11,1112和22,2221
                    if code.count("2221") + code.count("0222") > 1:
                        try:
                            code[code.index('2221')] = "2222"
                        except:
                            code[code.index('0222')] = "2222"
                    elif code.count("1112") + code.count("0111") > 1:
                        try:
                            code[code.index('1112')] = "1111"
                        except:
                            code[code.index('0111')] = "1111"
                    
                    elif code.count("2221") + code.count("0222") > 0 and code.count("202") + code.count("22") > 0:
                        try:
                            code[code.index('2221')] = "222"
                        except:
                            code[code.index('0222')] = "222"
                    elif code.count("1112") + code.count("0111") > 0 and code.count("101") + code.count("11") > 0:
                        try:
                            code[code.index('1112')] = "111"
                        except:
                            code[code.index('0111')] = "111"

                    elif code.count("202") + code.count("22") > 1:
                        try:
                            code[code.index('202')] = "22_22"
                        except:
                            code[code.index('22')] = "22_22"
                    elif code.count("101") + code.count("11") > 1:
                        try:
                            code[code.index('101')] = "11_11"
                        except:
                            code[code.index('11')] = "11_11"
                            
                    # 前期进攻加成，还待开发。。。
                    if "2" in code:
                        if code.count('2') + code.count("02") > 1:
                            code[code.index('2')] = "2_2"
                            
                                    
                    # 计算每一点下子的价值            
                    for j in range(8):
                        while True:
                            try:
                                self.list_v[r][c] += self.value_dic[code[j]]
                                break
                            except:
                                code[j] = code[j][:-1]
                        if self.value_dic[code[j]] > 100:
                            print(r,c,code[j],'----',self.value_dic[code[j]])
                                
                # 获取最大价值及其位置
                if self.max_value < self.list_v[r][c]:
                    self.max_value = self.list_v[r][c]
                    self.next_point[0] = r
                    self.next_point[1] = c

        # 下一步
        self.list_qi[self.next_point[0]][self.next_point[1]] = 2
        print('next_step: ', self.next_point, self.max_value, '\n')
#        for r in range(self.size):
#            for c in range(self.size):
#                print("%5d" % self.list_v[r][c], end = '')
#            print('')
#        print('')
                            

    # 检查是否五子连珠
    def check_fivepots(self):
        self.max_value = 0
        for r in range(self.size):
            for c in range(self.size):
                self.list_v[r][c] = 0 
                if self.list_qi[r][c] != 0:
                    for j in range(8):
                        x = int(1.5 * cos(j* pi/4))
                        y = int(1.5 * sin(j* pi/4))
                        num = 1
                        for i in range(1,5):
                            rr = r+ x*i
                            cc = c+ y*i
                            if rr in range(self.size) and cc in range(self.size):
                                if self.list_qi[rr][cc] == self.list_qi[r][c]:
                                    num +=1
                        if num == 5:
                            self.max_value = -1                    

