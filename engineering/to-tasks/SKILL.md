---
name: to-tasks
description: 將已確認的 slice 與 plan 拆成可由單一開發者或 coding agent 實作、驗證與 review 的工程 task。當使用者要求安排實作工作或建立可 review 的工作單位時使用。
---
> 執行本 skill 時，預設一併讀取 `make-ai-readable-zh` skill。

task 是一組由同一人或 agent 連續完成的改動。它有一項主要工程責任、可判斷的完成結果，以及能證明結果的驗證方式。所有 task 完成後，必須能以 slice 原本的方式驗證交付結果。

本 skill 不重新定義需求、調整 slice 邊界或改變 plan 已決定的架構。

## Inputs

開始前取得下列資料：

- slice 的行為、Scope、Out of Scope 與驗證方式。
- plan 的 Map、Constraints、既有模式與預定改法。
- 相關程式碼、專案指示、資料流、介面與測試方式。
- 開發範圍：`frontend`、`backend` 或 `fullstack`。
- 已知相依工作、外部責任、介面可用時間與發布限制。

先讀取 repository 根目錄的 `GLOSSARY.md`。輸出章節與用語優先使用其中已定義的名稱；需要新名稱時，先確認詞彙表沒有能表達相同意思的既有用語。

## Questions

- 尚未確認但仍可安全拆分的資訊，列出問題與目前採用的前提。
- 會改變實作方法、資料正確性、安全性、責任邊界或 task 順序的資訊，停止拆分並列為阻礙。
- plan 與目前程式碼不一致時，列出衝突證據與受影響的 task。
- 不假設 repository 中不存在的介面、資料模型、共用元件或抽象層。

## Constraints

- slice 已決定行為與交付邊界。task 拆分不得改變它；範圍無法合理拆分時，列入 Questions，並依既有邊界提出可執行的 task。
- 每個 task 只負責一項連貫的工程結果，名稱應描述該結果。
- 只有拆分後的 task 都能獨立 review 與 Validation 時才拆開；否則維持同一個 task。
- 每個 task 都要列出 Goal、Scope、Out of Scope、Constraints 與 Validation。Validation 選擇足以證明風險的最低層級。
- 沿用已確認的實作方向，只納入目前 slice 需要的工作；不為未確認的需求擴張架構或建立尚未使用的共用能力。

## Workflow

1. 確認 slice 內容，並在輸出中直接連結該 slice；不要重述內容。
2. 依 slice、plan 與 repository context，辨識完成這個 slice 所需的工程責任，以及責任之間的相依關係。
3. 依上述 Constraints，將工程責任組成 task。
4. 責任有獨立風險或失敗情境時，可以獨立成 task，但必須有完整完成條件。
5. 為每個 task 寫出 Goal、Scope、Out of Scope、Constraints 與 Validation。task 的 Validation 證明工程責任已完成；所有 task 完成後，依 slice 原本的驗證方式確認交付結果。
6. 依相依關係、風險、外部限制與取得回饋的順序安排 task，不依固定技術層排序。

## Validation

依要證明的結果選擇測試層級：

| 要證明的結果                              | 驗證方式                                  |
| ----------------------------------------- | ----------------------------------------- |
| 商業規則或演算法                          | Unit test                                 |
| 資料庫、transaction、queue 或外部服務整合 | Integration test 或 contract test         |
| API 的 request 與 response                | API integration test 或 contract test     |
| 前端元件與狀態互動                        | Component test 或 integration test        |
| 跨前後端的主要流程或跨層權限              | 少量 integration test 或 acceptance / E2E |

輸出前確認：

- 每個 task 都服務原 slice，且沒有改變 plan 的架構決策。
- 每個 task 只有一項主要責任，完成後可單獨 review 與驗證。
- Scope、Out of Scope、相依關係與 Constraints 足以判斷何時完成。
- task Validation 與 slice Validation 分開描述。
- 所有 task 完成後，可以執行 slice 原本的驗證方式。

## Output

```markdown
## slice

<已確認的 slice 文件或工作項目連結>

## Questions

- <尚未確認的事項與目前前提>

若無則寫「無」。

## Constraints

- <會影響所有 task 的既有做法、責任邊界或外部限制>

## task 1：<工程責任名稱>

### Goal

<完成後新增或改變的工程能力>

### Scope

- <必須完成的改動>

### Out of Scope

- <刻意不處理的內容>

### Constraints

- <實際相依、既有做法與不可違反的條件>

### Validation

- <這個 task 要證明的結果、測試層級與必要案例>
- <完成後能否驗證整個 slice；若不能，列出仍缺少的 task>

## task 2：<工程責任名稱>

...

## Workflow

1. task X：<相依、風險或回饋原因>
2. task Y：<相依、風險或回饋原因>

## Validation

- <所有 task 完成後要執行的原 slice 驗證方式>
```

沒有內容的 `Questions` 或 `Constraints` 寫「無」。
