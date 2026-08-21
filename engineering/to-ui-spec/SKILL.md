---
name: to-ui-spec
description: 將 Figma 畫面整理成可審查的 UI 規格：提出 Section Outline、建立 .stuff.md、自動取得 native annotations、CRUD 正式 .ux.md。提供 Figma URL、要求確認 Section、補充來源，或要求建立、讀取、更新、刪除 UI 規格時使用。
---

將使用者選定的 Figma 畫面整理成可審查的 UI 規格。工作固定分成四個階段，前一階段的產出直接作為下一階段的輸入：

| 階段 | 輸入 | 產出 |
| --- | --- | --- |
| 1. 提出 Section Outline | 含 node id 的 Figma root URL | 使用者已確認的 Section Outline；每項包含 `nodeId`、`titlePath` 與直接連結 |
| 2. 建立 scaffold | 已確認的 Section Outline | `.stuff.md`；供使用者補充額外的 Figma node URL 與手動截圖 |
| 3. 整理來源資料 | 使用者確認 `### Sources` 已補充完成或不需補充的 `.stuff.md` | 依 Section 整理的來源資料；預設包含各主要來源 node 及其子孫 node 的 native annotations |
| 4. CRUD 正式規格 | 第 3 階段的整理結果，或使用者指定的既有 `.ux.md` | 建立、讀取、更新或刪除正式規格的結果 |

`Section Outline` 是供使用者確認的 Section 拆分大綱。`CRUD 正式規格` 包含建立、讀取、更新與刪除 `.ux.md`。

每次回覆都在開頭標示目前階段與具體狀態：

```text
目前階段：<提出 Section Outline｜建立 scaffold｜整理來源資料｜CRUD 正式規格>
狀態：<已完成的結果、正在執行的工作，或等待使用者提供的內容>
```

狀態必須讓使用者知道目前已有什麼結果，以及下一步由誰處理。禁止只寫「進行中」「等待中」或「已完成」。

依目前輸入決定從哪個階段開始，再按需讀取下列 reference：

- 提出 Section Outline：不讀模板，也不讀 annotation 或畫面內容。
- 建立 scaffold：讀完 [scaffold-template.md](references/scaffold-template.md)。
- 整理來源資料：讀完 [scaffold-template.md](references/scaffold-template.md) 與 [source-rules.md](references/source-rules.md)。
- CRUD 正式規格：讀完 [formal-template.md](references/formal-template.md)。若變更依賴新的 Figma 或圖片來源，先完成第 3 階段。

各檔案只負責一類規則：

| 檔案 | 負責內容 |
| --- | --- |
| `SKILL.md` | 選擇流程、呼叫工具、修改檔案及處理失敗 |
| `scaffold-template.md` | 定義 `.stuff.md` 的結構，以及每個來源欄位可接受的格式 |
| `source-rules.md` | 判斷每個 Section 可以採用哪些資料，以及資料應寫入哪個欄位 |
| `formal-template.md` | 定義 `.ux.md` 的欄位、類型、排列及編號 |

## 判定與分流

| 已知輸入 | 執行流程 |
| --- | --- |
| 既有 `.ux.md` 與讀取、更新或刪除要求 | 第 4 階段；更新若依賴新來源，先執行第 3 階段 |
| 既有 `.stuff.md` 路徑 | 第 3 階段，再將整理結果交給第 4 階段 |
| Figma URL 與既有 scaffold | 第 3 階段；Figma URL 只補足 scaffold 已列出的 Section 來源 |
| 已確認的 Section Outline | 第 2 階段 |
| Figma root URL，尚未確認 Section Outline | 第 1 階段 |
| Figma URL 缺少 node id | 在第 1 階段取得頁面目錄，請使用者指定 root node |

使用者確認 Section Outline 前不得進入第 2 階段。建立 scaffold 時不得讀 annotation。使用者確認 `### Sources` 已完成後才能進入第 3 階段；native annotations 由第 3 階段自動取得，不需手動貼入 `### Sources`。第 4 階段只能使用第 3 階段的整理結果或既有 `.ux.md`。

## 判斷檔案位置

依下列順序判斷輸出路徑：

1. 使用者指定的路徑。
2. 目前專案的 `AGENTS.md`、`CLAUDE.md` 或其他明確規範。
3. 同一專案既有 `.stuff.md` 與 `.ux.md` 的目錄配置。
4. 找不到慣例時，提出 `<spec-root>/<screen-slug>/` 形式的候選路徑，等使用者確認後再建立。

檔名只使用畫面的穩定英文 kebab-case slug：

- scaffold：`<screen-slug>.stuff.md`
- 正式規格：`<screen-slug>.ux.md`
- 文件標題使用畫面名稱，不加序號。
- 新增、插入或刪除畫面時，不改既有目錄與檔名。

不得把固定專案名稱、功能名稱或規格根目錄寫成此 skill 的通用規則。

## 1. 提出 Section Outline

### 取得 Layers 目錄

