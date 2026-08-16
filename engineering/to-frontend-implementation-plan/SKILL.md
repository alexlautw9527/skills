---
name: to-frontend-implementation-plan
description: 依功能 spec 與既有前端 monorepo 的實際架構，產出可執行、可 review 的 Slice 實作計畫。規劃前端功能或拆解跨 workspace 實作時使用。
---

先向使用者確認實作計畫的存放位置，再讀完功能 spec 與 repository 並產生計畫。計畫依下列模板結構輸出，只保留會影響實作選擇的資訊：

- Current State：Entry points、Existing flow、Existing patterns、Constraints（狀態歸屬、workspace 邊界等限制）。每項先說明運作方式或責任，再於下一層列出 path、route、symbol 或設定依據
- Slice：每個 Slice 標明對應的 story，含 Outcome、Changes、Data flow、Validation。每項 Outcome 都要附上功能 spec 來源；spec 有提供設計稿時，附上對應此 Slice 的設計稿連結；Slice 排列順序即實作順序
- Shared Changes：跨 Slice 共用修改
- 檔案變更總覽：使用 `[DELETE]`、`[UPDATE]`、`[CREATE]` 標明本次刪除、修改與新增的全部檔案
- Story 覆蓋對照表：列出 PRD 全部 story，並以 Markdown 連結指向覆蓋它的 Slice
- Final Validation：含 PRD 所有 story（需求單元）的覆蓋檢查

## 輸入與產出

- 將下列來源視為功能 spec（以使用者指定或 repository 內可確認者為準）：
    - PRD
    - UI spec
    - issue
    - 設計說明
    - acceptance criteria
- 將 repository 內目前存在的程式碼、設定、測試與專案指令視為實作依據。spec 說明預期行為，repository 決定實作位置與沿用方式。
- 開始研究前，先確認使用者要直接在回覆中接收完整 Markdown 計畫，還是要將計畫寫入指定的檔案或目錄。使用者已提供路徑時，覆述該路徑並取得確認；未提供時，詢問存放位置，不自行決定。
- 取得確認後，依確認的形式交付計畫。寫入檔案或目錄時，只能使用使用者確認的路徑。
- 不修改產品程式碼。除非使用者另外要求，這個 skill 只負責研究與規劃。

### 拆檔產出

使用者要求將計畫拆成多個檔案時，將所有檔案放在同一個目錄。使用者未指定目錄名稱時，使用 `<feature>-implementation-plan/`；`<feature>` 取自 spec 或 repository 可確認的功能名稱，並轉成小寫英文 kebab-case。

```text
<feature>-implementation-plan/
├── index.md
├── 01-<observable-behavior>.md
├── 02-<observable-behavior>.md
└── 03-<observable-behavior>.md
```

- `index.md` 是整份計畫的入口，保留 Current State、Slice 順序與相對連結、Shared Changes、檔案變更總覽、Story 覆蓋對照表及 Final Validation。Story 覆蓋對照表中的 Slice 使用相對連結指向對應檔案。
- 每個 Slice 各自使用一個檔案，只包含該 Slice 的 Outcome（含來源）、Changes、Data flow、Design 與 Validation。
- Slice 檔名使用 `<兩位數順序>-<observable-behavior>.md`。順序與 Slice 編號一致；`<observable-behavior>` 取自 Slice 標題描述的可觀察行為，轉成小寫英文 kebab-case。
- Slice 檔名不得使用 story ID 或只描述技術層的名稱。調整 Slice 順序時，同步重新命名檔案，並更新 `index.md` 內的相對連結與 Slice 編號。

如果必要的 spec 無法存取，或缺少的規則會導致不同的可觀察行為，先提出一個可解除阻礙的問題。可以從 repository 查證的事項不得詢問使用者。

## 工作流程

### 1. 確認存放位置

1. 在讀取 spec、探索 repository 或建立文件前，先確認實作計畫的存放位置。
2. 使用者已指定輸出路徑時，覆述將要寫入的檔案或目錄，並等待使用者確認。
3. 使用者尚未指定時，詢問要直接在回覆中接收完整 Markdown 計畫，還是寫入指定的檔案或目錄。若選擇寫入，取得確切路徑後再繼續。
4. 確認前不得開始後續研究，也不得建立任何計畫檔案。

### 2. 確認規範與功能來源

1. 讀取 repository 的 `AGENTS.md`、`CLAUDE.md`、README、workspace manifest 與相關開發文件，確認搜尋、架構、測試和文件位置規範。
2. 讀完本次功能直接引用的 spec。分辨已決定的行為、明確排除的範圍與仍待確認的內容。
3. 只把 spec 當成預期行為的依據，不把其中的技術建議當成 repository 現況。任何修改位置與既有模式都要從 repository 查證。

### 3. 追蹤目前實作

