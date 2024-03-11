from flask import render_template, request, Flask
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

## use this page to uplad fmri
@app.route('/upload')
def template():
    return render_template('upload.html')

## submit the fmri, and render the analysis result
@app.route('/fmri/analysis', methods= ['POST'])
def analysis():
    f = request.files["file"]
    file_name = f.filename
    f.save(f"temporary/{file_name}")
    ## TODO 拿到前段页面上传的文件以后，调用分析 fmri 图片，获取spacing数据，渲染页面
    return "长:300mm, 宽40mm, 高:50mm, 坐标:44,66"