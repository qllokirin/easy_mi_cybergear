
import keyboard
from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>简易控制面板</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        .control-panel {
            display: inline-block;
            margin: 20px;
        }
        .direction-pad {
            display: grid;
            grid-template-columns: repeat(3, 80px);
            grid-template-rows: repeat(3, 80px);
            gap: 5px;
            margin-bottom: 20px;
        }
        button {
            width: 100%;
            height: 100%;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background-color: #f0f0f0;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: #ddd;
        }
        .go {
            grid-column: 2;
            grid-row: 1;
        }
        .left {
            grid-column: 1;
            grid-row: 2;
        }
        .right {
            grid-column: 3;
            grid-row: 2;
        }
        .back {
            grid-column: 2;
            grid-row: 3;
        }
        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        .action-btn {
            padding: 15px 30px;
            background-color: #4CAF50;
            color: white;
        }
        .action-btn.stop {
            background-color: #f44336;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            background-color: #e7f3fe;
            border-radius: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <h1>简易控制面板</h1>
    <div class="control-panel">
        <div class="direction-pad">
            <button class="go" onclick="sendCommand('go')">↑</button>
            <button class="left" onclick="sendCommand('left')">←</button>
            <button class="right" onclick="sendCommand('right')">→</button>
            <button class="back" onclick="sendCommand('back')">↓</button>
        </div>
        
        <div class="action-buttons">
            <button class="action-btn" onclick="sendCommand('stand')">立正</button>
            <button class="action-btn stop" onclick="sendCommand('lie_down')">趴下</button>
        </div>
        
        <div class="status" id="status">
            等待指令...
        </div>
    </div>
    
    <script>
        function sendCommand(command) {
            fetch('/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({command: command})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').innerText = data.message;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


current_state = 'lie_down'
@app.route('/command', methods=['POST'])
def handle_command():
    global current_state
    data = request.get_json()
    command = data.get('command', '')
    current_state = command
    return {'message': command}

@app.route('/current_state', methods=['GET'])
def get_state():
    return {'current_state': current_state}

if __name__ == '__main__':
    app.run(debug=True)