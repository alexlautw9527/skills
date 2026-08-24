# 來源資料規則

本檔定義每個 Section 可以採用哪些資料，以及資料應寫入正式規格的哪個位置。工具呼叫與檔案更新步驟由 [SKILL.md](../SKILL.md) 規範；正式文件欄位由 [formal-template.md](formal-template.md) 規範。

## 每個 Section 可以採用的資料

每個 Section 只採用下列資料：

- Section `來源：` 所連 Figma node 及其子孫 node 中的 native annotations。
- 該 Section `### Sources` 依 `scaffold-template.md` 格式逐行列出的補充資料。

HTML 註解與空白行不算來源。只出現在對話中、尚未寫入 `### Sources` 的圖片也不算來源，應先請使用者補入 scaffold。

每筆資料只能歸到列出它的 Section。不得因另一個 Section 使用相同文字、元件或畫面而混用資料。

## Figma 內容

- Native annotation 是主要資料。使用 annotation 的完整原文，並保留其中的連結。
- 畫布上的說明框、標籤或 callout 元件不會自動算作 annotation。只有使用者把它列入 `### Sources` 或明確指定為補充資料時才能採用。
- Section 名稱或內容若代表 error、overflow、onblur 等狀態，且沒有 annotation，檢查該 Section 來源 node 中可見的狀態與文字。能判斷的錯誤訊息、必填提示或狀態變化可寫成 UI 驗收項；無法判斷時建立 Question。

## URL 的寫入位置

依 URL 用途決定位置：

- UI 驗收項的主要資料：寫入該項 `來源：`。
- Annotation 描述操作後會開啟另一個 Figma 畫面：在對應驗證步驟附上該 Figma URL，連結文字使用目標畫面的標題或名稱。
- Annotation 連到外部規格頁面：寫入對應 UI 驗收項或 Question 的 `來源：`。
- 跨檔 UI ID：依 `formal-template.md` 寫入 `關聯：`。

Annotation 連到另一個 Figma node 時，只能使用該 URL 表示操作後開啟的畫面。除非該 node 也明列於目前 Section 的 `來源：` 或 `### Sources`，不得讀取它的子孫 node 或 annotations。

若 annotation 沒有目標 URL，先比對同一份 scaffold 其他 Section 的標題與來源連結。能明確對應時使用該 Section 的來源 URL；仍無法判斷時建立 Question。

## 圖片連結文字

正式 `.ux.md` 中的圖片連結文字必須描述畫面、狀態或標註內容，讓讀者不開啟連結也能理解來源。不得使用 `.png` 檔名或檔案路徑，也不得在正式規格正文使用「截圖」二字。

Scaffold 的 Reading Guide 可以使用「手動截圖」描述作者操作，因為該段不屬於正式規格正文。

## 判斷哪些資料可以形成 UI 驗收項或 Question

- 資料足以寫出可觀察結果時，在來源整理結果中標成可轉為 UI 驗收項的要求。
- 一筆 annotation 或補充資料包含多個可獨立驗收的要求時，拆成多項。每項都要保留自己的前置條件。
- 多個步驟共用同一前置條件，或後一步依賴前一步結果時，合併成一項，並保留連續步驟。
- 資料指出存在某項行為，但缺少畫面、文案、條件或結果而無法完成規格時，在來源整理結果中建立 Question 並說明還缺什麼。
- Section 完全沒有 annotation 或有效補充資料時，在來源整理結果中標明沒有可寫入內容。第 4 階段只保留 Section 標題與 `來源：`，不建立 UI 驗收項，也不因沒有資料建立 Question。
