from flask import Flask, request, send_file, jsonify, render_template_string
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# 업로드된 파일을 저장할 디렉토리
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB 제한

# uploads 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 허용할 파일 확장자
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'mp4', 'mp3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 간단한 HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>파일 전송 서버</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .upload-area { 
            border: 2px dashed #ccc; 
            padding: 20px; 
            text-align: center; 
            margin: 20px 0;
            border-radius: 10px;
        }
        .file-list { margin: 20px 0; }
        .file-item { 
            padding: 10px; 
            border: 1px solid #ddd; 
            margin: 5px 0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        button { 
            padding: 10px 20px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover { background: #0056b3; }
        .download-btn { background: #28a745; }
        .download-btn:hover { background: #1e7e34; }
    </style>
</head>
<body>
    <div class="container">
        <h1>파일 전송 서버</h1>
        
        <div class="upload-area">
            <h3>파일 업로드</h3>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" multiple accept="*/*">
                <br><br>
                <button type="submit">업로드</button>
            </form>
        </div>
        
        <div class="file-list">
            <h3>업로드된 파일 목록</h3>
            <div id="fileList"></div>
        </div>
    </div>

    <script>
        // 파일 업로드
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                alert(result.message);
                loadFileList();
            } catch (error) {
                alert('업로드 실패: ' + error.message);
            }
        });

        // 파일 목록 로드
        async function loadFileList() {
            try {
                const response = await fetch('/files');
                const files = await response.json();
                
                const fileList = document.getElementById('fileList');
                fileList.innerHTML = '';
                
                files.forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span>${file.name} (${file.size})</span>
                        <button class="download-btn" onclick="downloadFile('${file.name}')">다운로드</button>
                    `;
                    fileList.appendChild(fileItem);
                });
            } catch (error) {
                console.error('파일 목록 로드 실패:', error);
            }
        }

        // 파일 다운로드
        function downloadFile(filename) {
            window.open(`/download/${filename}`, '_blank');
        }

        // 페이지 로드 시 파일 목록 로드
        loadFileList();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        files = request.files.getlist('file')
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                continue
                
            if file and allowed_file(file.filename):
                # 파일명 보안 처리
                filename = secure_filename(file.filename)
                
                # 중복 파일명 처리
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    name, ext = os.path.splitext(filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{name}_{timestamp}{ext}"
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files.append(filename)
        
        if uploaded_files:
            return jsonify({
                'message': f'{len(uploaded_files)}개 파일이 성공적으로 업로드되었습니다.',
                'files': uploaded_files
            })
        else:
            return jsonify({'error': '업로드할 수 있는 파일이 없습니다.'}), 400
            
    except Exception as e:
        return jsonify({'error': f'업로드 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return jsonify({'error': '파일을 찾을 수 없습니다.'}), 404

@app.route('/files')
def list_files():
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                size_mb = round(size / (1024 * 1024), 2)
                files.append({
                    'name': filename,
                    'size': f'{size_mb} MB' if size_mb > 1 else f'{round(size / 1024, 2)} KB'
                })
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': f'파일 목록을 가져오는 중 오류가 발생했습니다: {str(e)}'}), 500

if __name__ == '__main__':
    print("파일 전송 서버가 시작됩니다...")
    print("웹 브라우저에서 http://localhost:5000 에 접속하세요")
    app.run(debug=True, host='0.0.0.0', port=5000)