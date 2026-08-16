---
name: to-frontend-implementation-plan
description: 依功能 spec 與既有前端 monorepo 的實際架構，產出可執行、可 review 的功能片段實作計畫。規劃前端功能或拆解跨 workspace 實作時使用。
---

先讀完功能 spec 與 repository，再產生實作計畫。計畫依下列模板結構輸出，只保留會影響實作選擇的資訊：

- Current State：Entry point、Existing flow、Existing patterns、Constraints（狀態歸屬、workspace 邊界等限制）
- 功能片段：每個片段標明對應的 story，含 Outcome、Changes、Data flow、Validation；spec 有提供設計稿時，附上對應此片段的設計稿連結；片段排列順序即實作順序
- Shared Changes：跨片段共用修改
- 檔案變更總覽：本次新增、修改、刪除的全部檔案一覽
- Story 覆蓋對照表：PRD 全部 story 與覆蓋它的片段
- Final Validation：含 PRD 所有 story（需求單元）的覆蓋檢查

## 輸入與產出

- 將下列來源視為功能 spec（以使用者指定或 repository 內可確認者為準）：
  - PRD
  - UI spec
  - issue
  - 設計說明
  - acceptance criteria
- 將 repository 內目前存在的程式碼、設定、測試與專案指令視為實作依據。spec 說明預期行為，repository 決定實作位置與沿用方式。
- 使用者指定輸出路徑時，將計畫寫入該路徑。未指定時，在回覆中輸出完整 Markdown 計畫，不自行建立文件。
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

- `index.md` 是整份計畫的入口，保留 Current State、片段順序與相對連結、Shared Changes、檔案變更總覽、Story 覆蓋對照表及 Final Validation。
- 每個功能片段各自使用一個檔案，只包含該片段的 Outcome、Changes、Data flow、Design 與 Validation。
- 片段檔名使用 `<兩位數順序>-<observable-behavior>.md`。順序與片段編號一致；`<observable-behavior>` 取自片段標題描述的可觀察行為，轉成小寫英文 kebab-case。
- 片段檔名不得使用 story ID 或只描述技術層的名稱。調整片段順序時，同步重新命名檔案，並更新 `index.md` 內的相對連結與片段編號。

如果必要的 spec 無法存取，或缺少的規則會導致不同的可觀察行為，先提出一個可解除阻礙的問題。可以從 repository 查證的事項不得詢問使用者。

## 工作流程

### 1. 確認規範與功能來源

1. 讀取 repository 的 `AGENTS.md`、`CLAUDE.md`、README、workspace manifest 與相關開發文件，確認搜尋、架構、測試和文件位置規範。
2. 讀完本次功能直接引用的 spec。分辨已決定的行為、明確排除的範圍與仍待確認的內容。
3. 只把 spec 當成預期行為的依據，不把其中的技術建議當成 repository 現況。任何修改位置與既有模式都要從 repository 查證。

### 2. 追蹤目前實作

依 repository 規範選擇搜尋工具；repository root 存在 `.codegraph/` 時，先用 CodeGraph 追蹤符號與呼叫路徑。從最接近使用者或系統可觀察行為的位置開始，沿資料流查到資料來源與輸出：

1. 找出功能進入點，例如 app、route、page、公開元件或事件入口。
2. 追蹤 UI 事件、狀態讀寫、query 或 API 呼叫、資料轉換與 render 結果，確認資料實際由誰持有，以及操作完成後資料必須符合的規則（invariants）。
3. 確認相關 workspace 的責任與依賴方向，包括 generated code、公開 exports、既有跨 package 介面及不得新增的反向依賴。
4. 找出一至三個最接近的既有實作與測試，記錄要沿用的做法及適用原因。名稱相似但資料流不同的實作不得當成既有模式。
5. 確認受影響 workspace 可執行的檢查指令，找不到時不自行發明：
   - test
   - typecheck
   - lint
   - integration 或 E2E

不要為了描述 repository 而列出所有相關檔案。每項 Current State 資訊都要通過以下檢查：

> 如果不知道這件事，實作者是否可能選錯修改位置、state ownership、workspace boundary 或 existing pattern？

答案為否時，從計畫刪除。

### 3. 切分可驗證行為

1. 整理完整行為鏈時，依據 spec 的 acceptance criteria、使用流程與系統可觀察狀態。覆蓋關係由每個片段標題的 story 對應直接呈現，不在計畫重述 spec 內容。Validation 欄位只寫驗證方式，不複製 acceptance criteria 原文。spec 的 acceptance criteria 有穩定 ID（例如 AC-001）時，直接引用該 ID；沒有穩定 ID 時，把 criteria 改寫成具體可執行的驗證步驟。
2. 依可觀察行為切成功能片段。每個片段貫穿 UI、state、資料存取與 API，包含完成該行為所需的跨 workspace 修改與測試。
3. 讓每個片段完成時都能獨立實作、驗證與 review。若結果只能等其他片段完成後觀察，合併片段或重新選擇邊界。
4. 依可以安全交付與驗證的順序排列片段。package boundary 不構成片段邊界；同一片段可以修改多個 workspace。
5. 優先沿用既有模式。只有多個片段確實共同依賴，且無法合理歸入最早使用它的片段時，才規劃 shared abstraction 或共用 contract。
6. 片段切分完成後，逐項核對 PRD 的 story 清單。每個片段都要標明對應的 story，同一片段對應多個 story 時全部列出；缺少對應片段的 story 要補片段，或說明排除理由。PRD 的全部 story 都必須有落點。
7. 依實作順序將片段編為「片段 1」、「片段 2」等連續編號。調整片段順序時，同步更新片段標題與 Story 覆蓋對照表中的編號。

