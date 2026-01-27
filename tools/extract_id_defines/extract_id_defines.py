import pathlib
import sys

# 1. 需要扫描的后缀
EXTS = {'.txt', '.h', '.hpp', '.c', '.cpp', '.cc'}

# 2. 输出文件
OUT_FILE = 'id_defines.txt'

def main():
    root = pathlib.Path('.').resolve()
    lines_out = []

    # 遍历目录树
    for file in root.rglob('*'):
        if file.suffix.lower() not in EXTS:
            continue
        try:
            with file.open('r', encoding='utf-8', errors='ignore') as f:
                for raw in f:
                    stripped = raw.lstrip()
                    if stripped.startswith('#define ID_'):
                        lines_out.append(raw.rstrip('\n'))
        except OSError as e:
            print(f'Warn: 无法读取 {file} , {e}', file=sys.stderr)

    # 写入结果
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines_out))

    print(f'提取完成，共 {len(lines_out)} 条，已保存到 {OUT_FILE}')

if __name__ == '__main__':
    main()