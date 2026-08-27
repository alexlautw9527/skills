---
name: frontend-solid-pattern
description: 設計、實作或審查前端功能的模組邊界、狀態與相依關係時使用。依 SOLID 的設計精神隔離變更原因、保留可替換介面，並讓核心邏輯不受框架與基礎設施綁定。
---

# Frontend SOLID Pattern

將 SOLID 的設計精神套用到前端程式碼，不限制 React、Vue、Angular、Svelte 或其他框架。適用於功能設計、重構與程式碼審查；不以介面、class 或 design pattern 的數量作為品質指標。

## Goal

讓每個前端功能能在需求改變時，將修改限制在直接負責該變化的程式碼，同時維持資料、狀態與副作用的責任歸屬清楚。

## Scope

本 skill 處理四個彼此獨立的設計面向：

- 責任與檔案位置：程式碼為何修改，以及相關程式碼是否放在能一起理解與修改的位置。
- 可替換與擴充：何時需要擴充位置，以及不同實作應維持的介面約定。
- 依賴方向：模組取得多少資料與能力，核心邏輯如何隔離框架與外部系統。
- 狀態與邏輯：誰維護同一份資訊，以及哪些邏輯能脫離框架執行。

需要定義 View、State & Logic、Data Access 與 Data Sources 的分層、介面與測試方式時，讀取 [frontend-testable-view-pattern](../frontend-testable-view-pattern/SKILL.md)。本 skill 用來判斷該架構內的責任邊界；該 skill 用來定義 View 可獨立測試的資料流與實作慣例。

## Workflow

1. 列出功能中的呈現、狀態、商業規則、資料轉換、I/O 與外部整合，確認各部分因哪些需求而改變。
2. 依序檢查本 skill 的四個設計面向，找出責任混雜、重複狀態、過寬依賴與不必要抽象。
3. 只對已知的變化、替換或測試需求建立模組邊界與擴充位置。
4. 修改後以 `Validation` 檢查責任、依賴與行為是否仍符合需求。

## 責任與檔案位置

### 依變更原因分離責任

依程式碼會因為什麼需求而修改，安排責任邊界。常見的獨立原因包括：

- UI 呈現。
- 狀態轉換。
- 商業規則與輸入驗證。
- 資料轉換與資料讀寫。
- 分析事件與外部 SDK 整合。

- 一個模組同時因多種互不相關的需求修改時，拆出直接負責各需求的單元。
- 函式短小或檔案行數少，不能證明責任已經分開。只因同一項需求而一起修改的程式碼可以留在同一單元。
- 不將呈現、商業規則、資料讀寫與第三方整合集中在同一個 manager、service 或元件。

### 保留功能程式碼的鄰近性

同一功能的 UI、狀態、資料轉換、資料存取與測試，應放在容易一起發現與修改的位置。

- 依功能放置程式碼；只有跨功能共用且介面穩定的內容才提升到 shared 層。
- 分離責任後，修改一項功能不應需要穿梭大量只按技術類型分類的目錄。
- 重複出現的程式碼先確認是否有共同且穩定的責任。只有確定後才抽成共用模組。

## 可替換與擴充

### 針對持續增加的變化提供擴充位置

已知會持續增加種類的行為，可以由明確的介面約定、資料映射、composition 或 strategy 負責分派。常見情境包括付款方式、驗證器、欄位類型、表格欄位、格式化器、渲染器、命令處理器、外掛與儲存實作。

- 新增一種類型時，優先新增該類型的 implementation 與登錄資料，避免持續修改中央 `if`、`switch` 或大型 dispatcher。
- 只有有限且穩定的狀態直接使用條件分支，例如載入中、已停用或資料不存在。
- 尚未出現替換需求、外部邊界或持續增加的變化時，保留直接的局部實作。

### 讓符合相同介面約定的實作可互換

兩個 implementation 即使通過同一個 TypeScript 型別，呼叫端仍可能需要用不同方式處理它們。例如，其中一個查無資料時回傳 `null`，另一個拋出錯誤，呼叫端就無法直接替換。以下約定必須一致：

- 接受哪些輸入。
- 回傳結果代表什麼。
- 如何回報錯誤。
- 會產生哪些副作用。
- 非同步結果何時完成或失敗。
- UI 元件也要定義 disabled、readonly、loading 等狀態的行為，以及 callback 觸發時機。
- 測試替身與 production implementation 都要遵守相同介面約定；測試方便不能改變呼叫端觀察到的行為。