不得建立只以技術層命名的片段，例如 `Add types`、`Update API`、`Update hooks`、`Update components` 或 `Add tests`。這些修改必須歸入會產生可觀察結果的片段。

### 4. 寫出計畫

使用 repository 中可確認的實際路徑、module、symbol 與指令。預計新增的檔案尚不存在時，參考相鄰既有實作與該目錄在專案中負責的職責，提出路徑，並說明新檔案承擔的責任。

Changes 寫到 file 或 module 層級，並說明每個變更承擔的責任：

- 寫清楚哪個既有責任會擴充、資料如何接入，以及選擇該位置的 repository 依據。
- 元件以檔案層級記錄：新增或擴充哪個元件、它與誰互動。不寫 props 設計與元件內部拆分。
- 不寫逐行程式碼、行號、完整函式內容或未經查證的介面。
- 不使用 `Update state` 這類無法判斷修改位置與結果的描述。
- 同一項修改同時支援多個片段時，放入 Shared Changes；只服務單一片段時，留在該片段。

依下列模板輸出。檔案路徑、module、symbol、workspace、package、指令、設定值，以及穩定的 story 或 acceptance criteria ID 使用 inline backtick；自然語言敘述不使用 inline backtick：

```md
# <Feature> Implementation Plan

## Current State

- Entry point: `<app / route / page>`
- Existing flow: `<UI> → <state/query> → <API> → <render>`
- Existing patterns:
  - `<path>`：<要沿用的做法，以及它為何適用>

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

## 功能片段

片段依實作順序從 1 開始編號。調整片段順序時，重新編號並同步更新所有引用。

### 片段 1：<可觀察行為>（對應 <story>）

**Outcome**

- <完成後可以觀察到什麼>

**Changes**

- `<path or module>`
  - <修改什麼，以及必要時說明為什麼在這裡改>

**Data flow**

`<action> → <state/data> → <result>`

**Design**

- [<對應此片段的畫面或互動>](<design-url>)

**Validation**

- <test 或明確驗證方式；test、symbol 或指令使用 inline backtick>

...

## Shared Changes

只放多個片段都依賴、無法合理歸屬單一片段的共用修改。

- `<shared package / contract / primitive>`
  - <修改內容與原因>

沒有則寫 `None`。

## 檔案變更總覽

將全部片段與 Shared Changes 的檔案彙整成 tree，依 workspace 與目錄排列，每個檔案標明新增、修改或刪除：

<workspace>/
└── <dir>/
├── <file> # 新增：<該檔案承擔的責任>
├── <file> # 修改：<擴充了哪個既有責任>
└── <file> # 刪除：<刪除原因>

## Story 覆蓋對照表

列出 PRD 的全部 story 與覆蓋它的片段；沒有片段覆蓋的 story 標明排除理由：

| story             | 覆蓋的片段       |
| ----------------- | ---------------- |
| <story ID 或名稱> | <片段 1、片段 2> |
| <story ID 或名稱> | 無，<排除理由>   |

## Final Validation

- [ ] Spec acceptance criteria 全部有對應驗證。
- [ ] PRD 的所有 story 都有對應的片段與驗證。
- [ ] Affected regression tests pass.
- [ ] Affected workspaces typecheck / lint pass.
- [ ] 必要的 integration / E2E flow pass.
- [ ] 沒有新增未規劃的 cross-package dependency。
```

### 5. 修訂與交付

1. 初稿完成且技術內容與覆蓋關係都已檢查後，交付前必須調用 make-ai-readable-zh skill 修訂所有輸出檔案。
2. 修訂時改善段落結構與句子完整性，使用台灣慣用的正體中文，並在上下文中說清楚技術名詞的作用。不得改變 spec 或 repository 支持的事實、檔案路徑、symbol、指令、資料流、片段順序與 Story 覆蓋關係。
3. 修訂後重新執行完成檢查，確認文字調整沒有造成技術內容遺漏或語意改變。

## 完成檢查

- Current State
  - 每一項（含 Constraints & Invariants）都影響實作選擇，並附有可追查的 path、module 或設定依據。
- 功能片段
  - 每個片段有單一可觀察 outcome、完整 data flow、可立即執行的 validation。
  - 每個片段標明對應 story，並依實作順序連續編號；片段標題與 Story 覆蓋對照表使用相同編號。
  - 每個片段在 spec 提供對應設計稿時附上連結；spec 未提供時整個 Design 小節省略，不自行猜測或編造 URL。
- Story 覆蓋
  - 每個 story 都有對應的片段（無對應者標明排除理由），與 Story 覆蓋對照表一致。
- Shared Changes
  - 只含至少兩個片段共同依賴的修改，沒有符合項目時寫 `None`。
- 檔案變更總覽
  - 列出全部變更檔案，每項標明新增、修改或刪除。
- Final Validation
  - 覆蓋 acceptance criteria、受影響 workspace 的既有檢查與跨 package dependency 變化。
- 表達與可讀性
  - 交付前已調用 make-ai-readable-zh skill 修訂所有輸出檔案，且修訂沒有改變技術事實、實作順序或 Story 覆蓋關係。
- 拆檔產出
  - 使用者要求拆檔時，`index.md` 包含所有跨片段內容與片段連結；每個片段檔名及內容都符合拆檔規則，且所有相對連結都能到達對應檔案。
- 計畫不重述需求或 acceptance criteria，不把 UI、state、API、package、tests 拆成獨立工作階段。
- 全文不含無法由 spec 或 repository 支持的專案假設。
