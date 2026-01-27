import json
import sys
from pathlib import Path

def load_ids(path: Path):
    """把 JSON 文件里所有出现的 id 收集到一个 set 中返回。"""
    data = json.loads(path.read_text(encoding='utf-8'))
    ids = set()
    # 支持对象或数组
    if isinstance(data, list):
        for item in data:
            if 'id' in item:
                ids.add(str(item['id']).strip())
    elif isinstance(data, dict):
        if 'id' in data:
            ids.add(str(data['id']).strip())
    return ids

def dedup(input_a: Path, input_b: Path, output_c: Path):
    """执行去重并写入新文件。"""
    ids_in_b = load_ids(input_b)
    data_a = json.loads(input_a.read_text(encoding='utf-8'))

    # 根据外层类型分别处理
    if isinstance(data_a, list):
        new_data = [item for item in data_a
                    if str(item.get('id', object())).strip() not in ids_in_b]
    elif isinstance(data_a, dict):
        new_data = data_a if str(data_a.get('id', object())).strip() not in ids_in_b else None
        if new_data is None:
            new_data = {}
    else:
        raise TypeError('仅支持 JSON 数组或对象格式！')

    output_c.write_text(json.dumps(new_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'已去重，结果保存至：{output_c.resolve()}')

def main():
    if len(sys.argv) != 4:
        print('用法：python dedup_json_id.py <input_A> <input_B> <output_C>')
        sys.exit(1)

    input_a = Path(sys.argv[1])
    input_b = Path(sys.argv[2])
    output_c = Path(sys.argv[3])

    if not input_a.exists() or not input_b.exists():
        print('错误：输入文件不存在！')
        sys.exit(1)

    dedup(input_a, input_b, output_c)

if __name__ == '__main__':
    main()