"""
Prompt configuration loader.
Loads prompts from prompts.json, falls back to prompts_default.json.
"""

import json
import os
import copy

_dir = os.path.dirname(os.path.abspath(__file__))
_default_path = os.path.join(_dir, 'prompts_default.json')
_custom_path = os.path.join(_dir, 'prompts.json')

_prompts = None

def _load():
    global _prompts
    # Load defaults first
    with open(_default_path, 'r', encoding='utf-8') as f:
        defaults = json.load(f)

    # Override with custom if exists
    if os.path.exists(_custom_path):
        try:
            with open(_custom_path, 'r', encoding='utf-8') as f:
                custom = json.load(f)
            # Deep merge: custom overrides defaults
            _prompts = _deep_merge(defaults, custom)
        except (json.JSONDecodeError, IOError):
            _prompts = defaults
    else:
        _prompts = defaults

def _deep_merge(base, override):
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result

def get_prompt(category, key):
    """Get a prompt by category and key. E.g. get_prompt('ontology', 'system')"""
    if _prompts is None:
        _load()
    return _prompts.get(category, {}).get(key, '')

def get_all_prompts():
    """Get all prompts as a dict."""
    if _prompts is None:
        _load()
    return copy.deepcopy(_prompts)

def save_prompts(data):
    """Save custom prompts to prompts.json."""
    with open(_custom_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Reload
    _load()

def reset_prompts():
    """Reset to defaults by removing prompts.json."""
    if os.path.exists(_custom_path):
        os.remove(_custom_path)
    _load()

def reload():
    """Force reload prompts from disk."""
    _load()
