# Invariant 的技術含義

## 結論

Invariant 是一個可判定真假的條件，也就是 state predicate。這個條件必須在指定範圍的每個合法或可到達狀態成立。初始狀態必須符合條件；後續允許的狀態轉換必須保持條件，或在指定的觀察邊界前恢復條件。

Invariant 維持的是條件的真值。資料本身可以改變。例如帳戶餘額與交易項目都可以增加，只要「餘額等於有效交易總和」仍然成立。

「難以從程式碼推論」不屬於 invariant 的定義。它適合作為 `AGENTS.md` 的收錄條件：先判斷某項規則是否為 invariant，再判斷這項 invariant 是否難以從局部程式碼確認，或每次重新推導是否會耗費大量 token。

「替換技術後仍須成立」也不是所有 invariant 的必要條件。Domain 或 API invariant 通常跨實作維持；representation invariant 與 loop invariant 可能隨實作方式改變。

## 不同種類的成立範圍

- System invariant 是所有可到達系統狀態都符合的 state predicate。TLA+ 也區分 invariant 與 inductive invariant：後者除了在所有初始狀態成立，也能被每一步狀態轉換直接保持。
- Loop invariant 在進入迴圈及每次執行迴圈內容後成立。迴圈內容執行途中可以暫時不成立，但必須在下一次條件判斷前恢復。
- Class 或 object invariant 描述有效物件必須符合的條件。它在物件建立完成及公開操作的進入、離開邊界成立；物件從一個一致狀態轉換到另一個一致狀態時可以暫時不成立。
- Representation invariant 定義哪些內部資料值是抽象資料型別的合法表示。所有建立或修改該表示的操作都必須產生仍符合條件的結果。

## 對 AGENTS.md 的分類建議

先用以下條件判斷一項資訊是否為 invariant：

1. 它能表達成對狀態判定真假的條件。
2. 它明確指出成立範圍，例如所有可到達狀態、公開操作邊界或每次迴圈迭代邊界。
3. 建立初始狀態的操作會使條件成立。
4. 所有允許的狀態變更都會保持條件，或在指定邊界前恢復條件。

符合 invariant 定義後，再用以下條件決定是否寫入 `AGENTS.md`：

- 這項條件會影響修改決策。
- LLM 容易依一般慣例推論錯誤，或無法從局部程式碼、型別與工具設定直接確認。
- 每次重新推導都必須跨大量程式碼、測試、設定或外部文件，會耗費大量 token。

## Primary sources

- Leslie Lamport, [Using TLC to Check Inductive Invariance](https://lamport.azurewebsites.net/tla/inductive-invariant.pdf)：invariant 在所有可到達狀態成立；inductive invariant 由初始條件與每一步保持條件共同建立。
- TLA+ Toolbox, [Model Overview Page](https://tla.msr-inria.inria.fr/tlatoolbox/doc/model/overview-page.html)：將 invariant 定義為所有可到達狀態都成立的 state predicate。
- Dafny, [Reference Manual](https://dafny.org/dafny/DafnyRef/out/DafnyRef.pdf)：loop invariant 在進入迴圈及每次執行迴圈內容後成立。
- Eiffel, [Design by Contract and Assertions](https://www.eiffel.org/doc/eiffel/I2E-_Design_by_Contract_and_Assertions)：class invariant 在物件建立完成及公開 routine 呼叫完成後成立。
- Oracle, [Programming With Assertions](https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html)：class invariant 適用於物件的一致狀態，可在兩個一致狀態之間的轉換期間暫時不成立。
- Cornell CS 3110, [Abstraction Functions and Representation Invariants](https://www.cs.cornell.edu/courses/cs3110/2010sp/Lectures/lec08.html)：representation invariant 定義哪些具體資料值是抽象值的合法表示，所有操作都必須維持這項限制。
