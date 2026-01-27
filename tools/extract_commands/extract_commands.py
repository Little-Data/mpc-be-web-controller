"""
从 index.html 提取所有 data-command 属性值并输出为 JSON 数组
用法: python extract_commands.py [path/to/index.html] > commands.json
"""

import re
import json
import sys
from pathlib import Path

def extract_data_commands(html_path: str) -> list:
    """提取所有 data-command 值并返回 [{id: value}, ...]"""
    content = Path(html_path).read_text(encoding='utf-8')
    # 匹配 data-command="数字"
    pattern = re.compile(r'data-command="(\d+)"')
    ids = sorted({int(m) for m in pattern.findall(content)})
    return [{"id": str(i)} for i in ids]

def main():
    html_file = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
    if not Path(html_file).is_file():
        sys.stderr.write(f'文件不存在: {html_file}\n')
        sys.exit(1)
    data = extract_data_commands(html_file)
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()