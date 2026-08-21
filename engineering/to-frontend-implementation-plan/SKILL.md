---
name: to-frontend-implementation-plan
description: 依功能規格與既有前端 repository 的實際架構，產出以可觀察行為切分、可直接開始實作的 Slice 計畫。規劃前端功能或拆解跨 workspace 實作時使用。
---

依功能規格確認預期行為，並從目前環境查證實作位置與可沿用做法。計畫預設寫成單一檔案，讓實作者可以從同一個入口查到目前實作、限制、每個 Slice 的需求來源與現有程式碼位置。

## Inputs

- 使用者指定或 repository 內可確認的功能規格，例如 PRD、UI spec、issue、設計說明與 acceptance criteria。
- 目前環境中會被同一個可觀察行為碰到的 repository、workspace 或 package 裡，已經存在的程式碼、設定、測試、專案指示文件與執行指令。
- 使用者確認的交付形式與存放位置。

功能規格決定預期行為。目前程式碼決定實作位置、責任邊界與可沿用模式。規格中的技術建議不能當成現況，所有路徑、module、symbol 與既有流程都要從目前程式碼查證。

開始搜尋前，先找出會被同一個可觀察行為碰到的 repository、workspace 或 package，不要預設功能只落在開啟計畫的那一個 repository。

外部介面規格由其他文件維護時，計畫只記錄前端需要理解的資料語意、失敗情境、介面邊界與正式串接前必讀的規格角色。不要複製或推測 schema、欄位、operation、錯誤代碼與相容策略。

## Output

預設產出一份 Markdown 檔案，依序包含：

1. 範圍與依據。
2. Map。
3. Rules。
4. Shared Concerns。
5. 依實作順序排列的 Slices。
6. Coverage。

除非使用者另外要求，不要加入估點、結案報告或其他非可觀察產品行為的附錄。

每個 Slice 使用下列欄位，順序固定：

1. **Story**
2. **Scope**（In Scope / Out of Scope）
3. **Rules**
4. **UI Source**
5. **UI Spec**
6. **Map**

功能規格沒有提供對應的 UI Source 或 UI Spec 時，省略整個欄位，不寫「無」或其他替代文字。Scope 可依後文規則整欄省略，省略時同樣不寫「無」。

除非使用者另外要求，這個 skill 只負責研究與規劃，不修改產品程式碼。

## 交付位置

開始研究前，先確認使用者要直接在回覆中接收完整 Markdown 計畫，還是要寫入指定檔案或目錄。

1. 使用者已提供路徑時，覆述該路徑並取得確認。
2. 使用者未提供路徑時，詢問交付形式；若要寫入檔案，再取得確切路徑。
3. 取得確認前，不讀取功能規格、不探索 repository，也不建立計畫檔案。
4. 取得確認後，只能寫入已確認的位置。

必要的功能規格無法存取，或缺少的規則會造成不同的可觀察行為時，只提出一個能解除目前阻礙的問題。可以從目前程式碼查證的事項不得詢問使用者。

## 單檔與拆檔

### 預設使用單一檔案

所有 Slice 放在同一份計畫中。Slice 的排列順序就是實作順序，Coverage 使用 Markdown 連結指向同一份文件內的 Slice heading。

### 使用者明確要求時才拆檔

拆檔時，所有檔案放在同一個目錄。使用者未指定目錄名稱時，可以使用 `<feature>-implementation-plan/`；`<feature>` 應取自功能規格或目前環境可確認的名稱，並轉成小寫英文 kebab-case。

```text
<feature>-implementation-plan/
├── index.md
├── 01-<observable-behavior>.md
├── 02-<observable-behavior>.md
└── 03-<observable-behavior>.md
```

