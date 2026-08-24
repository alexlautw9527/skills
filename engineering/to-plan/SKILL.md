---
name: to-plan
description: 依功能規格與目前系統的實際架構，產出可直接開始實作的跨平台計畫。規劃前端、後端、全端、mobile、API、服務、CLI 或跨 repository 功能，且需要切分可驗證的行為 slice、查證實作位置與建立需求追溯關係時使用。
---
> 執行本 skill 時，預設一併讀取 `make-ai-readable-zh` skill。

依功能規格確認預期行為，並從目前環境查證實作位置、責任邊界與可沿用模式。計畫涵蓋達成行為所需的系統範圍，不預設功能只屬於前端、後端、mobile 或單一 repository。

## Inputs

先取得下列材料：

- 使用者指定或目前環境可確認的功能規格，例如需求文件、issue、acceptance criteria、ui design、API 規格或架構決策。
- 被同一個可觀察行為碰到的 app、服務、package、repository 或其他部署單位中的程式碼、設定、測試與專案指示文件。
- 本次交付範圍、負責的開發職能，以及使用者指定的交付形式與存放位置。

功能規格決定預期行為。目前程式碼只用來確認實作位置、責任邊界與可沿用模式。規格中的技術建議不能當成現況，所有路徑、module、symbol、資料流與既有流程都要從目前環境查證。

外部介面由其他文件維護時，計畫只記錄實作者需要理解的資料語意、失敗情境、介面邊界與正式串接前必讀的規格位置。不要複製或推測 schema、欄位、operation、錯誤代碼、版本策略或相容策略。

資訊不足時，依影響分類：

- 不影響可觀察行為、slice 邊界、順序、資料正確性、安全性、責任歸屬或完成條件的未知資訊，可以依目前證據繼續規劃。
- 可能改變上述任一項的未知資訊，列入 `Questions`，寫明目前採用的前提與受影響的 slice。缺少的資訊會造成不同可觀察行為時，只提出一個能解除目前阻礙的問題。

使用者未指定交付形式時，確認要在回覆中提供計畫，或寫入檔案。寫入檔案前取得確切路徑的確認；只讀探索不必等待這項確認。

## Output

預設交付一份 Markdown 計畫，依序包含：

1. `Scope`
2. `Questions`，只有存在會影響規劃的未知資訊時才加入。
3. `Map`
4. `Constraints and Invariants`
5. `Prerequisites`，只有有必要前置工作時才加入。
6. `Shared Concerns`，只有兩個以上 slice 共同依賴既有前提時才加入。
7. `slices`
8. `Coverage`

除非使用者另外要求，不要加入估點、結案報告、commit 切分，或不對應可觀察產品行為的附錄。本 skill 只負責研究與規劃，不修改產品程式碼。

### 單檔與拆檔

預設將全部內容寫在同一份計畫中。slice 的排列順序就是實作順序，Coverage 使用 Markdown 連結指向同一份文件的 slice heading。

使用者明確要求拆檔時，所有檔案放在同一個目錄。使用者未指定目錄名稱時，可以使用 `<feature>--plan/`；`<feature>` 取自功能規格或目前環境可確認的名稱，並轉成小寫英文 kebab-case。

```text
<feature>-plan/
├── index.md
├── 01-<observable-behavior>.md
├── 02-<observable-behavior>.md
└── 03-<observable-behavior>.md
```

- `index.md` 保留 Scope、Questions、Map、Constraints and Invariants、Prerequisites、Shared Concerns、slice 順序與相對連結，以及 Coverage。
- 每個 slice 檔案只包含該 slice 的欄位。
- slice 檔名使用 `<兩位數順序>-<observable-behavior>.md`。檔名描述呼叫端可觀察的行為，不使用需求 ID，也不只描述技術層。
- 調整 slice 順序時，同步重新命名檔案，並更新 `index.md` 中的編號與相對連結。

## Workflow

### 1. 讀取規範與功能來源

1. 讀取適用範圍內的 `AGENTS.md`、`CLAUDE.md`、README、workspace manifest 與相關開發文件，確認架構、搜尋、測試與文件規範。計畫跨越多個 repository 時，每個 repository 都要讀取其指示文件。
2. 讀取本次功能直接引用的規格，分辨已決定的行為、明確排除的範圍與待確認內容。
3. 建立需求清單，保留既有的穩定 ID。規格沒有穩定 ID 時，以需求標題或來源連結建立追溯關係，不依目前排序自行建立新編號。
4. 找出每項需求的規格依據。ui design、介面規格、資料模型或架構決策只有在已確認適用時才能寫入計畫。

### 2. 追蹤目前實作

開始搜尋前，先確認專案指示文件與目前環境提供的工具。只檢查下一步會用到的工具，不為了建立完整工具清單而逐一探測。

