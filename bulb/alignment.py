import cv2
import numpy as np

def align_images_ecc(img1, img2):
    """
    findTransformECC を使って img2 を img1 にアライメント（重ね合わせ）する関数
    """
    # 画像をグレースケールに変換
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 画像サイズを取得
    sz = img1.shape

    # 初期変換行列を設定 (3x3 の単位行列)
    warp_matrix = np.eye(3, 3, dtype=np.float32)

    # ECC の収束条件を設定
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-6)

    # ECC アルゴリズムで変換行列を求める（ホモグラフィ行列）
    (cc, warp_matrix) = cv2.findTransformECC(img1_gray, img2_gray, warp_matrix, cv2.MOTION_HOMOGRAPHY, criteria)

    # 求めたホモグラフィ行列で画像を射影変換
    aligned_img = cv2.warpPerspective(img2, warp_matrix, (sz[1], sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    return aligned_img, warp_matrix

# 画像を読み込み
img1 = cv2.imread("/home/ros/ros2_ws/image1.png")  # 基準となる画像（ベース画像）
img2 = cv2.imread("/home/ros/ros2_ws/image2.png")  # 重ね合わせたい画像
h,w = img1.shape[:2]
print(h,w)
img2 = cv2.resize(img2,(w,h))
# サイズを合わせてアライメントを実行
aligned_img, homography_matrix = align_images_ecc(img1, img2)

# 結果を表示
cv2.imshow("Base Image1", img1)
cv2.imshow("Base Image2", img2)
# cv2.imshow("Aligned Image", aligned_img)
cv2.imshow("Aligned Image", aligned_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