- `index.md` 保留 Scope、Map、Rules、Shared Concerns、Slice 順序與相對連結，以及 Coverage。
- 每個 Slice 檔案只包含該 Slice 的欄位。Map、Rules 與 Shared Concerns 不複製到 Slice 檔案。
- Slice 檔名使用 `<兩位數順序>-<observable-behavior>.md`。檔名描述使用者或系統可觀察的行為，不使用 story ID，也不只描述技術層。
- 調整 Slice 順序時，同步重新命名檔案，並更新 `index.md` 中的編號與相對連結。

## Workflow

### 1. 讀取規範與功能來源

1. 讀取適用範圍內的 `AGENTS.md`、`CLAUDE.md`、README、workspace manifest 與相關開發文件，確認架構、搜尋、測試與文件規範。聲明會跨越多個 repository 時，每個 repository 都要讀取其指示文件。
2. 讀完本次功能直接引用的規格，分辨已決定的行為、明確排除的範圍與仍待確認的內容。Figma 或 UI spec 仍有待確認、且不同答案會造成不同可觀察行為時，標成 Constraint，不要在計畫裡補造行為。
3. 建立 story 清單，保留既有的穩定 ID。若規格沒有穩定 ID，使用可長期指向同一項需求的標題或連結，不依目前排序自行建立容易變動的編號。
4. 找出功能規格中每個 story 對應的設計來源與 UI spec。只有已查證的對應關係才能寫入計畫。

### 2. 追蹤目前實作

開始搜尋前，先確認專案指示文件與目前環境提供的工具。只檢查下一步會用到的工具，不為了建立完整工具清單而逐一探測。

1. 目前 repository root 存在 `.codegraph/` 時，先確認 CodeGraph MCP tool 或 `codegraph explore` CLI 可用，再用它取得相關 symbol、引用關係與呼叫路徑。既有索引無法回答問題時，改用下一個適合的工具，不自行建立或重建索引。
2. 依搜尋目的選擇工具：
   - 搜尋已知文字、錯誤訊息或設定值時，使用 `rg`。
   - 列出或篩選檔案時，使用專用檔案搜尋工具或 `rg --files`。
   - 查找 definition、reference、implementation 或 type 時，使用 LSP。
   - 依語法結構搜尋或確認重構範圍時，使用 `ast-grep`。
   - 不知道關鍵字，需尋找用途或行為相似的既有實作時，使用目前環境提供的 semantic search。
3. 工具不存在或缺少所需能力時，記錄限制並改用下一個適合的工具，不反覆執行相同呼叫。搜尋沒有結果時，先調整一次查詢，再用另一種適合該問題的方式交叉確認。

聲明跨越多個 repository 時，每個 repository 分開查證後再合併結果，不要把一個 repository 的目錄或模組結構套用到另一個。

從最接近使用者或系統可觀察行為的位置開始，沿目前資料流查到資料來源與輸出：

1. 找出功能入口，例如 route、page、供其他 module 使用的 export，或最先接收操作的事件處理位置。
2. 追蹤 UI 事件、狀態讀寫、資料存取、資料轉換與 render 結果，確認資料由誰持有。
3. 確認相關 workspace 或 package 的責任與 dependency direction，並辨識 generated code、公開 exports 與既有跨 package 介面。generated code、選單同步、型別產生等執行方式，從專案指示文件查證，不要在 skill 或計畫中寫死路徑與指令。
4. 找出一至三個最接近的既有實作，確認可以沿用的做法及適用原因。名稱相似但資料流不同的實作不能當成既有模式。
5. 同一可觀察行為若有兩套仍在使用的實作，兩邊的入口都要查證，後續歸入同一個 Slice。改過濾條件或標示時，改共用 selector 或共用資料邊界，不要讓每個入口各寫一套。
6. 查明受影響範圍已有的 test、typecheck、lint、integration 或 E2E 指令。找不到時不自行發明。

### 3. 整理 Map

Map 是實作位置與責任邊界的地圖，只記錄目前已存在，而且會影響實作選擇的內容。

每一項都要通過以下檢查：

