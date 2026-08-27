---
name: to-test-case
description: 使用 Vitest、Jest 或專案既有測試框架，產生或審查可執行的 regression test。適用於需要依需求、業務規則或公開介面防止行為回歸的單元、整合、元件與 API 測試；不以 coverage 或內部實作細節為目標。
---

產生或審查 regression test 時，以能防止已知或可預見的行為回歸為完成標準。regression test 應驗證呼叫端可觀察的結果；在不改變行為的重構後，測試通常不應失敗。

## Inputs

開始前取得與本次行為直接相關的材料：

- requirement、sbe、API contract、業務規則或已確認的 bug。
- 被測程式碼的公開介面、相依關係與既有測試。
- 專案已安裝的測試框架、測試指令、test environment 與 fixture 慣例。
- 需要驗證的整合邊界，例如資料庫、HTTP、queue、cache 或檔案系統。

先查閱專案指示文件與既有測試，沿用已安裝的 Vitest、Jest 或其他測試框架、assertion 風格與 test helper。沒有需求、規則或公開 contract 可以決定預期結果時，先列出缺少的依據；不得從目前實作反推 expected result。

## Constraints

- 每個 regression test 都要能說明它防止的 failure mode，以及失敗時會造成的可觀察錯誤。
- assertion 優先驗證回傳值、畫面、HTTP response、持久化後的資料、事件或其他外部 side effect。
- 不測 private method、內部 state、helper 呼叫順序、沒有 contract 意義的 CSS class，或只為了滿足 coverage 的分支。
- 測試彼此獨立，不依賴執行順序、前一個案例留下的資料或共用可變 state。
- mock 只隔離本次不需要驗證的外部邊界。資料庫 transaction、serialization、cache、queue 或實際依賴的行為需要成為驗證對象時，使用可隔離的真實 test dependency。
- 不在不同測試層級重複驗證相同的輸入排列組合。需要第二個層級時，該案例必須驗證第一個層級無法證明的介面或整合邊界。
- 不因為可生成大量測試而擴張測試範圍。每個新增案例都要對應已知規則、風險、邊界或失敗模式。
- 所有新增或修改的測試都必須依 AAA pattern 撰寫：Arrange 建立前置資料與必要 mock，Act 只執行被測行為，Assert 驗證可觀察結果。

## Workflow

1. 確認測試範圍

   若材料已定義 Invariant，先以它列出必須持續成立的行為與結果，再補充本次要維持的規則、公開 contract 與已知風險。每項行為寫出錯誤實作時會出現的 failure mode，以及呼叫端可觀察到的結果。

2. 選擇主要測試層級

   對每個 failure mode，選擇成本最低且足以可靠抓到錯誤的層級：
   - Unit test：純業務規則、計算、資料轉換、validation、條件分支與 boundary condition。
   - Component 或 frontend integration test：使用者輸入、loading、success、empty、error、權限差異，以及 API 結果造成的畫面與互動改變。使用 role、label 或可見文字等使用者可感知的 selector。
   - Backend integration test：資料庫 constraint、transaction、repository 行為、serialization、dependency wiring，或 queue、cache、檔案系統等整合邊界。
   - API test：request validation、status code、response schema、authentication、authorization 與最終資料狀態。
   - Contract test：獨立開發的 consumer 與 provider 對欄位、型別、格式或錯誤內容的約定。
   - E2E test：登入、結帳、付款、核心 CRUD 與跨前後端權限等少量主要使用流程。

   同一行為可以有不同層級的測試，但每個層級都要說明它額外驗證的邊界。能由 Unit 或 integration test 可靠驗證的規則，不移入 E2E。

