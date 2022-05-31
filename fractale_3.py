from select import select
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

#figureの初期化
def initialize(size_figure):

    figure = plt.axes()

    #figureの表示設定
    #範囲指定
    plt.xlim(-0.5,size_figure-0.5)
    plt.ylim(-0.5,size_figure-0.5)
    #グラフの表示を正方形にする
    figure.set_aspect('equal')
    
    return figure


#２点の直線を引く
def draw_line(coordinate, head_point, tail_point):

    coordinate[head_point[0]][head_point[1]] = 1
    coordinate[tail_point[0]][tail_point[1]] = 1

    search_mid_point(coordinate, head_point, tail_point)


#中間点を求める
def search_mid_point(coordinate, head_point, tail_point):

    if abs(head_point[0] - tail_point[0]) <= 1 and abs(head_point[1] - tail_point[1]) <= 1:
        return

    y = int((head_point[0] + tail_point[0])/2)
    x = int((head_point[1] + tail_point[1])/2)
    
    coordinate[y][x] = 1

    search_mid_point(coordinate, head_point, (y, x))
    search_mid_point(coordinate, (y, x), tail_point)


#i番目とi+1番目の点を結ぶ線を引く　０番目とｎ番目には同じ座標が入っている
def draw_figure(coordinate, points):

    n = len(points)

    for i in range(n-1):
        head_point = points[i]
        tail_point = points[i+1]
        draw_line(coordinate, head_point, tail_point)


#n-1角形のデータを作成
#データ形式　([頂点１],[頂点２],...[頂点ｎ],[頂点１])
#最初と最後には同じ座標を入れる
def make_polygon(vertex_points, size_figure, number_polygon):

    Ratio = 0.3
    radius = size_figure*Ratio

    t = np.linspace(0, np.pi*2 ,number_polygon)
    x = np.fix(radius*np.cos(t) + size_figure/2)
    y = np.fix(radius*np.sin(t) + size_figure/2)

    for i in range(number_polygon):
        vertex_points[i][0] = y[i]
        vertex_points[i][1] = x[i]


#直線の方程式ax+b = yよりaを求める
#直線の方程式を以下のように変形してa,bを求める
#           0 = x*a + b  - y
#垂直、水平の場合は計算せずフラグで管理する
def search_slope(head_point,tail_point):

    Vertical_Flag = False
    Horizontal_Flag = False
    slope = 0

    a = sp.Symbol('a')
    b = sp.Symbol('b')
    equation_1 = a*head_point[1]+b - head_point[0]
    equation_2 = a*tail_point[1]+b - tail_point[0]

    if head_point[1] == tail_point[1]:
        Vertical_Flag = True
    elif head_point[0] == tail_point[0]:
        Horizontal_Flag = True
    else:
        solution = sp.solve([equation_1,equation_2])
        slope = float(solution[a])

    return Vertical_Flag, Horizontal_Flag, slope


#垂直か水平の時,内側か外側か判断する
def judge_inside_VH(I_Flag, value, base, step):

    dist_1 = abs(base-value)
    dist_2 = abs(base-(value+step))
    
    if I_Flag == 0:#初回の呼び出しの時
        if dist_1 > dist_2:#内側に点が発生した場合
            I_Flag = -1
        else:#外側の時
            I_Flag = 1
    
    elif I_Flag == -1:#初回の発生が内側だった場合
        if dist_1 > dist_2:#今回も内側だった場合
            pass
        else:#外側だった場合
            step = -1*step

    else:#初回の発生が外側だった場合　I_Flag=1
        if dist_1 > dist_2:#今回も内側だった場合
            step = -1*step
        else:#外側だった場合
            pass

    return step, I_Flag

def judge_inside(I_Flag, base, points):

    Selected_Flag = -1

    dist_1 = ((points[0][0]-base)**2 + (points[0][1]-base)**2)**0.5
    dist_2 = ((points[1][0]-base)**2 + (points[1][1]-base)**2)**0.5
    
    if I_Flag == 0:#初回の呼び出しの時
        if np.random.randint(0,10,1)%2 == 0:#乱数で内か外か決める
            I_Flag = -1#内側
        else:
            I_Flag = 1#外側
    
    if I_Flag == -1:#初回の発生が内側だった場合
        if dist_1 > dist_2: #距離が短い方を採用
            Selected_Flag = 1
        else:
            Selected_Flag = 0

    if I_Flag == 1:#初回の発生が外側だった場合
        if dist_1 > dist_2:#距離が長い方を採用
            Selected_Flag = 0
        else:#外側だった場合
            Selected_Flag = 1

    return Selected_Flag, I_Flag