> 如果不知道這件事，實作者是否可能選錯修改位置、狀態歸屬、workspace 邊界或可沿用模式？

答案為否時，從計畫刪除。

Map 固定包含三類資訊：

- **Entry points**：依使用者可進入的頁面、route、公開 export 或事件處理位置分組。頂層先說明入口負責的行為，下一層再列 path、route 或 symbol。涉及多個 repository 或 workspace 時，頂層一併說明該入口目前由哪一邊負責。
- **Existing flow**：回答「目前怎麼運作」。頂層先說明資料從哪裡進入、由誰持有，以及最後產生什麼結果；下一層再列實際步驟與位置。
- **Existing patterns**：回答「多個 Slice 應沿用什麼做法，以及為何適用」。只保留跨 Slice 共用、若不知道就可能另建一套實作的慣例；下一層再列一至三個 path 或 symbol 作為依據。現有資料流已經提供衍生上限或狀態時，寫明沿用哪個入口，各畫面不要自行重算。

同一項資訊只能出現在一個位置：

- 描述目前資料如何流動，放 Existing flow。
- 只服務單一 Slice 的既有做法，放該 Slice 的 Map。
- 強制執行方式、generated code 限制或不可跨越的邊界，放 Constraints。
- 同一項資訊不得同時出現在 Existing flow 與 Existing patterns。

Map 的每項聲明都要以目前程式碼證實：

- 提到的檔案路徑必須實際存在。
- route 或入口檔只負責轉交時，把實作位置寫到實際 render 或處理事件的 module，不寫在轉交檔。
- query、mutation、fragment、enum 或其他 schema 名稱，與目前的 schema 或查詢定義核對；已經存在的欄位不得寫成需要新增。
- 列出消費者時，以 import 或實際引用為準，不依命名或印象推測。

Map 不包含：

- 逐頁完整欄位清單。
- 與本次功能無關的系統盤點。
- 不會影響實作位置的完整呼叫流程。
- 尚未存在的 route、module、頁面或資料流。
- 預計新增、修改或刪除的檔案。
- 已能從 Slice 的 Story 或 Map 得知的重複敘述。

### 4. 整理 Rules

這一節集中記錄所有 Slice 都要遵守，或會改變實作選擇的限制。不要在每個 Slice 重複相同內容。

- **Constraints** 記錄實作時不能跨越的邊界或前置條件，例如 workspace dependency、generated code、狀態歸屬、正式外部介面尚未定案，以及明確不屬於本計畫的範圍。
- **Invariants** 記錄操作完成後一定要成立的資料或業務規則，例如既有資料不能被重新推導，或數值不能超過已定義的上限。

一份 UI spec 或設計稿涵蓋多個功能時，Constraint 要點名排除哪些畫面或穩定 UI 編號；適用的 Slice 在 **UI Spec** 欄也寫排除範圍。

Figma 或 UI spec 仍有待確認問題時，計畫不補造行為；標成 Constraint，實作前先更新規格或取得產品決策。

頁面或流程目前不存在時，Constraint 只說明現況與應沿用的相鄰模式，不要把預計新增的檔案寫成現況。

每項內容直接說明規則及其對實作選擇的影響。只有能由功能規格、目前程式碼或使用者指示支持的內容才能列入。generated code、選單同步、型別產生等做法，寫「執行時從專案指示文件查證」，並在 Map 指向目前查到的入口，不寫死路徑。

### 5. 整理 Shared Concerns

當同一套規格或實作分工會出現在兩個以上 Slice 時，在 Rules 之後新增 **Shared Concerns** 一節。規則全文留在 Rules；本節只寫適用 Slice、規格來源，以及程式應抽共用或由各頁自行處理的部分。

列入 Shared Concerns 的判斷：