開始搜尋前，先確認 repository 規範與目前環境提供的工具。只檢查下一步需要使用的工具，不為了建立完整清單而逐一探測所有工具。工具優先順序如下：

1. repository root 存在 `.codegraph/` 時，先確認 CodeGraph MCP tool 或 `codegraph explore` CLI 可用，再用它取得相關 symbol 的原始程式碼、引用關係與呼叫路徑。既有索引無法回答問題時繼續下一順位，不自行建立或重建索引。
2. CodeGraph 不存在、不可用、未涵蓋所需資訊，或目前問題不適合用呼叫關係查找時，依搜尋目的選擇專用工具：
   - 已知文字、錯誤訊息或設定值：使用 `rg`。
   - 列出或篩選檔案：使用 `rg --files`。
   - 查找 definition、reference、implementation 或 type：使用 LSP。
   - 依語法結構搜尋或確認重構範圍：使用 `ast-grep`。
   - 不知道關鍵字，需尋找用途或行為相似的既有實作：使用目前環境提供的 semantic search。
3. 專用工具不可用或不適合目前資料格式時，檔案搜尋才退回 `find`，內容搜尋最後才退回 `grep`。

工具不存在或因缺少所需能力而失敗時，記錄限制並改用下一順位，不反覆重試相同呼叫。搜尋沒有結果不代表工具不可用；先調整查詢一次，再使用另一種適合該問題的工具交叉確認，才能判定 repository 沒有對應實作。

工具選定後，從最接近使用者或系統可觀察行為的位置開始，沿資料流查到資料來源與輸出：

1. 找出功能從哪裡開始執行，例如 app 的啟動檔、route、page、供其他模組使用的元件，或最先接收使用者操作的事件處理位置。
2. 追蹤 UI 事件、狀態讀寫、query 或 API 呼叫、資料轉換與 render 結果，確認資料實際由誰持有，以及操作完成後資料必須符合的規則（invariants）。
3. 確認每個相關 workspace 負責哪些功能，以及哪些 workspace 可以引用哪些 workspace。同時查清楚哪些檔案是 generated code、哪些 exports 供其他 package 使用、既有跨 package 介面如何串接，以及本次修改是否會違反既有 dependency direction。
4. 找出一至三個最接近的既有實作與測試，記錄要沿用的做法及適用原因。名稱相似但資料流不同的實作不得當成既有模式。
5. 確認受影響 workspace 可執行的檢查指令，找不到時不自行發明：
   - test
   - typecheck
   - lint
   - integration 或 E2E

不要為了描述 repository 而列出所有相關檔案。每項 Current State 資訊都要通過以下檢查：

> 如果不知道這件事，實作者是否可能選錯修改位置、state ownership、workspace boundary 或 existing pattern？

答案為否時，從計畫刪除。

Current State 使用「概覽 → 實際位置或流程步驟 → 證據」的順序：

1. Entry points 依使用者可進入的頁面、route、供其他 module 呼叫的 export，或事件處理位置分組。頂層 bullet 先說明該入口負責的行為與所屬 workspace，下一層再列 route、page、module 或 symbol。
2. Existing flow 依一條完整資料流分組。頂層 bullet 先說明資料從哪裡進入、由誰持有，以及最後產生什麼結果；下一層依 UI 事件、state、query、轉換與 render 等實際步驟列出位置。
3. Existing patterns 先說明要沿用的做法與適用原因，下一層再用一至三個 path 或 symbol 作為依據。只有路徑清單、沒有做法與適用原因，不算 existing pattern。
4. Current State 只記錄目前已存在的實作。尚未實作的 route、module 或資料流，請寫在對應 Slice 的 Changes。預計新增、修改或刪除的檔案，請同時列入檔案變更總覽。實作前必須滿足的條件，以及實作時必須遵守的限制，請寫在 Constraints。
5. 同一個 bullet 若同時混入入口、資料流、修改計畫或限制，依上述責任拆到對應小節，不用一個長段落保留全部資訊。

### 4. 切分可驗證行為

