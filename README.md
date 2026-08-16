# Skills

列出 repo 內可安裝的 skill

`npx skills add alexlautw9527/skills --list`

安裝 skill，互動式選擇要裝到哪些 agent

`npx skills add alexlautw9527/skills`

## Feature 文件流程

第一性原理：每增加一個文件要最小人工維護，最小化 LLM 推論成本與推論錯誤風險。文件分兩類：

- Artifact（.ux.md、實作計畫）：可以進 git，但合併前要刪掉。
- SSOT（蒸餾後的模組層級 AGENTS.md）：需要持久化，隨 feature 合進主分支。

1. UI 規格：Figma → `to-ui-spec` → .ux.md
2. 實作計畫：PRD + UI 規格 → `to-frontend-implementation-plan` → 實作計畫（含檔案變更總覽與 Story 覆蓋對照表）
3. 實作：依計畫執行，Final Validation 全過、變更與計畫一致為完成
4. 蒸餾：實作完成、merge 前，以 `to-local-agents-md` 更新 branch 觸及的模組層級 `AGENTS.md`
5. 合併：蒸餾過的 `AGENTS.md` 隨 feature 合進主分支（main/master）