- 功能規格或 UI spec 以相同條款描述多個入口的行為。
- 同一套規格或同一個 Invariant 適用於兩個以上 Slice，且實作者若不知道邊界，會在各頁各寫一套錯誤處理、運算、刷新或判斷時機。
- 各 Slice 的儲存編排、UI 或 state 持有方式仍不同，需要寫出「共用」與「不共用」。

沒有跨 Slice 共用項時，省略整節 Shared Concerns，不寫 `None`。只影響單一 Slice 的規則留在該 Slice 的 Scope。

節標題固定為 `## Shared Concerns`。每個 concern 用 `###` heading，標題格式為 `<行為或流程名稱> (<Invariant 編號>)`。一個 concern 對應一個 Invariant，不要把多個 Invariant 塞進同一個 heading。

heading 底下只用下列欄位，順序固定，使用 Markdown 清單：

- **適用 Slice**：Markdown 連結指向相關 Slice heading。同一 Slice 只適用其中一段行為時，連結後用白話標出範圍。
- **規格來源**：連到功能規格與（若有）UI spec 的具體段落或穩定 ID，不重述 invariant 全文。
- **觸發條件**：只在讀者無法從標題與共用欄看出何時發生時才寫；否則刪掉整個欄位，不寫「無」。
- **共用**：這些 Slice 對該規則必須一致的理解，或必要時一致的實作。
- **不共用**：各 Slice 仍自行持有的流程、UI 或 state，避免被強迫抽成同一套。

同一個 concern 可以同時寫共用理解與不共用實作。不要把「必須抽成共用模組」當成預設。不要在 Shared Concerns 列檔案變更，也不要預先規定「共用／不共用」內容屬於哪一種分類。

Rules 與 Shared Concerns 的分工：

- **Invariants** 只寫操作完成後一定要成立的規則。
- **Shared Concerns** 只寫多 Slice 如何共用同一套規格理解與實作邊界。
- 若某規則只影響單一 Slice，留在該 Slice 的 Scope，不進 Shared Concerns。

各 Slice 若適用 Shared Concerns，在 **Rules** 末尾加一行 `Shared Concerns：<標題>`，只列 heading 文字，不重述五個欄位。

### 6. 依 `to-slices` 切分 Slice

先使用 `to-slices` 判斷 Slice 的行為邊界、是否能獨立驗證與實作順序。本 skill 不重複定義這些切分規則；其結果只用來決定前端計畫的 Slice，最後仍依本 skill 的欄位填寫 Story、Scope、Rules、UI Source、UI Spec 與 Map。

1. 同一可觀察行為若有兩套仍在使用的實作，放進同一個 Slice。Map 兩邊都要標。
2. 同一 Story 若含兩個可獨立交付、可獨立觀察的狀態，拆成兩個 Slice。Coverage 要把該 Story 連到所有相關 Slice。
3. 外部介面尚未定案或由其他文件維護時，仍以可觀察行為切分，不建立只處理 API、schema、types、hooks、元件或測試的技術 Slice。
4. 逐項核對 story 清單。每個 story 都要指向至少一個 Slice；明確排除的項目則在 Coverage 中標出 Non-Goals 或排除理由。
5. Slice 從 1 開始連續編號。調整順序時，同步更新標題與所有連結。

### 7. 填寫 Slice 欄位

#### Story

- 列出這個 Slice 覆蓋的穩定 story ID，並用 Markdown 連結指向功能規格中的對應 heading。
- 同一個 Slice 覆蓋多個 story 時，全部列出。
- 連結只建立可追查關係，不重述 story、acceptance criteria 或預期行為。

#### Scope

- **In Scope**：這個 Slice 完成後可以觀察到哪些畫面、互動或系統狀態，以及沿用哪一條既有儲存或資料流。
- **Out of Scope**：相鄰 Slice 負責的部分、本計畫排除的畫面，以及正式外部介面細節。

出現下列任一情況時必須撰寫整欄：

