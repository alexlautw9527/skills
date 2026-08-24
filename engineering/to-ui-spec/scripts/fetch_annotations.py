#!/usr/bin/env python3
"""抓取 Figma node 子樹內的所有 native annotations。

用法：
    FIGMA_ACCESS_TOKEN=xxx python3 fetch_annotations.py <fileKey> <nodeId[,nodeId...]>

- 一次 REST 請求串接所有 node id（GET /v1/files/:key/nodes?ids=...）。
- Annotation 通常掛在子孫節點（常在 instance 內部節點）上，因此對每個
  回傳的 document 樹做遞迴走訪收集，而非只看頂層節點。
- REST 的 `label` 只有純文字，hyperlink 會丟失。script 只做粗抓，不負責還原連結。
"""

import html
import json
import os
import sys
import urllib.request


def walk(node, path, out):
    name = node.get('name', '')
    current = path + [name] if name else path
    for ann in node.get('annotations') or []:
        entry = {
            'nodeId': node.get('id'),
            'path': '/'.join(current[1:]),  # 不含被查詢的 root 名稱
        }
        if 'label' in ann:
            entry['label'] = html.unescape(ann['label'])
        if ann.get('properties'):
            entry['properties'] = ann['properties']
        if ann.get('categoryId'):
            entry['categoryId'] = ann['categoryId']
        out.append(entry)
    for child in node.get('children') or []:
        walk(child, current, out)


def main():
    if len(sys.argv) != 3:
        sys.exit(f'usage: {sys.argv[0]} <fileKey> <nodeId[,nodeId...]>')
    token = os.environ.get('FIGMA_ACCESS_TOKEN')
    if not token:
        sys.exit('FIGMA_ACCESS_TOKEN not set')

    file_key = sys.argv[1]
    ids = ','.join(i.strip().replace('-', ':') for i in sys.argv[2].split(','))
    url = f'https://api.figma.com/v1/files/{file_key}/nodes?ids={ids}'

    req = urllib.request.Request(url, headers={'X-Figma-Token': token})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    result = {}
    for node_id, wrapper in (data.get('nodes') or {}).items():
        doc = (wrapper or {}).get('document') or {}
        found = []
        walk(doc, [], found)
        result[node_id] = {'name': doc.get('name'), 'annotations': found}

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == '__main__':
    main()
