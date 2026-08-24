---
name: to-sbe
description: 將使用者需求、產品規格、ui design 或既有行為整理成 sbe。當使用者要求用具體情境、規則與驗收條件釐清系統行為、例外情境或既有行為變更時使用；不處理實作、架構、slice 或 task 的規劃。
---
> 執行本 skill 時，預設一併讀取 `make-ai-readable-zh` skill。

先與使用者確認本次需求的 Roles，再界定 Goals 與 Non-goals，並將一個或多個 Story 拆成 Feature、Rule、用來說明各 Rule 的 Example，以及尚待回答的 Questions，最後以 Gherkin 的 Feature、Rule 與 Scenario 交付。sbe 說明系統應遵守什麼規則與如何驗證結果，不決定實作方式。

## Inputs

取得下列資訊：

- 使用者需求、產品想法、issue 或 ticket。
- PM spec、PRD、ui design 或 prototype。
- 既有產品行為。
- 目標使用者與使用情境。
- 可能觸發、接收或驗證本次行為的角色。
- 已知限制，例如權限、安全性、資料正確性、相容性或法規要求。
- 已確認的 glossary，或用於判斷 glossary 位置與術語定義的材料。

資訊不足時，不要因次要未知資訊停止整理。

- 可能影響行為邊界、完成條件、權限、資料規則、流程或驗收方式的資訊，列入 Questions。
- 能以暫定前提繼續整理時，在同一項 Questions 寫出採用的前提；無法安全採用前提時，寫出需要產品決定的事項。不要默默決定。
- 不要把尚未要求、可安全排除的未來能力列為 Questions；改列入 Non-goals，或不提及。

## Constraints

以 Story、Rule 與 Example 描述誰可以完成什麼事情、系統在什麼條件下如何回應，以及呼叫端如何知道結果成立。新增按鈕、建立元件或資料表等實作活動，以及 class、function、資料庫 schema、API endpoint 或特定技術方案的選擇，都不是行為描述；這些決策屬於 plan 或 system design。

Gherkin 程式碼區塊中的關鍵字必須維持原始語法，不得使用反引號。

Roles 列出本次需求中會觸發、接收或驗證系統行為的人或外部系統，以及各自與需求的關係。依目標、權限或可觀察行為不同來區分角色；名稱不同但行為與權限相同時，使用同一個角色。系統本身不是角色。每個 Story 的 As a <角色> 都必須使用已確認的角色名稱。