- 相鄰 Slice 碰同一畫面或同一流程。
- 同一 Story 被拆成多個 Slice。
- 同一份 UI spec 或設計稿含有本計畫排除的畫面。

Story 與 Map 已能看出邊界時，可省略整欄。省略時不寫「無」。

#### Rules

- 只列這個 Slice 適用的 Constraint 與 Invariant 編號，不重述全文。
- 適用 Shared Concerns 時，末尾加一行 `Shared Concerns：<標題>`，只列標題。

#### UI Source

- 連結到對應畫面或互動的設計來源，例如設計檔中的特定 node。
- 連結必須來自功能規格、功能索引或使用者提供的已確認來源。
- 沒有對應設計來源時，省略整個欄位。

#### UI Spec

- 連結到對應的 UI 規格檔案或小節。
- 同一份 UI 規格只引用與此 Slice 有關的段落；能連到 heading 時使用 heading 連結。
- 該 UI 規格含有本計畫排除的畫面時，在此欄寫出排除範圍。
- 沒有對應 UI 規格時，省略整個欄位。

#### Map

Map 告訴實作者應先閱讀哪些現有程式碼，以及這些位置在目前行為中負責什麼。它不是預計變更的檔案清單，也不需要完整盤點所有相關檔案。

- 每個頂層 bullet 先用完整句子說明現有檔案、module 或流程在這條行為中的責任，下一層再列 path、route 或 symbol。
- 只列開始實作時需要閱讀，而且已從目前程式碼查證的現有位置。
- 兩套仍在使用的實作都要列出，並說明目前的過濾或標示邊界。
- 不標示檔案將被新增、修改或刪除，也不要求列出所有可能受影響的檔案。
- 不設計 props、內部元件拆分、未查證的欄位名、operation 或錯誤格式。
- 不重述 story、acceptance criteria 或 UI 規格描述的行為。
- 頁面或流程尚未存在時，直接寫明目前沒有對應實作，並指出應參考哪個已存在的相鄰頁面或模式。不要預先列出完整的新檔案樹。

### 8. 建立 Coverage

列出功能規格中的全部 story，並使用 Markdown 連結指向覆蓋它的 Slice。

- 每個 story 使用穩定 ID，並連到功能規格的對應 heading。
- 單檔計畫連到同一份文件內的 Slice heading anchor。
- 拆檔計畫連到對應的 Slice 檔案。
- 同一個 story 由多個 Slice 覆蓋時，分別列出所有連結。
- 明確排除的 story 或 Non-Goals 要標示排除原因，不能留空。

### 9. 修訂與交付

1. 初稿的技術內容與覆蓋關係確認完成後，交付前使用 `make-ai-readable-zh` skill 修訂所有輸出檔案。
2. 修訂時改善段落結構與句子完整性，使用台灣慣用的正體中文，並在上下文中說清楚技術名詞的用途。
3. 文字修訂不能改變功能規格與目前程式碼支持的事實、路徑、symbol、Slice 順序或 Coverage 關係。
4. 修訂後重新執行 Validation。

## Output Template

檔案路徑、module、symbol、workspace、package、指令、設定值與穩定 story ID 使用 inline backtick。自然語言敘述不使用 inline backtick。

