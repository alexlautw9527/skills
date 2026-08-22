---
name: to-sbe
description: 將使用者需求、產品規格、設計稿或既有行為整理成 Specification by Example（SBE）。當使用者要求用具體情境、規則與驗收條件釐清系統行為、例外情境或既有行為變更時使用；不處理實作、架構、Slice 或 task 的規劃。
---

將一項 Story 整理成 Rules、用來說明各 Rule 的 Examples，以及尚待回答的 Questions，再以 Gherkin 的 Feature、Rule 與 Scenario 交付。SBE 說明系統應遵守什麼規則與如何驗證結果，不決定實作方式。

## Inputs

取得下列資訊：

- 使用者需求、產品想法、issue 或 ticket。
- PM spec、PRD、設計稿或 prototype。
- 既有產品行為。
- 目標使用者與使用情境。
- 已知限制，例如權限、安全性、資料正確性、相容性或法規要求。

資訊不足時，不要因次要未知資訊停止整理。

- 可能影響行為邊界、完成條件、權限、資料規則、流程或驗收方式的資訊，列入 `Questions`。
- 能以暫定前提繼續整理時，在同一項 `Questions` 寫出採用的前提；無法安全採用前提時，寫出需要產品決定的事項。不要默默決定。
- 不要把尚未要求、可安全排除的未來能力列為 `Questions`；改列入 `Out of Scope`，或不提及。

## Constraints

以 Story、Rule 與 Example 描述需求，不以功能名稱或實作活動描述。

- 寫出誰可以完成什麼事情、系統在什麼條件下如何回應，以及呼叫端如何知道結果成立。
- 不將新增按鈕、建立元件、建立 API 或資料表等實作活動當成行為。
- 不指定 class、function、資料庫 schema、API endpoint、framework、程式碼目錄或特定技術方案。這些決策屬於 implementation plan 或 system design。

每個 Rule 都是團隊同意的 acceptance criterion，可以描述允許的行為、預期結果或限制條件。每個 Scenario 只說明一個 Rule，並包含：

- 誰執行。
- 在什麼情境下開始。
- 執行什麼操作。
- 系統產生什麼結果。
- 呼叫端如何確認結果成立。

可用 3 到 5 個步驟清楚表達的情境，使用正式 Gherkin 的 `Scenario`、`Given`、`When`、`Then` 與必要的 `And` 或 `But`。替代與失敗情境各自寫成 `Scenario`。流程過長且不能切成可獨立驗證的情境時，改用條列，不要把冗長流程偽裝成 Gherkin。

`Scenario` 是 Gherkin 對 Example 的名稱。Feature、Rule 與 Scenario 合在一起，構成可交付、可驗證的規格。

Questions 是釐清 Story 時的暫時記錄。Questions 尚未回答時，SBE 仍是草稿；答案應形成或調整 Rule 與 Example，而不是保留在準備交付的規格中。

補上行為正確性必要的非成功流程，例如沒有結果、無效輸入、權限不足、可恢復失敗、破壞性操作確認或狀態衝突。不要列出不影響呼叫端結果的純技術 edge case。

Rule 可以描述允許的行為，例如使用者可以取消預約，也可以描述限制，例如付款完成超過 24 小時後不可取消。Rule 不改寫成操作流程。

修改既有系統時，描述目前行為與行為變更。不要只描述新增需求而省略將被修改、移除或保持的行為。

## Workflow

### 1. 描述 Story

使用 user story 格式說明角色、目標與目的：

```text
As a <角色>,
I want <想完成的事情>,
so that <取得的價值或目的>.
```

### 2. 進行 Example Mapping

為 Story 找出 Rules、說明各 Rule 的 Examples，並記錄 Questions。Example 包含情境、操作與可觀察的結果。

### 3. 轉成 Gherkin

將規格寫成 Feature、Rule 與 Scenario。Story 與 Feature 的對應由需求範圍決定；不要預設一項 Story 只對應一項 Feature。

### 4. 檢查 Rules 與 Scenarios

確認 Rules 足以說明 Story 的完成條件，且每個 Scenario 只說明一個 Rule。相同 Scenario 需要多組輸入與預期結果驗證時，使用 `Scenario Outline` 與 `Examples` 表格；這個 `Examples` 表格是資料列集合，不是 Example Mapping 的 Example。

### 5. 標記範圍與待確認事項

列出刻意不包含的能力，以及仍會影響規格的待確認事項。

## Output

````markdown
# Specification by Example

## Story

As a <角色>,
I want <想完成的事情>,
so that <取得的價值或目的>.

## Features

<每個 Feature 各自寫成一個 Gherkin block。>

```gherkin
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
```

其他情境或失敗情境各自寫成 `Scenario`。不適合寫成 3 到 5 個步驟時，改用條列。

同一情境需要多組輸入時，在相同 Rule 下使用 `Scenario Outline` 與 `Examples` 表格。該表格的每一列是一組測試資料，不是 Example Mapping 的 Example。

## Out of Scope

- <刻意不包含的能力>

## Questions

- <待確認事項>
  - 影響：<受影響的行為、規則或驗收條件>
  - 暫定前提或需要決定：<目前採用的前提，或需要產品決定的事項>
````

其他章節沒有內容時，寫「無」。

`Questions` 不是空白時，標示 SBE 為草稿；回答後將結果併入 Rule 或 Scenario，並移除 Questions。

## Validation

輸出前逐項檢查：

- 每個需求都已整理成 Story、Rules、Examples 與 Questions，並以 Feature、Rule 與 Scenario 表示。
- 沒有以技術實作描述需求或完成條件。
- 每個 Rule 都是該 Story 的 acceptance criterion，並以一個或多個 Example 或 Scenario 說明。
- 每個 `Scenario` 都能由使用者或其他呼叫端驗證，並只說明一個 Rule；需要多組資料時使用 `Scenario Outline` 與 `Examples`。
- 行為正確性必要的失敗流程與限制都已描述。
- 每個 `Questions` 都說明影響範圍，以及暫定前提或需要產品決定的事項。
- `Questions` 沒有包含可安全排除的未來能力或臆測需求。
- 準備交付的 SBE 沒有未回答的 Questions；回答後已反映在 Rule 或 Scenario。
- 沒有提前決定架構、API、資料模型或 framework。
- 沒有將 Slice 或 task 拆解混入 SBE。