## 依賴方向

### 只依賴工作所需的資料與能力

元件、函式與模組只接收完成工作需要的資料欄位與能力。

- Leaf component 依自身呈現需求定義資料，不接收完整 domain model、application context 或 API response。
- 函式只依賴所需能力，例如注入「取得折扣」的函式，而非整個 API client、設定與 service 集合。
- 當 dependency 只為了轉交給下一層，縮小呼叫端介面，讓真正使用它的地方直接取得所需能力。

### 由外層連接框架與基礎設施

domain 與 application logic 依賴自身需要的能力，不直接綁定下列具體實作：

- UI framework。
- HTTP client。
- browser API 與儲存機制。
- router 與全域 singleton。
- 第三方 SDK。

- 外層 adapter 將 framework 的 reactivity、lifecycle 與事件，連接到 application API。
- HTTP、storage、analytics 與 SDK adapter 實作核心定義的讀寫或操作能力。
- 注入 dependency 時，將組裝位置放在 application 邊界，讓核心可用明確輸入與輸出驗證。

## 狀態與邏輯

### 指定同一份資訊的唯一主要維護位置

每份資訊指定一個主要 state owner。其他位置讀取它、由它推導結果，或在需要時送出事件請它更新。

- URL、全域 state、功能內共用 state、表單 state 與元件 local state 不應各自保存同一份可變資料後再以 effect、watch 或 listener 同步。
- 新增 state 前先判斷能否由既有 state 推導。可以推導時，不保存另一份副本。
- 同一資訊必須跨邊界同步時，明確定義主要維護位置、更新入口與衝突處理方式。

### 將不依賴框架的邏輯保持為普通程式

下列邏輯能用普通 TypeScript 或 JavaScript 函式表示時，保持為普通函式：

- 商業規則與驗證。
- 資料轉換與狀態轉換。
- 決策邏輯。

- 純函式接收明確輸入並回傳結果，不讀取 lifecycle、reactivity、DOM、HTTP、storage、router 或 UI event object。
- framework 專屬程式負責 rendering、reactivity、lifecycle 與事件綁定。
- 將邏輯包進 hook、composable、service 或 store 前，確認它確實需要框架能力，或該邊界有獨立的狀態與副作用責任。

## 抽象的判斷

符合下列任一條件時，可以考慮建立抽象、介面或 adapter：

- 已存在兩個以上可互換的 implementation。
- dependency 是外部系統、browser API 或第三方 SDK。
- 行為有已知且持續增加的變化維度。
- 邊界需要獨立測試或替換。
- 呼叫端與實作有不同的變更原因。
- 不隔離會讓 domain 或 application logic 直接依賴 framework 或基礎設施。

其餘情況優先使用普通函式、資料結構與局部 composition。避免為每個 class 建立 interface，或建立沒有替換需求的 `IService`、`ServiceImpl`、factory、provider 與多層繼承架構。

## Review Questions

- 哪些需求會修改這段程式碼？它們是否屬於不同責任？
- 新增同類型行為時，會新增 implementation 還是擴大中央分派邏輯？
- 可互換的 implementation 是否對輸入、輸出、錯誤、副作用與非同步行為維持相同約定？
- 此模組知道或接收的資料、dependency 是否超過完成工作所需範圍？
- 核心邏輯是否直接使用 framework 或外部系統？
- 同一份資訊是否有多個 state owner，並透過同步程式維持一致？
- 哪些邏輯能用不依賴框架的函式表達？
- 分離責任後，修改一項功能需要跨越哪些不直接相關的位置？
- 新增的抽象對應哪一項已知的替換或變化需求？

## Validation

- 每個模組的責任可由它會因哪類需求修改來說明。
- 新增同類型行為不必修改不直接負責該類型的既有程式碼，除非中央登錄資料是刻意的擴充位置。
- 符合相同介面約定的 implementation 可以互換，且測試覆蓋呼叫端可觀察到的行為。
- 元件與模組只依賴所需資料與能力；核心邏輯不直接依賴 framework 或基礎設施。
- 每份可變資訊都有明確 state owner，衍生資料沒有被當成獨立 state 保存。
- 同一功能的程式碼維持可發現性，新增的抽象有已知需求支持。