```md
# <Feature> Implementation Plan

## Scope

- 預期行為以 [<behavior-spec>](<spec-link>) 為準。
- UI 依據來自 [<feature-design-index>](<design-index-link>) 與各 Slice 引用的 UI spec。
- 目前程式碼只用來確認實作位置、責任邊界與可沿用模式。
- 涉及的 repository 或 workspace：
  - `<repo-or-workspace>`：<目前負責的行為>
- <本計畫包含與排除的範圍；沒有補充時省略。>

## Map

### Entry points

- <入口目前負責的使用者行為>（`<workspace-or-package>`）
  - Route、export 或事件：`<route-export-or-event>`
  - 實作位置：`<path-or-symbol>`

### Existing flow

- <資料如何進入、由誰持有，以及最後產生什麼結果>
  - 輸入或事件：`<path-or-symbol>`
  - 狀態或資料存取：`<path-or-symbol>`
  - 輸出或 render：`<path-or-symbol>`

### Existing patterns

- <要沿用的做法，以及它為何適用>
  - 依據：`<path-or-symbol>`

## Rules

### Constraints

- <會限制實作位置、責任邊界或交付範圍的條件。>

### Invariants

- <操作完成後一定要成立的資料或業務規則。>

## Shared Concerns

<若有多 Slice 共用規格或實作分工，在此集中記錄；沒有則省略整節。>

### <行為或流程名稱> (<Invariant 編號>)

- **適用 Slice**：[Slice N](#slice-n-heading)、[Slice M](#slice-m-heading)
- **規格來源**：[功能規格](<spec-link>) <story 或段落>；[<ui-spec>](<ui-spec-link>) `<UI-id>`
- **觸發條件**：<非顯而易見時才寫；否則刪掉此欄>
- **共用**：<這些 Slice 必須一致的理解或實作>
- **不共用**：<各 Slice 仍自行持有的流程、UI 或 state>

## Slices

### Slice 1：<可觀察行為>

**Story**

- [`<story-id>`：<story-title>](<behavior-spec-heading-link>)

**Scope**

#### In Scope

- <這個 Slice 完成後可以觀察到什麼。>

#### Out of Scope

- <由相鄰 Slice 負責，或本計畫排除的部分。>

**Rules**

- Constraints：`<constraint-id>`。
- Invariants：`<invariant-id>`。
- Shared Concerns：<行為或流程名稱> (<Invariant 編號>)。

**UI Source**

- [<對應畫面或互動>](<design-node-link>)

**UI Spec**

- [<對應 UI 規格或小節>](<ui-spec-heading-link>)

**Map**

- <這個現有位置在目前行為中負責什麼。>
  - 路徑：`<existing-path-or-symbol>`

### Slice 2：<可觀察行為>

**Story**

- [`<story-id>`：<story-title>](<behavior-spec-heading-link>)

**Map**

- 目前沒有對應頁面；實作時沿用 <現有頁面的哪一種模式>。
  - 參考：`<existing-pattern-path-or-symbol>`

## Coverage

- [`<story-id>`](<behavior-spec-heading-link>) → [Slice 1](#slice-1可觀察行為)
- [`<story-id>`](<behavior-spec-heading-link>) → [Slice 2](#slice-2可觀察行為)
- `<non-goal-id-or-title>`：排除，<原因>。
```

模板中的 UI Source、UI Spec、Scope、觸發條件只示範有對應內容時的格式。沒有對應來源或可省略的欄位，必須省略整個欄位。Slice 2 示範在邊界已清楚時省略 Scope。

## Validation

### 交付位置與範圍

- 已在研究前取得使用者對交付形式與存放位置的確認。
- 只寫入使用者確認的位置，且沒有修改產品程式碼。
- 計畫清楚說明預期行為、UI 與目前程式碼各以哪些來源為準。
- 範圍與依據已列出會被同一個可觀察行為碰到的 repository 或 workspace，以及各自目前負責的行為。
- 外部介面由其他文件維護時，沒有複製或推測其 schema、欄位、operation、錯誤代碼與相容策略。
- 沒有把估點、結案報告或其他非可觀察產品行為寫成 Slice 或預設產出。

### Map

- Entry points、Existing flow 與 Existing patterns 的頂層 bullet 先說明運作方式、責任或沿用原因，下一層才列 path、route、symbol 或設定依據。
- 每一項都會影響修改位置、狀態歸屬、workspace 邊界或可沿用模式。
- 只記錄目前存在的實作，沒有混入未來檔案、預計修改內容或無關的系統盤點。
- Existing flow 只描述目前資料如何流動；Existing patterns 只保留跨 Slice 共用的既有做法，兩者沒有重複項目。
- 現有資料流已提供衍生上限或狀態時，Existing patterns 已寫明沿用入口，而不是讓各畫面重算。
- 單一 Slice 的既有做法已放入該 Slice 的 Map；強制執行方式與 generated code 限制已放入 Rules。
- 跨越多個 repository 的聲明已分別查證；檔案路徑存在，入口與實際處理位置沒有寫反，schema 名稱已核對。

