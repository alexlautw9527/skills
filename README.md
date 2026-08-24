# Skills

此 repository 提供可安裝的 Skill。

列出可安裝的 Skill：

```bash
npx skills add alexlautw9527/skills --list
```

互動式選擇要安裝到哪些 agent：

```bash
npx skills add alexlautw9527/skills
```

## 從需求到落地

功能開發從模糊的需求開始，逐步確認行為、技術做法與交付範圍，最後產出可驗證的程式行為。每個階段只處理會影響下一步的未知，並留下下一步或日後維護會使用的文件。

```text
綠地：需求
  → discuss
  → to-sbe
  → 可驗收的行為規格 ＋ ui design（可選）

棕地：產品端提供的 sbe 與既有系統
  → 確認現有行為與影響範圍

兩條路徑接著共用下列流程：
  → 有未知使用 discuss 確認技術影響
  → 準備實作所需設計：to-ui-spec／to-system-design
  → 建立可供 review 的 task：to-plan 或 to-slices → to-tasks
  → 工程師確認 task 後實作、驗證與 review
  → 蒸餾需要長期保留的內容
  → 落地
```

### 1. 依綠地或棕地取得行為規格

- 綠地是建立尚未存在的新能力。先使用 [`general/discuss`](general/discuss/) 釐清需求中會影響行為規格的未知，再使用 [`to-sbe`](engineering/to-sbe/) 整理成可驗收的 sbe。ui design 可依需求提供，並在後續設計階段使用。確認範圍、限制與外部系統後，再進入下一步。
- 棕地是修改既有能力。以產品端提供的 sbe 為準，確認它與 ui design 及實際行為一致，並找出必須維持的行為、相依關係與資料流。

### 2. 確認技術影響

- 規格、現有行為或技術限制有會改變方案的未知時，使用 [`general/discuss`](general/discuss/) 討論、查證或比較方案。取得足以決定下一步的結論後停止討論。

### 3. 完成必要設計

- 有 Figma ui design 時，使用 [`to-ui-spec`](engineering/to-ui-spec/) 將畫面、互動與標註整理成 ui spec。
- 需要先決定責任分工、狀態、資料、介面，或日後難以改動的設計選擇時，使用 [`to-system-design`](engineering/to-system-design/)。

### 4. 規劃交付順序

- 需要查證實作位置、既有模式或跨 repository 範圍時，使用 [`to-plan`](engineering/to-plan/)。它會一併使用 [`to-slices`](engineering/to-slices/) 的方式，將功能切分成可獨立驗證的交付單位。
- 行為與設計已清楚時，可直接使用 [`to-slices`](engineering/to-slices/) 切分可獨立驗證的交付單位，再以 [`to-tasks`](engineering/to-tasks/) 拆成可實作與 review 的 task。
- 工程師在 task 文件確認交付範圍、驗收方式與仍需取捨的事項後，再開始實作。此時工程師只需判斷這項工作是否可執行及可驗收。

### 5. 實作與驗證

- 依計畫或 slice 完成程式碼，執行足以驗證行為與風險的測試或檢查。

### 6. 工程師 Review

- 將程式碼、驗證結果與已確認的決策整理到 review 文件，讓工程師核對實作是否符合 task 與行為規格。

### 7. 蒸餾需要長期保留的內容

- review 完成後，使用 [`general/distill`](general/distill/) 從實作、驗證與 review 中萃取有證據支持且會改變後續工程判斷的知識。沒有符合條件的知識時，不新增知識條目。
- 將 system design 草稿整理為日後仍需理解的責任分工、資料規則與難以撤回的決策，並使用 [`to-local-agents-md`](engineering/to-local-agents-md/) 更新觸及模組的 `AGENTS.md`。

### 8. 落地

- 將 sbe、整理後的 system design、更新後的 `AGENTS.md` 與程式碼一起合併並落地。
- ui spec、system design 草稿、plan、slice 與 task 等工作文件可留在功能分支，合併前移除。