3. 呼叫 `$mece` 檢查案例集合

   將「本次要維持的行為、規則與 failure mode」定義為母集合，將每個候選 regression test 視為分析單位，呼叫 `$mece` 檢查：
   - 每個 failure mode 是否至少有一個案例可驗證。
   - 兩個案例是否以相同測試層級與 assertion 驗證相同錯誤，因而重複。
   - 同一清單是否混合行為分類、測試層級與資料排列等不同維度。
   - 少量跨層測試是否各自驗證不同 contract 或 integration boundary。

   不要求測試層級本身互斥。測試層級、行為規則與資料排列是交叉維度，應分開檢查。

4. 撰寫可執行的測試程式碼

   在既有或新增的測試檔中，以目前專案的 Vitest、Jest 或相容 API 撰寫 regression test。每個案例以行為與結果命名，並使用 AAA pattern：

   - Arrange：建立輸入、前置狀態與必要 mock。
   - Act：執行一次被測行為。
   - Assert：驗證預期的可觀察結果與必要 side effect。

   以空白行分隔 AAA 區段。需要協助讀者辨識較複雜的 setup、操作或 assertion 群組時，使用 `// Arrange`、`// Act`、`// Assert` 註解；簡單案例的區段已由程式碼與空白行表達時，不新增重複註解。

   - 表單至少檢查有效輸入、必填欄位、無效輸入與後端錯誤。
   - 後端規則至少檢查成功流程與有意義的失敗流程；涉及授權時檢查 authorization 與資源 ownership。
   - API 測試同時檢查 response 與必要的最終狀態。
   - 結構相同、只有輸入與預期結果不同的案例，使用 `it.each`、`test.each` 或專案對應的 parameterized test，避免重複測試程式碼。

5. 驗證測試能抓到錯誤

   執行受影響的測試。對風險高或 AI 大量生成的案例，進行 mutation check：暫時反轉條件、修改 boundary、回傳錯誤值、移除授權檢查、略過寫入，或改錯 mapping。相關測試必須失敗；若仍通過，補強 assertion、調整 mock boundary 或重寫案例。

## 審查既有測試

審查測試時，依下列順序檢查：

1. 每個測試的 expected result 是否有 requirement、業務規則或公開 contract 支持。
2. assertion 是否驗證可觀察結果，且 production code 改錯時會失敗。
3. mock 是否只隔離不在本次驗證範圍的邊界。
4. AAA 區段是否清楚，且 Act 只執行被測行為，避免 setup 或 assertion 混入操作。
5. 測試層級是否足以驗證錯誤發生的位置，且沒有以較高成本層級重複同一規則。
6. parameterized case、fixture、setup 與 teardown 是否只有資料差異，可抽樣檢查代表案例。

優先重寫或刪除無法指出 failure mode、只增加 coverage、只驗證 mock、assertion 永遠成立、與其他案例重複，或 production code 改錯後仍通過的測試。

## Output

交付下列內容：

- 可執行的 regression test 程式碼，以及每個修改或新增測試檔的位置。
- 一份精簡的案例對照，列出 regression test 名稱、要防止的 failure mode、測試層級與主要可觀察 assertion。
- 使用 `$mece` 後發現並處理的重複案例、涵蓋缺口或交叉維度。
- 實際執行的測試指令與結果；若無法執行，說明阻礙與尚未驗證的範圍。

## Validation

- 每個 regression test 都有可追溯的 failure mode，且 expected result 不依賴目前實作才成立。
- 每個 assertion 都能證明外部可觀察行為或需要保證的公開 contract。
- 每個 failure mode 都由最低成本且足夠可靠的測試層級處理。
- `$mece` 已檢查本次案例集合的重複、遺漏、層級與分類維度。
- 測試獨立執行時可重現，且不依賴其他案例或共享可變 state。
- 所有測試都以 AAA pattern 分隔前置條件、操作與 assertion；AAA 註解只出現在程式碼或空白行不足以辨識區段的位置。
- 需要真實整合行為的測試沒有被 mock 取代。
- 主要流程的 E2E 測試數量有限，且沒有重複 Unit、integration 或 API 測試已可靠驗證的排列組合。
- 已執行受影響的測試；高風險或大量生成的案例已完成適當的 mutation check。
