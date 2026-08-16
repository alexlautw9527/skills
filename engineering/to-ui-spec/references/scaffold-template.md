# Scaffold 模板

建立 `.stuff.md` 時，整份文件依此模板產出。本檔只定義 scaffold 的結構，以及 `來源：` 與 `### Sources` 可接受的格式。

模板內的 `` ```hint `` 區塊是產出說明。依照說明建立文件，但不要把 hint 留在產出中。

---

````markdown
# <文件名稱>

## Reading Guide

本檔為 UI 規格 scaffold。每個 Section 的 `來源：` 填主要 Figma node；`### Sources` 只補充 Section 子孫 node 以外的 Figma node URL、Markdown 圖片或可存取圖片路徑，每項各佔一行。沒有補充資料時留空。整理來源資料時會自動取得主要來源 node 及其子孫 node 的 native annotations，不需手動貼入 `### Sources`。

## <Section 名稱>

```hint
每個已確認的 Section 建立一個 `##` 區塊。標題使用 Figma 原文。
```

來源：[<Figma titlePath 或 name>](<直接連結>)

```hint
一個 Section 對應多個 Figma node 時，每個 node 各寫一行 `來源：`。
```

### Sources

```hint
補充資料區，可留空。每項各佔一行。
```

## Questions

```hint
建立 scaffold 時留空。第 3 階段整理來源資料時依 source-rules.md 判斷需要建立的 Question。
```
````
