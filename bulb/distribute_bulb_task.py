import cv2
import numpy as np
from bulb import param_bulb

def mouseEvents(event, x, y, flags, points):
    #左クリックした場合、その座標を保管
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])

def distribute_task(values):

    img = np.zeros((300,640,3))
    button_positions = []
    baseX = 20
    diffX = 140
    baseY = 45
    diffY = 70

    for y in range(3):
        for x in range(1):
            pos_x = baseX+diffX*x
            pos_y = baseY+diffY*y
            button_positions.append((pos_x, pos_y))
    button_width = 400
    button_height = 50
    
    for i, pos in enumerate(button_positions):
        top_left = pos
        bottom_right = (top_left[0] + button_width,
                        top_left[1] + button_height)

        # 白でボタンを描画
        cv2.rectangle(img, top_left, bottom_right, (255, 255, 255), -1)

        # ボタン上にテキストを描画
        cv2.putText(img, values[i], (top_left[0] + 10, top_left[1] + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    points=[]
    cv2.imshow("Choose bulb situation",img)
    cv2.setMouseCallback("Choose bulb situation",mouseEvents,points)
    while True:
        key=cv2.waitKey(1)
        if len(points)>0:
            X, Y = points[-1]

            # ボタンのクリック位置に応じた値を返す
            # for i, pos in enumerate(button_positions):
            #     top_left = pos
            #     bottom_right = (top_left[0] + rect_width, top_left[1] + rect_height)
            #     if top_left[0] <= X < bottom_right[0] and top_left[1] <= Y < bottom_right[1]:
            #         if i < len(values):  # 有効な値の範囲内の場合
            #             cv2.destroyAllWindows()
            #             return i  # クリックしたボタンに対応する値を返す
            for i, pos in enumerate(button_positions):
                top_left = pos
                bottom_right = (top_left[0] + button_width,top_left[1] + button_height)
                if top_left[0] <= X <= bottom_right[0] and top_left[1] <= Y <= bottom_right[1]:
                    if i < len(values):  # 有効な値の範囲内の場合
                        print(f"Button {i+1} clicked, sending image to {values[i]}")
                        cv2.destroyAllWindows()
                        if i != 2:
                            v = 100
                            print(i)
                            print(type(v))
                            
                            return i, v
                        else:
                            param = ["Open","Close"]
                            img = np.zeros((240,640,3))
                            txt = param_bulb.choose_param(img,param)
                            return i,txt
def main():

    # n = initialize()
    # print(n)
    # image_path = "/home/ros/ros2_ws/src/pressure/data/0908_results/bw_test_1.jpg"
    

    # 各ボタンに対応するテキスト
    texts = ["BAR_value","ROUND_Value","OPEN or CLOSE"]
    
    # img = cv2.imread(image_path)
    num = distribute(texts)
    print(texts[num])

if __name__ == "__main__":
    main()