使用 `get_metadata` 讀取使用者指定的 root node：

1. 從回傳 XML 只保留每個圖層的 `id` 與 `name`。
2. 將 root 視為第 1 層，最多保留 4 層，但不把 root 列為候選 Section。
3. 為 root 以下每個圖層建立 `{ nodeId, titlePath }`。`titlePath` 從 root 的直接子層開始，以 `/` 串接 `name`。
4. 依 XML 開關標籤維護父層 stack。解析完成時 stack 必須為空；否則視為回應不完整。

探勘期間不得呼叫 `use_figma`、`get_design_context` 或 `get_screenshot`，也不得讀 annotation、文字、樣式或 prototype。

### 組成 Section Outline 並請使用者確認

- 依可獨立閱讀與驗收的畫面、流程或狀態提出 Section 拆分建議。
- 合併重複結構，排除純排版圖層與元件內部圖層。
- 使用 ASCII tree，格式為 `[nodeId] titlePath`；候選 Section 放在第一層，不輸出 root。
- 不輸出 XML 或完整圖層清單。使用者要求時才補充未列入的 node。
- XML 不完整或無法解析時，請使用者提供範圍較小的 Figma node URL，不得猜測缺少內容。
- 使用者確認後，產出最終 Section Outline。每個 Section 必須包含 `nodeId`、`titlePath` 與直接連結，再將這份 Outline 交給第 2 階段。

## 2. 建立 scaffold

讀完 [scaffold-template.md](references/scaffold-template.md)，再執行：

1. 檢查 Section Outline 的每個 Section 都有 `nodeId`、`titlePath` 與直接連結。缺少任一欄位時返回第 1 階段補齊。
2. 以 `titlePath` 作為 `來源：` 連結文字，Section 標題保留 Figma 原文。
3. 依「判斷檔案位置」決定 `.stuff.md` 路徑。
4. 按 scaffold 模板建立整份文件，不加入 UI 驗收項或 Question 內容。
5. 告知使用者可在各 Section 的 `### Sources` 補充額外的 Figma node URL 與手動截圖。第 3 階段會自動取得主要來源 node 及其子孫 node 的 native annotations，不需手動加入。
6. 等使用者確認補充完成或不需補充後，再以 `.stuff.md` 路徑進入第 3 階段。

## 3. 整理來源資料

讀完 [scaffold-template.md](references/scaffold-template.md) 與 [source-rules.md](references/source-rules.md)，再依序執行。

### 1. 解析 Section 來源

- 解析每個 Section `來源：` 與 `### Sources` 中的 Figma URL，取得 file key 與 node id。
- URL 缺少 node id 時，建立 Question，且不讀取該檔案的其他 node。
- 將每筆來源資料記錄到所屬 Section，後續不得混用其他 Section 的資料。

### 2. 取得 native annotations

有 `FIGMA_ACCESS_TOKEN` 時，先用 REST 列出 annotation，再用 MCP 還原連結：

1. 執行 `python3 <skill-dir>/scripts/fetch_annotations.py <fileKey> <nodeId,nodeId…>`。同一 file key 的 Section 來源 node 與 `### Sources` 額外列出的 Figma node id 要合併成一次請求。
2. 腳本會遞迴走訪每個查詢 node 的子孫 node，輸出 `{nodeId, path, label}`。REST 回應可能達數十 MB，不得直接使用 `curl` 或將原始回應讀進對話。
3. 先讀完 `figma-design-to-code` skill。接著針對 REST 清單中的每個 annotation `nodeId` 各呼叫一次 `get_design_context`；各 node 可以獨立處理且工具支援並行呼叫時，同時送出多個呼叫。這一步只需要 annotation 原文，因此設定 `excludeScreenshot: true`。
4. 呼叫 `get_design_context` 時，將 `skillNames` 設為 `figma-design-to-code`。此參數只供 MCP 服務記錄本次呼叫遵循的 skill，不會載入 skill，也不會修改 Figma 檔案；呼叫工具前仍須先讀完該 skill。
5. 從每次回傳 code 的 `data--annotations` 取得 annotation 的 Markdown 原文，保留其中的文字與 URL，並用它取代 REST 的純文字 `label`。REST 的 `properties` 列出 annotation 釘選的 node 屬性，例如寬度、填色或字級；這個欄位不含 URL。

來源：

