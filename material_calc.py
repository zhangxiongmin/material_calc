from flask import Flask, render_template, request, jsonify
import math
# 创建templates文件夹并在其中创建index.html文件
import os

# 用于存储计算历史的列表
calculation_history = []

# 单位换算函数
def mm_to_m(mm):
    """将毫米转换为米"""
    return mm / 1000.0

def calculate_volume(shape, params):
    """计算不同形状的体积(立方米)"""
    if shape == '圆棒':
        radius = mm_to_m(float(params['radius'])) / 2  # 直径转半径
        length = mm_to_m(float(params['length1']))
        return math.pi * (radius ** 2) * length
        
    elif shape == '圆管':
        outer_radius = mm_to_m(float(params['outer_diameter'])) / 2
        inner_radius = mm_to_m(float(params['inner_diameter'])) / 2
        length = mm_to_m(float(params['length2']))
        return math.pi * (outer_radius ** 2 - inner_radius ** 2) * length
        
    elif shape == '方料':
        length = mm_to_m(float(params['length3']))
        width = mm_to_m(float(params['width']))
        height = mm_to_m(float(params['height']))
        return length * width * height
        
    elif shape == '方管':
        outer_length = mm_to_m(float(params['outer_length']))
        outer_width = mm_to_m(float(params['outer_width']))
        inner_length = mm_to_m(float(params['inner_length'])) 
        inner_width = mm_to_m(float(params['inner_width']))
        height = mm_to_m(float(params['height']))
        outer_area = outer_length * outer_width
        inner_area = inner_length * inner_width
        return (outer_area - inner_area) * height

# 确保templates文件夹存在
if not os.path.exists('templates'):
    os.makedirs('templates', exist_ok=True)

# 创建默认的index.html文件(如果不存在)
if not os.path.exists('templates/index.html'):
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('index.html')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        shape = request.form.get('shape')
        density = float(request.form.get('density'))*1000.0  # 转换为kg/m³
        price = float(request.form.get('price'))
        
        # 使用calculate_volume函数统一处理体积计算
        params = {}
        for key in request.form:
            if key not in ['shape', 'density', 'price']:
                params[key] = request.form.get(key)
                
        volume = calculate_volume(shape, params)
        weight = volume * density  # 计算重量(kg)
        total_price = weight * price  # 计算总价格
        
        # 将计算结果添加到历史记录中
        result = {
            'shape': shape,
            'weight': round(weight, 3),
            'total_price': round(total_price, 2)
        }
        
        return jsonify({
            'weight': round(weight, 3),
            'total_price': round(total_price, 2)
        })
    except (TypeError, ValueError) as e:
        return jsonify({'error': '请输入有效的数值'}), 400

if __name__ == '__main__':
    app.run(debug=True)
