from flask import render_template, request, Flask ,jsonify
import logging
import SimpleITK as sitk
import numpy as np
from scipy.ndimage import label
import os
import base64

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

## use this page to uplad fmri
@app.route('/upload')
def template():
    return render_template('upload.html')

@app.route('/fmri/convert2pic', methods = ['POST'])
def convert2pic():
    f = request.files["file"]
    file_name = f.filename
    temp_path = f"temporary/{file_name}"
    f.save(temp_path)
    ##TODO convert nil_image to pic 

    ## 获取 pic的bytes字节流，转化为base64字符串，前端展示
    with open('temporary/WechatIMG15.jpg', 'rb') as file:
        file_bytes = file.read()
    base64_data = base64.b64encode(file_bytes).decode('utf-8')
     # 清理临时文件
    os.remove(temp_path)
    return base64_data

## submit the fmri, and render the analysis result
# @app.route('/fmri/analysis', methods= ['POST'])
# def analysis():
#     f = request.files["file"]
#     file_name = f.filename
#     # f.save(f"temporary/{file_name}")
#     temp_path = f"temporary/{file_name}"
#     f.save(temp_path)
#
#     # 使用 SimpleITK 读取并处理图像
#     reader = sitk.ImageFileReader()
#     reader.SetFileName(temp_path)
#     image = reader.Execute()
#
#     # 转换为 numpy 数组并计算体积
#     imageArr = sitk.GetArrayFromImage(image)
#     counts = np.sum(imageArr != 0)  # 计算图像中所有非零像素的数量
#     spacing = image.GetSpacing()
#     unitVol = np.prod(spacing)
#     roiVol = round(unitVol * counts,3)
#
#     # 清理临时文件
#     os.remove(temp_path)
#
#     # 返回结果
#     return f"结节的体素数：{counts}，结节体积: {roiVol} 立方毫米"
    ## TODO 拿到前段页面上传的文件以后，调用分析 fmri 图片，获取spacing数据，渲染页面
    # return "长:300mm, 宽40mm, 高:50mm, 坐标:44,66"

@app.route('/fmri/analysis', methods= ['POST'])
def analysis():
    f = request.files["file"]
    file_name = f.filename
    # f.save(f"temporary/{file_name}")
    temp_path = f"temporary/{file_name}"
    f.save(temp_path)
    # 使用 SimpleITK 读取并处理图像
    reader = sitk.ImageFileReader()
    reader.SetFileName(temp_path)
    mask = reader.Execute()

    # 将掩膜图像转换为数组
    maskArr = sitk.GetArrayFromImage(mask)

    # 使用label函数标记连通域（结节）
    labeled_array, num_features = label(maskArr)

    # 计算体积
    spacing = mask.GetSpacing()
    unitVol = np.prod(spacing)
    roiVols = [np.sum(labeled_array == i) * unitVol for i in range(1, num_features + 1)]

    volumes = [{'volume': round(vol,3)} for vol in roiVols]
    total_volume = round(sum(roiVols))
    return jsonify(volumes=volumes, total_volume=total_volume)