1. 整理完整行為鏈時，依據 spec 的 acceptance criteria、使用流程與系統可觀察狀態。覆蓋關係由每個 Slice 標題的 story 對應直接呈現，不在計畫重述 spec 內容。Validation 欄位只寫驗證方式，不複製 acceptance criteria 原文。spec 的 acceptance criteria 有穩定 ID（例如 AC-001）時，直接引用該 ID；沒有穩定 ID 時，把 criteria 改寫成具體可執行的驗證步驟。
2. 每項 Outcome 都要附上支持該結果的功能 spec 來源。優先引用穩定的 story ID、acceptance criteria ID 或 UI spec ID；沒有穩定 ID 時，連結到使用者提供或 repository 內的 spec 小節。來源只建立可追查關係，不在 Outcome 重抄需求內容。
3. 依可觀察行為切成 Slice。每個 Slice 貫穿 UI、state、資料存取與 API，包含完成該行為所需的跨 workspace 修改與測試。
4. 讓每個 Slice 完成時都能獨立實作、驗證與 review。若結果只能等其他 Slice 完成後觀察，合併 Slice 或重新選擇邊界。
5. 依可以安全交付與驗證的順序排列 Slice。package boundary 不構成 Slice 邊界；同一 Slice 可以修改多個 workspace。
6. 優先沿用既有模式。只有多個 Slice 確實共同依賴，且無法合理歸入最早使用它的 Slice 時，才規劃 shared abstraction 或共用 contract。
7. Slice 切分完成後，逐項核對 PRD 的 story 清單。每個 Slice 都要標明對應的 story，同一 Slice 對應多個 story 時全部列出；缺少對應 Slice 的 story 要補 Slice，或說明排除理由。PRD 的全部 story 都必須有落點。
8. 依實作順序將 Slice 編為「Slice 1」、「Slice 2」等連續編號。調整 Slice 順序時，同步更新 Slice 標題與 Story 覆蓋對照表中的編號。
9. Story 覆蓋對照表中的 Slice 一律使用 Markdown 連結。拆檔計畫連到對應的 Slice 檔案；單檔計畫連到同一份文件內的 Slice heading anchor。同一個 story 由多個 Slice 覆蓋時，每個 Slice 各自提供連結。

不得建立只以技術層命名的 Slice，例如 `Add types`、`Update API`、`Update hooks`、`Update components` 或 `Add tests`。這些修改必須歸入會產生可觀察結果的 Slice。

### 5. 寫出計畫

使用 repository 中可確認的實際路徑、module、symbol 與指令。預計新增的檔案尚不存在時，參考相鄰既有實作與該目錄在專案中負責的職責，提出路徑，並說明新檔案承擔的責任。

Changes 寫到 file 或 module 層級，並說明每個變更承擔的責任：

- 寫清楚哪個既有責任會擴充、資料如何接入，以及選擇該位置的 repository 依據。
- 元件以檔案層級記錄：新增或擴充哪個元件、它與誰互動。不寫 props 設計與元件內部拆分。
- 不寫逐行程式碼、行號、完整函式內容或未經查證的介面。
- 不使用 `Update state` 這類無法判斷修改位置與結果的描述。
- 同一項修改同時支援多個 Slice 時，放入 Shared Changes；只服務單一 Slice 時，留在該 Slice。

依下列模板輸出。檔案路徑、module、symbol、workspace、package、指令、設定值，以及穩定的 story 或 acceptance criteria ID 使用 inline backtick；自然語言敘述不使用 inline backtick：

```md
# <Feature> Implementation Plan

## Current State

### Entry points

- <入口負責的使用者行為>（`<workspace>`）
  - Route、export 或事件：`<route-export-or-event>`
  - 實作位置：`<path-or-symbol>`

### Existing flow

- <這條流程如何接收輸入、持有資料並產生結果>
  - 輸入或事件：`<path-or-symbol>`
  - 狀態或資料存取：`<path-or-symbol>`
  - 輸出或 render：`<path-or-symbol>`

### Existing patterns

- <要沿用的做法，以及它為何適用>
  - 依據：`<path-or-symbol>`

### Constraints & Invariants

每項 constraint 或 invariant 先用一個頂層 bullet 說明規則，再於下一層列出一個 `影響：` 或 `驗證：`。需要補充其他會影響實作判斷的敘述時，繼續新增下一層 bullet；沒有則省略。

#### Constraints

- `<workspace / module / config>`：<限制修改選擇的條件，例如 workspace boundary、generated code、state ownership>
  - `影響：` <這項限制會排除哪些修改位置或實作方式>
  - <其他會影響實作判斷的補充說明；沒有則省略>

#### Invariants

- <操作完成後資料必須符合的規則，寫成「只要 X 完成就一定要 Y」或「任何完成的結果都不能出現 Z」>
  - `驗證：` <如何判斷結果符合這項規則；test、assertion、symbol 或指令使用 inline backtick>
  - <其他會影響實作判斷的補充說明；沒有則省略>

## Slice

Slice 依實作順序從 1 開始編號。調整 Slice 順序時，重新編號並同步更新所有引用。

### Slice 1：<可觀察行為>（對應 <story>）

**Outcome**

- <完成後可以觀察到什麼>
  - 來源：`<story-or-acceptance-criteria-ID>`、[<UI spec 或其他功能 spec 小節>](<spec-url-or-relative-path>)

**Changes**

- `<path or module>`
  - <修改什麼，以及必要時說明為什麼在這裡改>

**Data flow**

`<action> → <state/data> → <result>`

**Design**

- [<對應此 Slice 的畫面或互動>](design-url)

**Validation**

- <test 或明確驗證方式；test、symbol 或指令使用 inline backtick>

...

## Shared Changes

只放多個 Slice 都依賴、無法合理歸屬單一 Slice 的共用修改。

- `<shared package / contract / primitive>`
  - <修改內容與原因>

沒有則寫 `None`。

## 檔案變更總覽

將全部 Slice 與 Shared Changes 的檔案彙整成 tree，依 workspace 與目錄排列。每個檔案路徑前使用下列固定標記：

- `[DELETE]`：刪除既有檔案。
- `[UPDATE]`：修改既有檔案。
- `[CREATE]`：新增檔案。

<workspace>/
└── <dir>/
├── [DELETE] <file> # <刪除原因>
├── [UPDATE] <file> # <擴充了哪個既有責任>
└── [CREATE] <file> # <該檔案承擔的責任>

## Story 覆蓋對照表

列出 PRD 的全部 story 與覆蓋它的 Slice；沒有 Slice 覆蓋的 story 標明排除理由。`<slice-target>` 在拆檔計畫使用相對檔案路徑，在單檔計畫使用 Slice heading anchor：

| story             | 覆蓋的 Slice                                                        |
| ----------------- | ------------------------------------------------------------------- |
| <story ID 或名稱> | [Slice 1](<slice-1-target>)、[Slice 2](<slice-2-target>)             |
| <story ID 或名稱> | 無，<排除理由>                                                      |

## Final Validation

- [ ] Spec acceptance criteria 全部有對應驗證。
- [ ] PRD 的所有 story 都有對應的 Slice 與驗證。
- [ ] Affected regression tests pass.
- [ ] Affected workspaces typecheck / lint pass.
- [ ] 必要的 integration / E2E flow pass.
- [ ] 沒有新增未規劃的 cross-package dependency。
```