1. repository root 存在 `.codegraph/` 時，先確認 CodeGraph MCP tool 或 `codegraph explore` CLI 可用，再用它取得相關 symbol、引用關係與呼叫路徑。既有索引無法回答問題時，改用下一個適合的工具，不自行建立或重建索引。
2. 依搜尋目的選擇工具：
   - 搜尋已知文字、錯誤訊息或設定值時，使用 `rg`。
   - 列出或篩選檔案時，使用專用檔案搜尋工具或 `rg --files`。
   - 查找 definition、reference、implementation 或 type 時，使用 LSP。
   - 依語法結構搜尋或確認重構範圍時，使用 `ast-grep`。
   - 不知道關鍵字，需尋找用途或行為相似的既有實作時，使用目前環境提供的 semantic search。
3. 工具不存在或缺少所需能力時，記錄限制並改用下一個適合的工具。搜尋沒有結果時，先調整一次查詢，再用另一種適合該問題的方式交叉確認。

從最接近呼叫端可觀察行為的位置開始，沿目前資料流查到資料來源與輸出：

1. 找出功能入口，例如畫面、route、公開 export、API handler、job consumer、CLI command，或最先接收操作的事件處理位置。
2. 追蹤輸入、狀態或資料讀寫、轉換、外部呼叫與輸出或副作用，確認資料與流程由誰負責。
3. 確認相關 app、服務、package 或 repository 的責任與 dependency direction，並辨識 generated code、公開 exports、部署邊界與既有跨系統介面。執行指令與產生流程從專案指示文件查證，不在計畫中寫死未驗證的路徑或指令。
4. 找出一至三個資料流與行為都相近的既有實作，確認可以沿用的做法及適用原因。名稱相似但資料流不同的實作不能當成既有模式。
5. 查明受影響範圍已有的 test、typecheck、lint、integration、contract 或 E2E 指令。找不到時記錄現況，不自行發明。

計畫跨越多個 repository 時，分別查證各自的程式碼與規範，再合併結果。不要把一個 repository 的目錄、模組結構或責任邊界套用到另一個 repository。

### 3. 整理 Map

Map 是實作位置與責任邊界的地圖，只記錄目前已存在，而且會影響實作選擇的內容。若不知道某項內容不會導致實作者選錯修改位置、狀態或資料歸屬、系統邊界或可沿用模式，就從 Map 刪除。

Map 固定包含：

- **Entry points**：依呼叫端進入的畫面、route、公開 export、API handler、背景工作或 CLI command 分組。頂層先說明入口負責的行為，下一層再列 path、route 或 symbol。
- **Existing flow**：說明目前輸入從哪裡進入、資料或狀態由誰持有，以及最後產生什麼輸出或副作用；下一層列實際步驟與位置。
- **Existing patterns**：說明多個 slice 應沿用什麼做法及適用原因；下一層列一至三個 path 或 symbol 作為依據。

每項聲明都要以目前環境證實：提到的路徑必須存在；入口只負責轉交時，寫出實際處理位置；列出消費者時，以 import、呼叫關係或實際引用為準；已存在的介面定義不能誤寫成新增需求。

Map 不包含預計新增、修改或刪除的檔案、完整欄位清單、無關系統盤點、尚未存在的流程，或已能從 slice 得知的重複內容。

### 4. 整理 Constraints、Invariants 與 Prerequisites

`Constraints and Invariants` 集中記錄所有 slice 都要遵守，或會改變實作選擇的條件：

- **Constraints**：不可跨越的系統邊界、已確認的責任分工、generated code 限制、外部介面尚未定案，或明確不屬於本計畫的範圍。
- **Invariants**：每次操作完成後都必須成立的資料或系統條件，例如授權、資料一致性、相容性或不能超過既有上限的規則。

每項內容直接說明規則與其對實作選擇的影響，並連回功能規格、目前程式碼或使用者指示。未定案的規格不補造行為，放入 Questions 或 Constraint，並在實作前取得決策。

先嘗試將技術工作納入第一個需要它的行為 slice。只有工作無法合理形成呼叫端可驗證的行為，或必須先獨立完成才能避免不可接受風險時，才新增 `Prerequisites`。每個 Prerequisite 都要說明原因、受益 slice、完成條件與解除阻礙後最先啟動的行為。

### 5. 整理 Shared Concerns

兩個以上 slice 共同依賴既有的基礎能力、資料模型、規格理解或實作邊界時，新增 `Shared Concerns`。尚未具備且必須先完成的工作放在 Prerequisites，不放在此節。

每個 concern 使用 `### <行為或流程名稱>` heading，並只包含：

- **適用 slice**：Markdown 連結指向相關 slice heading；同一 slice 只適用部分行為時，連結後寫明範圍。
- **規格來源**：連到需求、資料模型、介面規格或架構決策的具體段落或既有穩定 ID，不重述規則全文。
- **觸發條件**：讀者無法從標題與其他欄位判斷何時發生時才加入。
- **共用**：這些 slice 必須一致理解或實作的部分。
- **不共用**：各 slice 仍自行持有的流程、輸出或狀態，避免被強迫抽成同一套實作。

### 6. 切分與排序 slices

使用 `to-slices` 的可觀察行為、可驗證結果與前置工作規則，判斷行為邊界、是否能獨立驗證與實作順序。本 skill 不重複定義切分規則，只將結果轉成可開始實作的計畫。