Rule 是關聯 Story 的驗收條件；每個 Scenario 用一個具體情境驗證一條 Rule。[Cucumber 將 Rule 定義為需要實作的業務規則，並要求以一個或多個 Scenario 說明](https://cucumber.io/docs/gherkin/reference/)；Cucumber 也將 Rule 視為 acceptance criterion，將具體 Example 視為說明 Rule 行為的情境。[Better requirements by harnessing the power of examples](https://cucumber.io/blog/bdd/better-requirements-by-harnessing-the-power-of-exa/)

Feature 是完成 Story 所需的一項系統能力。Feature 只服務一項 Story 時，直接寫在該 Story 下方。Feature 服務多項 Story 時，集中定義為 Shared Feature，並由各 Story 以連結參照。這是 sbe 的需求管理結構；Gherkin 的正式結構仍是 Feature、Rule 與 Scenario。

Inputs 已包含本次要修改的功能之既有 sbe 時，交付 diff 版本的 sbe：只輸出受影響的 Story 與 Feature 區塊，以及隨之行為變更需要調整的 Glossary、Roles、Goals 或 Non-goals 項目，並沿用既有 sbe 的章節結構與名稱，讓 diff 可以直接合併回來源文件；未受影響的內容不重寫。合併屬於後續工作，不在本次交付範圍。

diff 中每個受影響的 Markdown Feature 區塊標題後，以獨立欄位標示變更標記，格式為 Change: [CREATE]。[CREATE] 表示來源文件沒有這個能力，本次新增；[UPDATE] 表示改變來源文件既有能力的可觀察行為；[DELETE] 表示移除來源文件中的既有能力。依本次需求造成的可觀察行為變化選擇標記。

非 diff 的交付不加 Change 欄位，即使其中的 Feature 是首次定義或描述既有系統的行為異動。

每個 Rule 都是團隊同意的 acceptance criterion，可以描述允許的行為、預期結果或限制條件。每個 Scenario 只說明一個 Rule，並包含：

- 誰執行。
- 在什麼情境下開始。
- 執行什麼操作。
- 系統產生什麼結果。
- 呼叫端如何確認結果成立。

可用 3 到 5 個步驟清楚表達的情境，使用正式 Gherkin 的 Scenario、Given、When、Then 與必要的 And 或 But。替代與失敗情境各自寫成 Scenario。流程過長且不能切成可獨立驗證的情境時，改用條列。

Example 盡可能以資料驅動的方式表達：多個情境的步驟與預期結果結構相同，只有輸入或前置狀態不同時，寫成一個 Scenario Outline，把各案例的差異放進 Examples 表格，不重複撰寫相同的步驟。

Scenario 是 Gherkin 對 Example 的名稱。Feature、Rule 與 Scenario 合在一起，構成可交付、可驗證的規格。

Questions 是釐清各 Story 時的暫時記錄。Questions 尚未回答時，sbe 仍是草稿；答案應形成或調整 Rule 與 Example，而不是保留在準備交付的規格中。

補上行為正確性必要的非成功流程，例如沒有結果、無效輸入、權限不足、可恢復失敗、破壞性操作確認或狀態衝突。不要列出不影響呼叫端結果的純技術 edge case。

Rule 可以描述允許的行為，例如使用者可以取消預約，也可以描述限制，例如付款完成超過 24 小時後不可取消。Rule 不改寫成操作流程。

修改既有系統時，描述目前行為與行為變更，不要只描述新增需求而省略將被修改、移除或保持的行為。

Goals 說明本次需求完成後應達成的使用者或業務結果。Non-goals 說明刻意不包含的結果或能力，用來界定規格邊界。兩者都以可判斷是否達成或排除的結果描述，不列出實作活動。

## Workflow

### 1. 確認 Roles

從需求材料整理候選角色，說明每個角色會觸發、接收或驗證哪些行為，並為每個候選角色列出一個或多個候選需求句子：

~~~text
As a <角色>,
I want <想完成的事情>,
so that <取得的價值或目的>.
~~~

請使用者確認、修改、新增或排除角色與候選需求句子。候選需求句子只用於確認 Roles，不寫入後續交付的 sbe。使用者已在需求中明確確認角色時，將該資訊視為確認結果。

在使用者確認前，不要整理正式的 Goals、Non-goals、Story、Rule 或 Scenario，也不要交付完整 sbe。候選角色不足以讓使用者判斷時，先詢問角色名稱、目標、權限或互動是否不同。

### 2. 整理術語與詞彙表

依 document/glossary/SKILL.md 整理需求中的 domain terminology，並依詞彙的適用範圍與重用關係選擇位置模式。選擇鑲嵌文件時，將已確認的術語寫入交付物的 Glossary 章節；選擇共用或分散 glossary 時，引用適用的 glossary，不重複定義詞彙。未確認的術語、名稱或適用範圍列入 Questions。

### 3. 界定 Goals 與 Non-goals

列出本次需求要達成的結果，以及刻意不包含的結果或能力。將會影響行為邊界的未決事項列入 Questions，不要自行推定為 Non-goals。

### 4. 描述 Stories

使用 user story 格式說明角色、目標與目的：

~~~text
As a <角色>,
I want <想完成的事情>,
so that <取得的價值或目的>.
~~~

為每個 Story 使用這個格式，並使用 Roles 已確認的角色名稱。

### 5. 進行 Example Mapping

為每個 Story 找出 Rules、說明各 Rule 的 Examples，並記錄 Questions。Example 包含情境、操作與可觀察的結果。

### 6. 轉成 Gherkin

將規格寫成 Feature、Rule 與 Scenario。Feature 只服務目前 Story 時，將它與 Rule 和 Scenario 直接寫在 Story 下方。Feature 服務多項 Story 時，將它集中定義為 Shared Feature；每個使用它的 Story 都以文件內連結參照，Shared Feature 的 Rule 與 Scenario 只定義一次。Story 還需要不同 Rule 或 Scenario 時，保留 Shared Feature 的參照，並加入自己的 Feature。

### 7. 檢查 Rules 與 Scenarios

確認 Rules 足以說明各 Story 的完成條件，且每個 Scenario 只說明一個 Rule。Scenario Outline 的 Examples 表格是資料列集合，不是 Example Mapping 的 Example。

### 8. 檢查範圍與待確認事項

確認 Goals 都由一個或多個 Rule 與 Scenario 說明，Non-goals 沒有與規格承諾的行為衝突，並列出仍會影響規格的待確認事項。

## Output

交付既有 sbe 的 diff 時，以下模板只需包含受影響的章節與 Feature 區塊。

    # <需求範圍名稱>

    ## Glossary

    <選擇鑲嵌文件時列出已確認的詞彙與定義；使用共用或分散 glossary 時，引用適用 glossary 的位置。>

    ## Roles

    - <角色名稱>：<此角色在本次需求中觸發、接收或驗證的行為>

    ## Goals

    - <本次需求完成後要達成的結果>

    ## Non-goals

    - <本次刻意不包含的結果或能力>

    ## Stories

    ### Story：<Story 名稱>

    As a <角色>,
    I want <想完成的事情>,
    so that <取得的價值或目的>.

    #### Questions

    - [ ] <待確認事項>
      - 影響：<受影響的行為、規則或驗收條件>
      - 暫定前提或需要決定：<目前採用的前提，或需要產品決定的事項>

    #### Feature：<此 Story 專屬的能力名稱>

    <交付 diff 時，在此 Feature 區塊標題後加入下列欄位。>

    - Change: [CREATE]

    ~~~gherkin
    Feature: <能力名稱>

      Rule: <團隊同意的業務規則或 acceptance criterion>

        Scenario: <可觀察的結果>
          Given <執行者與成立前需要的條件>
          When <執行的操作或開始事件>
          Then <系統結果與呼叫端可觀察的結果>
    ~~~

    <若本 Story 使用 Shared Feature，建立連至該共通能力的 Feature 標題與文件內連結。>

    <其他 Story 依相同結構加入。>

    ## Shared Features

    <只有服務多項 Story 的 Feature 才列在這裡；沒有時寫「無」。>

    ### Feature：<共通能力名稱>

    <交付 diff 時，在此 Feature 區塊標題後加入下列欄位。>

    - Change: [UPDATE]

    ~~~gherkin
    Feature: <能力名稱>

      Rule: <團隊同意的業務規則或 acceptance criterion>

        Scenario: <可觀察的結果>
          Given <執行者與成立前需要的條件>
          When <執行的操作或開始事件>
          Then <系統結果與呼叫端可觀察的結果>

        Scenario: <另一個情境或失敗結果>
          Given <執行者與成立前需要的條件>
          When <執行的操作或開始事件>
          Then <系統結果與呼叫端可觀察的結果>
    ~~~

    其他情境或失敗情境各自寫成 Scenario。不適合寫成 3 到 5 個步驟時，改用條列。

    其他章節沒有內容時，寫「無」。

    Questions 不是空白時，標示 sbe 為草稿；回答後將結果併入 Rule 或 Scenario，並移除 Questions。

## Validation

輸出前逐項檢查：

- 每個 Goal 都由一個或多個 Rule 與 Scenario 說明，並以 Feature、Rule 與 Scenario 表示。
- 每個 Non-goal 都是刻意排除的結果或能力，且沒有與任何 Rule 或 Scenario 衝突。
- 每個 domain terminology 都有已確認的定義，且依選定模式嵌入 sbe 或引用適用的 glossary。
- Roles 已由使用者確認，且每個角色都說明其在本次需求中觸發、接收或驗證的行為。
- 每個 Story 的角色都存在於 Roles，並使用相同名稱。
- 每個需求都已整理成一個或多個 Story、Rules、Examples 與 Questions。
- 每個 Story 都有一個或多個專屬 Feature，或有指向既有 Shared Feature 錨點的 Feature 連結。
- Shared Feature 的連結可到達唯一的 Rule 與 Scenario 定義。多項 Story 參照同一個 Shared Feature 時，不重複定義相同規格。
- 交付 diff 時，每個受影響的 Markdown Feature 區塊都有且只有一個獨立的 Change 欄位，值為 [CREATE]、[UPDATE] 或 [DELETE]，並與相對來源文件的行為變更相符。
- 非 diff 的交付中，Markdown Feature 區塊沒有 Change 欄位。
- Inputs 已包含本次要修改的功能之既有 sbe 時，交付物只包含受影響的區塊，並沿用來源文件的章節結構與名稱。
- 每個 Rule 都是關聯 Story 的 acceptance criterion，並以一個或多個 Example 或 Scenario 說明。
- 每個 Scenario 都能由使用者或其他呼叫端驗證，並只說明一個 Rule。
- 步驟與預期結果結構相同、只有輸入或前置狀態不同的情境，已合併為 Scenario Outline 與 Examples 表格。
- 行為正確性必要的失敗流程與限制都已描述。
- 每個 Questions 都說明影響範圍，以及暫定前提或需要產品決定的事項。
- Questions 沒有包含可安全排除的未來能力或臆測需求。
- 準備交付的 sbe 沒有未回答的 Questions；回答後已反映在 Rule 或 Scenario。
