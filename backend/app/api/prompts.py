"""
Prompts API - CRUD for prompt templates
"""

from flask import jsonify, request
from . import prompts_bp
from ..prompts.prompt_loader import get_all_prompts, save_prompts, reset_prompts


@prompts_bp.route('', methods=['GET'])
def get_prompts():
    """Get all prompt templates."""
    try:
        prompts = get_all_prompts()
        return jsonify({'success': True, 'data': prompts})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@prompts_bp.route('', methods=['PUT'])
def update_prompts():
    """Update prompt templates."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        save_prompts(data)
        return jsonify({'success': True, 'message': 'Prompts updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@prompts_bp.route('/reset', methods=['POST'])
def reset_to_defaults():
    """Reset prompts to defaults."""
    try:
        reset_prompts()
        prompts = get_all_prompts()
        return jsonify({'success': True, 'data': prompts, 'message': 'Reset to defaults'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
