---
name: make-id-stable
description: 設計或審查 requirement、story、ADR、test case、API spec 等長期引用項目的識別碼規則時使用。確保 ID 只表示永久 identity，不受排序、改名、搬移或刪除的連鎖影響。
---

## 目的

識別碼只用來表示項目的永久 identity。排序、標題、檔名、路徑、分類、狀態等可變資訊必須分開管理，避免重新排序、搬移、刪除或改名時產生大量連鎖引用修改。

適用於 requirement、story、ADR、test case、API spec 等需要長期引用的項目。

不適用於一次性草稿、臨時筆記，以及沒有跨項目引用的純展示內容：沒有引用者的位置，ID 只是多餘的維護成本。

## 建議格式

除非專案已有其他 ID 規則，優先使用沒有業務語意的隨機 ID（opaque）：

```text
<TYPE>-<8~12 字元隨機 ID>
```

例如：

```text
REQ-3ZGUEWQV
ADR-R6XW42PK
TEST-EU7SXKGY
```

- `REQ-`、`ADR-` 等類型前綴只有在類型不會改變時才能放進 ID。
- 隨機段 8~12 字元是碰撞風險與可讀性的平衡：用 29 個字元的字元集時，10 字元即有約 4×10 的 14 次方種組合，隨機生成的碰撞可以忽略。
- 字元集以 base32（RFC 4648）的 A-Z 加 2-7 為基礎，再排除字形容易混淆的 I、L、O，其餘 23 個字母加 2-7 共 29 字元。0、1、8、9 不在字元集內，人眼不會混淆。
- 產生 ID 一律用 `scripts/generate-id.sh <TYPE> [LENGTH]`，例如 `generate-id.sh REQ` 輸出 `REQ-` 加 8 個隨機字元。

ID 只表示永久 identity；排序、名稱、位置與其他組織資訊另外維護。

## 規則

- ID 建立後永久不變。
- 已使用過的 ID 永遠不得回收或重新指派。
- ID 不表示排序，也不得因插入、刪除或重新排序而重新編號。
- ID 不得編碼可能變動的資訊，包括：
  - 標題
  - heading
  - 排序
  - 文件階層
  - 檔名與路徑
  - slug
  - 分類
  - owner
  - status
- 跨項目引用必須以 ID 為準。標題只能作為顯示文字。
- 拆分項目時，原 ID 保留給範圍最接近原項目的那一部分，拆出的新項目各自取得新 ID；原 ID 不刪除。
- 合併項目時，保留其中一個既有 ID 給合併後的項目，其餘被合併項目的 ID 永久停用，不得轉給其他項目。

例如：

```yaml
id: REQ-3ZGUEWQV
title: Password reset
area: authentication
status: approved
```

改名、搬移或重新分類後：

```yaml
id: REQ-3ZGUEWQV
title: Recover account by email
area: account-recovery
status: approved
```

ID 不變。

## 既有結構化 ID 的遷移

不要為了符合新格式而立即全量重編既有 ID：重新編號會迫使所有引用同時修改，且外部系統可能仍以舊格式引用。

- 既有 ID 沒有違規：保留原樣，只對新項目套用新格式。
- 既有 ID 已編碼結構（例如 `REQ-001`、`AUTH-LOGIN-003`）且已有跨項目引用：保留舊 ID，只讓新項目採用新格式，兩者並存。
- 必須全面重編時（例如尚無任何外部引用）：一次性完成所有項目與引用的更新，不可半遷移造成新舊格式混用。
- 有外部系統以舊格式引用時：先與引用方協調，或保留一份舊 ID 對照新 ID 的對應表，直到外部引用全部更新。

## Anti-pattern

不要使用會把 identity 與目前結構綁在一起的格式：

```text
REQ-001
AUTH-LOGIN-003
CH3-REQ-04
API-USERS-GET-02
requirements/auth/password-reset
```

這些資訊一旦改變，就可能迫使其他引用一起修改。

## 檢查方式

設計或 review ID 規則時，確認以下操作都不需要修改既有 ID 或無關引用：

- 插入新項目
- 重新排序
- 改標題
- 改 heading
- 搬移或重新命名檔案
- 改分類
- 拆分或合併項目
- 刪除項目
- 多個 Git branch 同時新增項目

如果其中任何操作會造成大量 reference-only 修改，就應把造成變動的資訊從 ID 或 reference target 中移除。
