from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_code
from refactor import refactor_code
from tester import test_code
import difflib

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Analyze code for issues."""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        issues = analyze_code(code)
        return jsonify({'issues': issues})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refactor', methods=['POST'])
def api_refactor():
    """Refactor code based on issues."""
    try:
        data = request.json
        code = data.get('code', '')
        issues = data.get('issues', [])
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        refactored = refactor_code(code, issues)
        is_valid = test_code(code, refactored)
        
        return jsonify({
            'refactored_code': refactored,
            'is_valid': is_valid
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diff', methods=['POST'])
def api_diff():
    """Get diff between original and refactored code."""
    try:
        data = request.json
        original = data.get('original', '')
        refactored = data.get('refactored', '')
        
        diff = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            refactored.splitlines(keepends=True),
            fromfile='Original',
            tofile='Refactored'
        ))
        
        return jsonify({'diff': ''.join(diff)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """Validate code syntax."""
    try:
        data = request.json
        code = data.get('code', '')
        
        is_valid = test_code(code, code)
        return jsonify({'is_valid': is_valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