### Rules

- 所有項目都能由功能規格、目前程式碼或使用者指示支持。
- 跨 Slice 適用的限制集中在這一節，沒有在各 Slice 重複全文。
- Invariants 說明操作完成後必須成立的規則，沒有只寫抽象名詞。
- UI spec 或設計稿涵蓋其他功能時，已點名排除的畫面或穩定 UI 編號。
- 待確認問題已標成 Constraint，沒有補造行為。
- 尚未存在的頁面沒有被寫成現況檔案樹。
- 需要跨 Slice 說明共用規格或實作分工時，已新增 Shared Concerns，且 Invariant 若有對應項目會連到該節。

### Shared Concerns

- 只收錄兩個以上 Slice 共用的項目；單 Slice 規則留在該 Slice 的 Scope。
- 每個 concern 的 heading 為 `<行為或流程名稱> (<Invariant 編號>)`，且只對應一個 Invariant。
- 每項都依序包含適用 Slice、規格來源、共用與不共用；觸發條件只在非顯而易見時出現。
- 沒有跨 Slice 共用項時，已省略整節 Shared Concerns，沒有寫 `None`。
- 各 Slice 的 Rules 只引用 Shared Concerns 標題，沒有重述全文。

### Slices

- Slice 的行為邊界、獨立驗證條件與實作順序依 `to-slices` 判斷，沒有自行建立相衝突的切分規則。
- 同一 Story 若含兩個可獨立交付的可觀察狀態，已拆成不同 Slice，並在 Coverage 列出全部連結。
- 兩套仍在使用的實作已放進同一個 Slice，Map 兩邊都有標。
- Slice 依實作順序連續編號，標題、檔名與連結中的編號一致。
- 每個 Slice 的欄位順序為 Story、Scope、Rules、UI Source、UI Spec、Map；可省略的欄位已整欄省略。
- 出現相鄰 Slice 同畫面、Story 被拆、或 UI spec 含排除畫面時，已撰寫 Scope。
- 每個 Story 都使用穩定 ID 並連到功能規格的對應 heading。
- 只有已確認的設計來源與 UI spec 才會出現；缺少來源時已省略整個欄位。
- Map 的頂層先說明現有位置的責任，下一層才列查證過的 path、route 或 symbol。
- Map 沒有變更狀態、完整未來檔案樹、props、未查證的介面細節，或對需求內容的重述。
- 尚未存在的頁面或流程已明確說明現況，並指向查證過的既有模式。

### Coverage

- 功能規格中的每個 story 都連到至少一個 Slice，明確排除的項目則附有原因。
- 每個 story 都有指向功能規格 heading 的連結，沒有改成只有編號的壓縮表。
- 單檔計畫的連結可到達對應 heading；拆檔計畫的相對連結可到達對應檔案。

### 拆檔產出

- 只有使用者明確要求時才拆檔。
- Map、Rules 與 Shared Concerns 只出現在 `index.md`。
- 每個 Slice 檔案只包含該 Slice 的欄位。
- Slice 檔名描述可觀察行為，編號、順序與 `index.md` 連結一致。

### 表達與泛化

- 交付前已依 `make-ai-readable-zh` skill 修訂，且修訂沒有改變技術事實、Slice 順序與 Coverage。
- 規則使用角色、關係或 placeholder 表達，沒有寫死特定專案的名稱、目錄、框架、元件、領域實體或 API。
- 全文沒有功能規格或目前程式碼無法支持的假設。