- `skillNames` 的用途依目前環境中 `get_design_context` MCP tool schema 的參數說明。
- [Figma MCP：get_design_context](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/#get_design_context)
- [Figma Plugin API：Annotation](https://developers.figma.com/docs/plugins/api/Annotation/)
- [Figma REST API：AnnotationProperty](https://developers.figma.com/docs/rest-api/file-property-types/#annotationproperty)

不得對 Section 根或過大的子樹反覆呼叫 `get_design_context`。這類呼叫通常只回傳零散 metadata，無法取得子孫 node 的 annotations。

沒有 `FIGMA_ACCESS_TOKEN` 時，使用 `get_metadata` 列出各 Section 來源 node 的子孫 node，再將查詢拆成 MCP 可處理的大小，逐步尋找 `data--annotations`。不得擴大到 Section 未列出的其他來源 node。

### 3. 產生來源整理結果

1. 依 `source-rules.md` 將每筆資料標成可轉成 UI 驗收項的要求、Question，或操作後開啟畫面的 Figma 連結。
2. 依 Section 保留原始文字、URL 與來源位置，讓第 4 階段可以追溯每項內容。
3. 將來源整理結果交給第 4 階段，不在本階段建立或修改 `.ux.md`。

## 4. CRUD 正式規格

讀完 [formal-template.md](references/formal-template.md)。CRUD 分別表示建立、讀取、更新與刪除正式 `.ux.md`。

### 建立

1. 使用第 3 階段的來源整理結果，依 `formal-template.md` 建立完整 `.ux.md`。
2. 目標檔案已存在時，改用「更新」流程。只有使用者明確要求重新產生整份規格時，才以本次結果取代原內容。
3. 保留 `.stuff.md` 原內容，只在 Reading Guide 補上「已整理為 `<filename>.ux.md`，內容以正式檔為準」。已存在相同說明時不要重複加入。

### 讀取

- 讀取使用者指定的 `.ux.md`，依要求說明、摘要或檢查內容。
- 讀取操作不得修改 `.ux.md`、`.stuff.md` 或其他引用檔案。

### 更新

1. 先讀取既有 `.ux.md`，保留未受本次要求影響的 Section、UI 驗收項與人工 Review 狀態。
2. 更新若依賴新的 Figma node、annotation 或圖片，先執行第 3 階段，再用新的來源整理結果修改對應內容。
3. 只修改使用者指定或受新來源影響的內容，並維持 `formal-template.md` 的欄位、排序與編號規則。
4. UI ID 改變時，依「更新 UI ID 引用」同步修改其他檔案。

### 刪除

1. 只有使用者明確指定要刪除的 `.ux.md` 或 UI 驗收項時才執行。
2. 刪除前確認目標路徑或 UI ID，並搜尋其他 `.ux.md` 對該目標的引用。
3. 同步移除或更新引用後再刪除目標。除非使用者一併指定，否則保留對應 `.stuff.md`。

### 更新 UI ID 引用

新增、刪除或重編 UI ID 後，使用 `rg` 搜尋舊 ID 並更新：

1. 先搜尋目前 `.ux.md` 所在目錄及其子目錄。
2. 再搜尋本檔 `關聯：` 所連到的其他 `.ux.md` 所在目錄及其子目錄。
3. 無法確定引用範圍時，搜尋目前 workspace 內全部 `*.ux.md`。

同步更新 `###` heading、`關聯：`、`受影響 UI 驗收項` 與跨檔 Markdown 連結文字。

## Risks

- Figma URL 缺 node id：建立 Question 或請使用者指定 node，不猜測目標。
- `get_metadata` 回傳的 XML 不完整：請使用者提供較小的 node，不補寫缺少圖層。
- 補充圖片只存在於對話：請使用者把圖片或可存取路徑加入對應 `### Sources`。
- 來源資料存在但無法判斷可觀察結果：建立 Question，說明還缺什麼。
- Section 沒有 annotation 或有效補充資料：依 `source-rules.md` 保留 Section 標題與來源，不自行推測需求。
- Annotation 連到其他 Figma node：把 URL 寫入驗證步驟，但不因此讀取該 node 的內容。

## Validation

### 1. 提出 Section Outline

- 最多輸出 4 層 `nodeId` 與 `titlePath`。
- 省略 root，並以 ASCII tree 請使用者確認 Section Outline。
- 已確認的每個 Section 都包含 `nodeId`、`titlePath` 與直接連結。
- 確認前未建立檔案，也未讀取 annotation 或畫面內容。

### 2. 建立 scaffold

- 輸入是已確認的 Section Outline。
- 文件符合 `scaffold-template.md`。
- `來源：` 連結文字可直接辨識 node，且未加入 UI 驗收項或 Question 內容。
- 已告知使用者只需補充額外來源與手動截圖，native annotations 會在第 3 階段自動取得。

### 3. 整理來源資料

- 只採用 `source-rules.md` 允許的資料。
- 預設取得每個主要來源 node 及其子孫 node 的 native annotations。
- 來源整理結果依 Section 保留原始文字、URL 與來源位置。

### 4. CRUD 正式規格

- 建立與更新後的文件符合 `formal-template.md`，且不含 scaffold hints 或 `### Sources`。
- 建立與更新時已保留 `data--annotations` 內的 URL，圖片連結文字描述畫面或標註內容，不使用檔名或路徑。
- 更新與刪除造成 UI ID 或檔案引用變化時，相關引用已同步修改，且搜尋不到應淘汰的舊引用。
- 讀取操作沒有修改檔案。
- 刪除操作只處理使用者明確指定的目標，未被指定的 `.stuff.md` 仍然保留。