### 6. 修訂與交付

1. 初稿完成且技術內容與覆蓋關係都已檢查後，交付前必須調用 `make-ai-readable-zh` skill 修訂所有輸出檔案。
2. 修訂時改善段落結構與句子完整性，使用台灣慣用的正體中文，並在上下文中說清楚技術名詞的作用。不得改變 spec 或 repository 支持的事實、檔案路徑、symbol、指令、資料流、Slice 順序與 Story 覆蓋關係。
3. 修訂後重新執行完成檢查，確認文字調整沒有造成技術內容遺漏或語意改變。

## 完成檢查

- 存放位置
    - 已在讀取 spec、探索 repository 或建立文件前取得使用者確認，且交付形式與路徑符合確認內容。
- Current State
    - Entry points、Existing flow 與 Existing patterns 的頂層 bullet 先說明運作方式、責任或沿用原因，下一層才列 path、route、symbol 或設定依據。
    - 每一項（含 Constraints & Invariants）都影響實作選擇，並附有可追查的 path、module 或設定依據。
    - Current State 不含尚未存在的 route、module 或預計修改內容。
- Slice
    - 每個 Slice 有單一可觀察 Outcome、完整 Data flow、可立即執行的 Validation。
    - 每項 Outcome 都附上可追查的功能 spec 來源；來源使用穩定 ID 或連結，不以 repository 實作位置代替需求來源。
    - 每個 Slice 標明對應 story，並依實作順序連續編號；Slice 標題與 Story 覆蓋對照表使用相同編號。
    - 每個 Slice 在 spec 提供對應設計稿時附上連結；spec 未提供時整個 Design 小節省略，不自行猜測或編造 URL。
- Story 覆蓋
    - 每個 story 都有對應的 Slice（無對應者標明排除理由），與 Story 覆蓋對照表一致。
    - Story 覆蓋對照表中的每個 Slice 都是 Markdown 連結，且能到達對應的 Slice 檔案或 heading。
- Shared Changes
    - 只含至少兩個 Slice 共同依賴的修改，沒有符合項目時寫 `None`。
- 檔案變更總覽
    - 列出全部變更檔案，並在每個檔案路徑前使用 `[DELETE]`、`[UPDATE]` 或 `[CREATE]`；不得使用其他狀態文字或標記。
- Final Validation
    - 覆蓋 acceptance criteria、受影響 workspace 的既有檢查與跨 package dependency 變化。
- 表達與可讀性
    - 交付前已調用 make-ai-readable-zh skill 修訂所有輸出檔案，且修訂沒有改變技術事實、實作順序或 Story 覆蓋關係。
- 拆檔產出
    - 使用者要求拆檔時，`index.md` 包含所有跨 Slice 內容與 Slice 連結；每個 Slice 檔名及內容都符合拆檔規則，且功能清單與 Story 覆蓋對照表的所有相對連結都能到達對應檔案。
- 計畫不重述需求或 acceptance criteria，不把 UI、state、API、package、tests 拆成獨立工作階段。
- 全文不含無法由 spec 或 repository 支持的專案假設。