規劃工作不在 `to-slices` 的 Developer Mode 範圍內時，例如 mobile，仍套用相同的行為邊界與驗證原則。不要將不適用的職能分工表套用到該計畫。

- 同一需求包含兩個可獨立交付、可獨立觀察的狀態時，拆成不同 slice。
- 同一行為有多個仍在使用的入口時，將它們放入同一個 slice，並在 Map 記錄各入口的邊界。
- 外部介面尚未定案或由其他文件維護時，仍依可觀察行為切分，不建立只處理 API、schema、資料庫、元件或測試的技術 slice。
- slice 從 1 開始依實作順序連續編號。slice 編號只表示文件中的順序，不是需求的永久 ID；調整順序時同步更新標題、檔名與連結。

### 7. 填寫 slice 與 Coverage

每個 slice 依序使用下列欄位：

1. **Requirements**
2. **Scope**，只有相鄰 slice 碰到同一流程、同一需求拆成多個 slice，或規格證據含排除範圍時才加入。
3. **Constraints and Invariants**
4. **規格依據**，只有需要指向 slice 特有的設計、介面、資料模型或架構規格時才加入。
5. **Map**
6. **Validation**

各欄位的內容依下列規則填寫：

- `Requirements` 使用既有來源連結與來源章節名稱，例如 Story、Feature、UI Spec 的章節，或設計稿的 section。來源有穩定需求 ID 時一併保留；不要自訂 ID，也不要只寫沒有來源連結的摘要。
- `Scope` 說明完成後可觀察到的結果、沿用的既有資料流，以及刻意不處理的相鄰能力。
- `Constraints and Invariants` 只引用已在共用章節完整說明的規則。
- `Map` 只列開始實作前需要閱讀且已查證的現有位置，不是變更檔案清單。
- `Validation` 直接證明呼叫端取得 slice 宣稱的結果。可使用畫面操作、API request / response、CLI command、integration test、contract test、acceptance test，或可觀察的資料與外部系統結果。

建立 Coverage，列出功能規格中的全部需求，並使用 Markdown 連結指向覆蓋它的 slice。每個需求至少對應一個 slice；明確排除的需求要附上原因。

## Output Template

```md
# <Feature> plan

## Scope

- 預期行為以 [<behavior-spec>](spec-link) 為準。
- 目前系統只用來確認實作位置、責任邊界與可沿用模式。
- 涉及的系統範圍：
  - `<system-unit>`：<目前負責的行為>

## Map

### Entry points

- <入口目前負責的呼叫端行為>（`<system-unit>`）
  - Route、handler、export、command 或事件：`<entry>`
  - 實作位置：`<path-or-symbol>`

### Existing flow

- <輸入如何進入、資料或狀態由誰持有，以及最後產生什麼結果>
  - <步驟或位置>：`<path-or-symbol>`

### Existing patterns

- <要沿用的做法與適用原因>
  - 依據：`<path-or-symbol>`

## Constraints and Invariants

### Constraints

- <限制與對實作選擇的影響>

### Invariants

- <每次操作完成後必須成立的資料或系統條件>

## slices

### slice 1：<可觀察行為>

**Requirements**

- [<source-section-name>](source-link)

**Constraints and Invariants**

- <適用的既有 Constraint、Invariant 或 Shared Concern>

**Map**

- <這個現有位置在目前行為中負責什麼>
  - 路徑：`<existing-path-or-symbol>`

**Validation**

- <直接證明呼叫端取得此 slice 結果的方式>

## Coverage

- [<stable-requirement-id-or-title>](requirement-link) → [slice 1](#slice-1可觀察行為)
```

`Questions`、`Prerequisites`、`Shared Concerns`、`Scope` 與 `規格依據` 沒有內容時，省略整個章節或欄位，不寫「無」。

## Validation

交付前逐項檢查：

- 每個需求都能追溯到至少一個 slice；排除項目附有原因。
- 每個 slice 都以呼叫端可觀察的行為與結果描述，並能直接驗證；沒有依技術 layer 切成半成品。
- Map 只記錄已存在的實作。每個路徑、symbol、入口、介面名稱與消費者都已查證。
- 功能規格、規格依據與目前程式碼的用途已分開說明，沒有以程式碼補造需求或以規格建議推定現況。
- Questions 只包含會改變規劃的未知資訊，並說明採用前提與受影響的 slice。
- Constraints、Invariants、Prerequisites 與 Shared Concerns 已依定義分開，沒有重複或混用。
- 外部介面的未定案細節沒有被推測為 schema、欄位、錯誤格式或相容策略。
- 每個 slice 的 Validation 能直接證明所宣稱結果，不以內部 class、資料表、元件或 mock 存在作為完整交付證據。
- slice 編號、拆檔檔名、順序與 Coverage 連結一致；需求的既有穩定 ID 沒有因排序或文件搬移而改變。
- 全文沒有把特定平台、framework、目錄結構、程式語言、資料庫、介面形式或 repository 配置寫成普遍規則。