def extract_coordinate(x, y, a, b, step):

    mid_x = sp.Symbol('mid_x')
    step = abs(step)
    equation = ((x-mid_x)**2 + (y-(mid_x*a+b))**2)**0.5 - step
    solution = sp.solve(equation)

    candidate_points = np.zeros([2,2])
    
    for i in range(2):
        tmp_data = solution[i][mid_x]
        string_data = str(tmp_data)
        x_data = float(string_data)
        y_data = a*x_data+b

        candidate_points[i][0] = y_data
        candidate_points[i][1] = x_data

    return candidate_points




#引数の直線の垂直二等分線上の点の座標を求める
def search_new_vertex(I_Flag, V_Flag, H_Flag, slope, head_point, tail_point, size_figure, random_number):

    y = int((head_point[0] + tail_point[0])/2)
    x = int((head_point[1] + tail_point[1])/2)
    base = size_figure/2
    step = size_figure*random_number
    
    if V_Flag == True:
        step, I_Flag = judge_inside_VH(I_Flag, x, base, step)
        x += step
    elif H_Flag == True:
        step, I_Flag = judge_inside_VH(I_Flag, y, base, step)
        y += step
    else:
        orthogonal_slope = -1/slope
        intercept = -1*orthogonal_slope*x + y

        candidate_points = extract_coordinate(x, y, orthogonal_slope, intercept, step)

        Selected_Flag, I_Flag = judge_inside(I_Flag, base, candidate_points)

        y = candidate_points[Selected_Flag][0]
        x = candidate_points[Selected_Flag][1]
        

    y, x = int(y), int(x)

    return y, x, I_Flag


#フラクタルデータを生成する
def make_fractale_data(mid_data_number, points, size_figure):

    random_number = np.random.normal(0,0.05,1)
    mid_vertex_points = np.zeros([mid_data_number,2], dtype=np.int32)
    Inside_Flag = 0

    for i in range(mid_data_number):
        V_Flag, H_Flag, slope = search_slope(points[i], points[i+1])

        new_y, new_x, Inside_Flag = search_new_vertex(Inside_Flag, V_Flag, H_Flag, slope, points[i], points[i+1], size_figure, random_number)

        mid_vertex_points[i][0] = new_y
        mid_vertex_points[i][1] = new_x

    return mid_vertex_points


#新しい頂点データを作成する
def make_new_vertex_points(new_data_number, points, mid_vertex_points):

    new_vertex_points = np.zeros([new_data_number,2], dtype=np.int32)

    count, mid_count = 0, 0

    for i in range(new_data_number):
        if i%2 == 0:
            new_vertex_points[i] = points[count]
            count += 1
        else:
            new_vertex_points[i] = mid_vertex_points[mid_count]
            mid_count +=1

    return new_vertex_points


def make_one_lap_fractale(points, size_figure):

    data_number = len(points)
    mid_data_number = data_number-1
    new_data_number = mid_data_number+data_number

    mid_vertex_points = make_fractale_data(mid_data_number, points, size_figure) 

    new_vertex_points = make_new_vertex_points(new_data_number, points, mid_vertex_points)

    return new_vertex_points

#フラクタルデータを作成する
def make_fractale(points, size_figure):

    for i in range(2):
        points = make_one_lap_fractale(points, size_figure)

    return points
    

def main():

    #グラフの大きさ
    size_figure = 512

    #n-1角形
    number_polygon = np.random.randint(4,10)

    #頂点データの初期化
    vertex_points = np.zeros([number_polygon,2], dtype=np.int32)

    #座標データの初期化
    coordinate = np.zeros([size_figure,size_figure])
    figure = initialize(size_figure)

    #ｎ角形の頂点データを作成
    make_polygon(vertex_points, size_figure, number_polygon)

    #draw_figure(coordinate, vertex_points)

    #ｎ角形の頂点データをもとにフラクタルを作成
    vertex_points = make_fractale(vertex_points, size_figure)

    #データをもとに作図する
    draw_figure(coordinate, vertex_points)

    #グレイスケール化
    plt.imshow(coordinate,cmap="Greys")
    plt.show()

#ax + b = y
if __name__ == '__main__':
    main()