---
name: engineer-eli5
description: 用足以讓工程師預測系統行為的最小正確模型，解釋陌生的軟體工程概念或新接觸的專案。當使用者要求 ELI5、簡單解釋、白話解釋，想理解陌生的技術、協定、架構、framework、演算法、基礎設施元件，或想快速理解一個不熟悉的專案在做什麼、怎麼運作時使用；使用者明確要求正式規格、完整實作、API reference 或完整 internals 時不使用。
---
> 執行本 skill 時，預設一併讀取 `make-ai-readable-zh` skill。

# Engineer ELI5

## Goal

用足以讓工程師預測系統行為的最小正確模型，解釋陌生的工程概念或新接觸的專案。先建立可以實際拿來理解系統的心智模型，再逐層補上前面省略的機制、限制、抽象層與失敗情境。

## 使用時機

當使用者有以下需求時使用：

- 想簡單理解軟體工程或電腦科學概念。
- 使用 `ELI5`、`簡單解釋`、`白話解釋`、`我不懂 X` 等說法。
- 想理解陌生的技術、協定、架構、framework、演算法、基礎設施元件或程式語言行為。
- 想快速理解一個沒接觸過的專案：它在做什麼、有哪些部分、一次操作怎麼走完。
- 想先建立基本心智模型，再去讀正式文件或原始碼。
- 想知道某個系統「為什麼會這樣運作」，但還不需要完整 implementation 細節。

例如：

- `ELI5 Raft`
- `簡單解釋 Kubernetes networking`
- `我會寫後端，但不懂 eBPF`
- `為什麼 React 要 reconciliation？`
- `用工程師聽得懂的方式解釋 MVCC`
- `我知道 HTTP，但 QUIC 到底在做什麼？`
- `ELI5 這個 repo`
- `我要接手這個 service，先給我整體概念`

## Constraints

- 使用者明確要求正式規格、完整實作、API reference、數學證明、benchmark 分析或完整 internals 時，直接照使用者需要的層次回答，不套用 ELI5 深度。
- 不把讀者當成兒童。除非理解目前主題真的需要，否則不從「什麼是程式」這種層次開始解釋。
- 圖不能取代文字的因果說明；生成圖片不能取代文字解釋。

## 預設讀者背景

除非使用者另外說明，假設讀者：

- 會寫程式。
- 知道 function、process、memory、API、database、request、file、network 等基本概念。
- 可能完全不熟目前這個技術領域。
- 不應假設他知道該領域的專有名詞、協定細節、framework internals、分散式系統理論或縮寫。

## 解釋深度

依使用者的問法自動判斷深度，不需要把 depth 參數暴露給使用者。

### Depth 1：快速建立方向感

目標：讀者能在一個畫面左右理解這個概念，之後看到時知道它大概在做什麼。

至少包含：

- 解決的問題。
- 最小模型。
- 一次流程。
- 一個限制。

### Depth 2：可以開始工作

目標：讀者可以讀一般 documentation、參與 code review，並推理常見行為。

包含：

- 運作機制。
- 設計取捨。
- 常見正式術語。
- 工程上的影響。
- 主要 failure mode。

這是預設深度。

### Depth 3：可以開始 implementation 或 debugging

目標：讀者有足夠模型開始實作、debug 或操作這個系統。

包含：

- 主要內部 state。
- state transition。
- invariant 或 guarantee。
- concurrency 或 failure behavior。
- debugging signal。
- 常見 implementation mistake。

Depth 3 仍然是解釋，不是 implementation 文件。

## Workflow

1. 說明它解決什麼問題。
2. 建立最小心智模型。
3. 畫出這個模型。
4. 用一個具體案例走一次流程。
5. 說明為什麼這樣設計。
6. 接到實際工程情境。
7. 畫出必要的 failure、state change 或第二層模型。
8. 指出簡化模型省略了什麼。
9. 告訴讀者下一層可以理解哪些概念。

不要求每次都一定有兩張圖。第一張圖已經足以解釋問題時，不要為了滿足格式多畫一張。

### 解釋新專案時的調整

Workflow 的步驟同樣適用，只是對象從單一概念換成一個專案：

- 第 1 步改為說明專案為誰解決什麼問題，以及它刻意不做什麼。
- 第 2 步把主要模組或 service 當成系統裡的角色介紹，說明各自負責什麼，而不是逐目錄列檔案結構。
- 第 4 步挑一個具體入口走完一次：一次 request、一個指令、一個主要工作流程。讓讀者看到控制權怎麼在模組之間移動。
- 額外說明閱讀與修改的切入點：想改某一類行為時，通常從哪裡開始看、會動到哪些部分。
- 簡化模型的界線同樣要交代：這個層次的模型省略了哪些子系統、設定與部署細節。

## 合格解釋的標準

一個合格的解釋，至少應讓讀者能回答：

1. 這個東西解決什麼問題？
2. 系統裡有哪些主要角色或元件？（解釋專案時：主要模組各自負責什麼）
3. 正常情況下，資料或控制流程怎麼走？
4. 為什麼要這樣設計？
5. 放進真實系統後，工程師會看到什麼行為？
6. 連線或元件處於正常狀態，不代表 application 正常。例如 network partition 可能讓 application 看到 latency 突然升高，但 TCP connection 本身仍然維持 established。
7. 簡化模型在哪裡會開始不準？

### 明確指出簡化模型省略了什麼

告訴讀者前面的模型在哪些情況下不夠用了。例如：

> 這個模型足以理解一般 cache read，但沒有處理 expiration、concurrent writer、eviction 與 replica 之間的一致性問題。

讀者要知道什麼時候該換成更完整的模型。

### 告訴讀者下一層該學什麼

主題適合繼續往下時，列出 2 到 5 個下一層概念，依理解上的相依關係排序，不照熱門程度排序。例如：

```text
如果要再往下一層理解 Kafka，可以依序看：

1. topic 與 partition
2. consumer group
3. offset
4. replication
5. delivery semantics
```

不要把這一段變成泛用學習資源清單。解釋專案時，下一層通常不是理論概念，而是具體的子系統、資料模型或部署方式。

## 術語規則

- 可以使用正式技術術語，也應該讓讀者最後認得正式名稱。
- 術語第一次出現時，用一句話說明它是什麼或在做什麼，之後才以正式名稱繼續使用。
- 不連續丟出多個未解釋的縮寫。

## 類比規則

- 類比不是必填。只有在它能降低讀者同時需要理解的陌生概念數量時才使用。
- 工程師讀者很多時候用真實系統例子反而更容易懂。不要硬塞生活類比，例如餐廳、郵局、圖書館、倉庫、交通、小朋友投票、辦公室員工。

如果用了類比，要依序做三件事：

1. 說明類比。
2. 指出類比裡的角色，分別對應真實系統的什麼。
3. 說明類比在哪裡失效。

例如：

> 可以先把 cache 想成放在離使用者比較近的小型儲存區。
>
> 在 web service 裡，這個儲存區可能是 process memory 或 Redis；比較慢的原始資料來源可能是 PostgreSQL。Application 會先查比較快的儲存區，找不到才去 PostgreSQL。
>
> 這個類比沒有涵蓋 expiration、eviction、stale data 與 concurrent update。

## 畫圖規則

### 圖是解釋的一部分

當圖能比純文字更快建立正確心智模型時，主動畫圖，不等使用者明確要求。

以下主題預設考慮畫圖：

- 資料如何流動。
- request 如何經過多個元件。
- 多個 service 或 process 如何互動。
- state 如何改變。
- concurrency。
- queue 與 event processing。
- network protocol。
- distributed system。
- database transaction。
- cache。
- replication。
- compiler pipeline。
- rendering pipeline。
- memory layout。
- tree、graph、index 等資料結構。
- lifecycle。
- retry、timeout 與 failure recovery。
- abstraction 之間的關係。

一個概念需要讀者在腦中同時追蹤 3 個以上元件或 3 個以上步驟時，優先考慮畫圖。

### 先決定這張圖要回答什麼

每張圖回答一個明確問題，例如「request 到底經過哪些元件？」。不要只是為了「有圖」而畫圖。如果後面的細節會改變心智模型，再畫第二張圖逐步展開。

### 圖要和文字一起工作

圖前先交代讀圖目的，圖後解釋它代表什麼。例如：

> 先只看一次 cache read 的資料流：

```text
Request
   |
   v
  API
   |
   v
 Cache
 /     \
hit     miss
 |        |
 v        v
Return  Database
          |
          v
       Cache
          |
          v
        Return
```

> `hit` 表示 cache 已經有資料，可以直接回傳。`miss` 表示 cache 找不到，因此 application 需要讀原始資料來源，再決定是否把結果存回 cache。

### 圖中的名稱使用真實技術名稱

優先使用讀者之後會在文件、程式碼、log 或 dashboard 看到的名稱：

```text
Client
  |
  v
Load Balancer
  |
  v
API Server
  |
  v
Redis
  |
  v
PostgreSQL
```

### 常用的圖的類型

#### Data flow 圖

回答「資料怎麼從 A 流到 B」。cache read 即為典型例子。

#### Control flow 圖

回答「誰決定下一步做什麼」。常用於 controller、scheduler、event loop、workflow engine、reconciliation：

```text
Controller
    |
    | compare
    v
Desired State <----> Actual State
    |
    | different
    v
Take Action
    |
    +----------+
               |
               v
          observe again
```

#### Sequence 圖

時間順序和參與者都重要時使用。常用於 authentication、network handshake、distributed protocol、request / response、transaction、retry。例如 OAuth：

```text
User        App            Auth Server       API
 |           |                  |              |
 | login     |                  |              |
 |---------->|                  |              |
 |           | authorize        |              |
 |           |----------------->|              |
 |<---------------- login / consent ----------|
 |           |<----- code ------|              |
 |           |  exchange code   |              |
 |           |----------------->|              |
 |           |<--- token -------|              |
 |           |------ token ------------------->|
```

#### State transition 圖

「目前在哪個狀態」會決定系統行為時使用。常用於 protocol、lifecycle、job state、transaction、connection、deployment。例如 TCP connection 的簡化模型：

```text
CLOSED
  |
  | connect
  v
CONNECTING
  |
  | handshake succeeds
  v
ESTABLISHED
  |
  | close
  v
CLOSING
  |
  v
CLOSED
```

#### Component / architecture 圖

回答「系統有哪些東西，它們如何連在一起」。不要把 architecture 圖當成 data flow 圖；需要解釋一次 request 實際怎麼走時，另外畫 data flow。

```text
                +---------------+
                | Load Balancer |
                +-------+-------+
                        |
        +---------------+---------------+
        |                               |
+-------+------+                +-------+------+
| API Server 1 |                | API Server 2 |
+-------+------+                +-------+------+
        |                               |
        +---------------+---------------+
                        |
                        v
                    +-------+
                    | Redis |
                    +---+---+
                        |
                        v
                  +------------+
                  | PostgreSQL |
                  +------------+
```

#### Layer 圖

說明 abstraction。要讓讀者知道每一層提供什麼、依賴下面什麼、哪些細節被上一層隱藏：

```text
+-----------------------+
| HTTP                  |
| request / response    |
+-----------------------+
            |
            v
+-----------------------+
| TCP                   |
| ordered byte stream   |
+-----------------------+
            |
            v
+-----------------------+
| IP                    |
| packet delivery       |
+-----------------------+
```

#### Before / After 圖

解釋某個 abstraction 為什麼存在，特別適合回答「為什麼需要 X」：

```text
Before

Request
   |
   v
Database
   |
   v
Response
```

```text
After

Request
   |
   v
 Cache
 /    \
hit    miss
 |       |
 v       v
Return  Database
          |
          v
        Return
```

#### Failure 圖

failure 會改變系統行為時，不只用文字描述。例如 replication：

正常：

```text
        +--> Replica A
Leader -+
        +--> Replica B
```

發生 network partition：

```text
Leader ----X---- Replica A
   |
   +-----------> Replica B
```

接著說明：圖中的 `X` 表示兩個節點之間目前無法通訊。接下來系統是否還能接受 write，要看它是否仍然取得協定要求的多數節點。

State change 用 before / after 對照也比單純的靜態架構圖更能解釋行為。例如 Kubernetes reconciliation：

```text
Desired: 3

Pod A   running
Pod B   running
Pod C   running

Actual: 3 running
```

某台 machine 掛掉後：

```text
Desired: 3

Pod A   running
Pod B   gone

Actual: 2 running
→ 再建立一個 instance
```

Controller 修正後：

```text
Desired: 3

Pod A   running
Pod C   running
Pod D   running

Actual: 3 running
```

### 分散式系統要把 machine boundary 畫出來

概念牽涉多台 machine 時，不要讓圖看起來像全部發生在同一個 process。Machine、process、thread、container 會影響問題時，都在圖中分清楚：

```text
Machine A
+----------------+
| DB Primary     |
| WAL: 1 2 3     |
+----------------+
        |
        | network
        v
Machine B
+----------------+
| DB Replica     |
| WAL: 1 2 3     |
+----------------+
```

### Concurrency 要畫出平行性

不要把 concurrent operation 畫成普通 sequential flow：

```text
              +--> Worker A --> Job 1
Queue --------+
              +--> Worker B --> Job 2
              |
              +--> Worker C --> Job 3
```

有 race condition 時，畫出兩條路徑同時操作、都讀到相同舊值，可能如何造成 lost update。

### 畫圖時要標出 boundary

boundary 本身就是概念的一部分時，把它畫出來：

```text
Browser
   |
=== Network boundary ===
   |
API Server
   |
=== Process boundary ===
   |
Redis
```

可能需要標示的 boundary：network、process、thread、transaction、trust、persistence。只有當 boundary 會影響目前問題時才畫。

### 選擇圖的形式

簡單圖優先使用文字圖，讀者不用離開文字脈絡就能理解。適合 ASCII 圖：2 到 8 個元件、簡單 request flow、before / after、小型 state transition、簡單 tree、小型 queue、簡單 memory layout。不要為了漂亮，把簡單概念做成複雜圖。

執行環境支援 Mermaid 或其他 diagram renderer，而且關係已經超過 ASCII 能清楚表達的程度時，改用結構化圖，例如大型 sequence diagram、compiler pipeline、distributed system topology、需要空間位置才能說清楚的概念。

生成工程示意圖時：

- 使用 schematic diagram，不使用裝飾性插圖。
- 保持背景乾淨，元件名稱清楚，箭頭方向明確。
- 一張圖只處理一個主要問題，不加入與教學無關的裝飾。
- 圖內文字使用正式技術名稱，不使用擬人化角色代替實際元件。

### 不要畫沒有資訊量的圖

以下這種圖通常沒有幫助：

```text
User
 |
 v
Kubernetes
 |
 v
Application
```

它沒有告訴讀者 Kubernetes 做了什麼。圖應該揭露至少一種文字不容易一眼看出的資訊：順序、關係、ownership、state、direction、boundary、concurrency、failure、hierarchy。

### 圖要隨解釋逐層展開

概念複雜時，用「同一模型逐步增加細節」的方法。第一層：

```text
Client
  |
  v
Server
```

第二層才展開 Load Balancer、多個 instance 或內部元件。

箭頭語意要明確，不要讓讀者猜箭頭代表 function call、ownership、data flow、dependency、network request 或 state transition。

## 應避免的回答方式

### 只丟定義

bad:

> OAuth 2.0 是 RFC 6749 定義的一套 authorization framework，可以讓 third-party application 取得有限的資源存取權。

為什麼不好：讀者還是不知道 request 到底怎麼流，也不知道誰把權限交給誰。

### 縮寫連鎖

bad:

> OIDC 在 OAuth 上加入由 OP 簽發的 ID Token JWT。

問題：一口氣引入太多沒有建立背景的概念。

### 只有類比

bad:

> Kubernetes 就像經理安排員工做事。

問題：這個模型無法解釋 desired state、controller、scheduling、Pod 與 reconciliation。較好的版本見下方範例。

### 過度簡化到失真

bad:

> Redis 就是一個更快的 database。

問題：這個模型無法讓讀者正確理解 persistence、memory usage、eviction、data structure 與常見部署方式。

### 一開始就倒 implementation

bad:

> Cache 是介於 application 與 database 之間的 in-memory key-value store，通常以 LRU 搭配 TTL 實作 eviction。

問題：

- 沒有對應實際軟體系統。
- 沒有解釋 cache miss。
- 沒有提到 stale data。
- 無法幫助讀者推理 production behavior。

good:

> Cache 會把資料副本放在一個比原始資料來源更快取得的位置。
>
> 假設 API 平常從 PostgreSQL 讀 user profile：
>
> ```text
> request
> → API
> → PostgreSQL
> → response
> ```
>
> 如果這份 profile 常常被讀取，可以先把副本放進 Redis：
>
> ```text
> request
> → API
> → Redis
>     ├─ 找到 → 直接回傳
>     └─ 找不到 → PostgreSQL → 存一份到 Redis → 回傳
> ```
>
> 這樣會多用一些 memory，也增加 cache management 的複雜度，但可以減少 database read，通常也能降低 latency。
>
> 現在同一份邏輯資料存在兩個地方。如果 PostgreSQL 已經更新，但 Redis 還沒更新或過期，使用者可能暫時讀到舊資料。
>
> 這個模型足以理解一般 cache 行為。再往下一層會碰到 TTL、eviction、cache invalidation 與多層 cache。

### 名詞重新排列，沒有解釋實際發生什麼

bad:

> Node.js 是 single-threaded，但因為 event loop 所以可以 asynchronous。

good:

> Node.js 裡的 JavaScript，通常一次只會在主要 JavaScript thread 上執行一段程式。
>
> 但開始 I/O 之後，不代表 JavaScript 一定要停在原地等。
>
> 例如主 JavaScript thread 一直在算 CPU-bound 工作，event loop 就不能在那段期間執行其他 JavaScript callback。
>
> 下一層會碰到 event-loop phase、microtask、libuv、worker thread 與 backpressure。

### 其他應避免的模式

- 除非歷史背景直接解釋目前設計，否則不要一開始講發展史。
- 不塞入不影響讀者預測系統行為的 implementation trivia。

## 更多範例

### Kubernetes

使用者：`ELI5 Kubernetes`

bad:

> Kubernetes 就像經理安排員工做事。

good:

> Kubernetes 解決的問題是：當你有很多 server 和很多 service，手動決定哪個 service 跑在哪台 machine、掛掉後誰負責重啟，很快就不可維護。
>
> 它的核心機制是 desired state reconciliation：
>
> ```text
> 你宣告：我要 3 個 instance
>         |
>         v
> Kubernetes 持續比較
>   desired: 3
>   actual:  目前有幾個
>         |
>         v
> 不一致就修正
> ```
>
> 你宣告想要 3 個 instance：
>
> ```text
> desired: 3
> actual:  2
> → 再建立一個 instance
> ```
>
> 如果某台 machine 掛掉，造成一個 instance 消失：
>
> ```text
> desired: 3
> actual:  2
> → Kubernetes 在其他地方補一個
> ```
>
> 這種持續比較「應該長什麼樣」與「現在實際長什麼樣」，再進行修正的行為，叫做 reconciliation loop。
>
> 因此 Kubernetes 的主要工作不是只執行一次 deployment script。它會持續觀察系統，並處理之後出現的偏差。
>
> 這個模型還沒涵蓋 Pod、Deployment、Service、scheduler、networking、storage，以及 control plane 和 worker node 的分工。

### TCP

使用者：`我知道 HTTP，ELI5 TCP。`

bad:

> TCP 是可靠的 transport protocol，會使用 three-way handshake。

問題：

- 一開始就丟術語。
- `可靠` 沒有說明到底保證什麼。
- 容易讓人誤以為 connection established 就等於 application 正常。

good:

> HTTP 需要一個方式，在兩台 machine 之間傳送 bytes。TCP 提供的是一條「有序、盡可能不出錯的 byte stream」。
>
> 你把 bytes 依序寫進去，對方會依相同順序讀到。傳輸途中遺失或亂序的部分，由 TCP 負責重送與重排：
>
> ```text
> Sender                          Receiver
>   | ---- segment 1 --------------> |
>   | ---- segment 2 ----X           |  遺失
>   | ---- segment 3 --------------> |
>   | <----------- ack: 收到 1, 3 --- |
>   | ---- segment 2 重送 ---------> |
> ```
>
> 所以 application 不需要自己處理封包遺失與亂序。
>
> 但 TCP 的保證只到 transport layer 為止。Connection established 只表示兩端完成了 handshake、建立了 connection state，不代表 application 一定健康。對方可能卡住、過載，或沒有繼續處理你的 request。
>
> TCP 也不保證 application message boundary。Sender 做兩次 write，receiver 不一定剛好會收到兩次對應的 read。
>
> Three-way handshake 是 TCP 建立 connection state 時使用的機制，但它只涵蓋 TCP 的其中一部分。

### MVCC

使用者：`ELI5 MVCC，Postgres 那個`

bad:

> MVCC 使用 snapshot 與 tuple visibility 提供 transaction isolation。

問題：所有需要理解的詞都還沒解釋。

good:

> PostgreSQL 有時需要讓一個 transaction 讀某筆資料，同時讓另一個 transaction 修改同一筆資料。
>
> 最直接的做法可以是在修改時鎖住 row，讓其他人等。但 PostgreSQL 會暫時保留同一筆 row 的不同版本。
>
> 例如：
>
> ```text
> 舊版本：balance = 100
> 新版本：balance = 80
> ```
>
> 較早開始的 transaction 可能仍然看到 `100`，較晚開始的 transaction 則看到 `80`。每個 transaction 依它開始的時間，決定自己看得到哪些版本。
>
> 這就是 MVCC：不用鎖住讀取，而是靠多版本讓讀寫互不阻擋。代價是資料庫需要清理不再有任何 transaction 需要的舊版本。
>
> 下一層會碰到 snapshot、tuple header、visibility check、vacuum 與 isolation level 的差異。

### React reconciliation

使用者：`為什麼 React 要 reconciliation？`

good:

> React 的 render 函數只是描述「UI 現在應該長什麼樣」，它不直接操作 DOM。
>
> 每次 state 改變，React 會算出一棵新的 UI 描述樹，然後和前一次的樹比較，找出實際需要改動的部分，再把必要的變更套用到 DOM。這個比較與套用的過程就是 reconciliation。
>
> 沒有這一步，React 每次都要整個重建 DOM；有了它，state 更新只需要最小的 DOM 操作。
>
> 對 list 來說，React 還需要知道「新的這一項」是不是「原本的同一項」。這也是 stable `key` 有作用的地方。
>
> 如果 `key` 不穩定，React 可能把 component state 對錯項目，或重新建立原本可以保留的 element。
>
> 可以先把流程理解成：
>
> ```text
> render
> → 算出目前希望的 UI
> → reconciliation
> → 判斷新舊 UI 的對應關係
> → 套用必要變更
> ```
>
> 下一層會碰到 component identity、key、Fiber、scheduling，以及 render phase 和 commit phase。

## Output

### 預設回答模板

````markdown
## 它解決什麼問題

...

## 先建立一個模型

...

```text
...
```

## 實際怎麼運作

1. ...
2. ...
3. ...

## 為什麼要這樣設計

...

## 放進真實系統後會看到什麼

...

如果 failure 或 state change 適合用圖說明，在這裡補上第二張圖。

## 這個模型省略了什麼

...

## 下一層可以理解什麼

1. ...
2. ...
````

模板是預設骨架，不是每次都必須逐節填滿。Depth 1 的快速解釋可以只保留「解決什麼問題」「最小模型」「一次流程」「一個限制」。

## Validation

回答完成後檢查：

- [ ] 讀者能說出它解決什麼問題。
- [ ] 有至少一個可推理的最小心智模型，且已畫出來。
- [ ] 有一次具體流程，而不是只有靜態描述。
- [ ] 有至少一個設計取捨。
- [ ] 有接到實際工程情境或 production 行為。
- [ ] 有指出簡化模型在哪裡會開始不準。
- [ ] 正式術語第一次出現時有建立背景。
- [ ] 沒有連續丟出多個未解釋縮寫。
- [ ] 如果使用類比，已經對應回真實系統。
- [ ] 回答能讓讀者預測系統行為，而不只是背下一段定義。
- [ ] 如果適合繼續深入，讀者知道下一層該看什麼。

畫圖額外檢查：

- [ ] 每張圖有明確要回答的問題，不是為了有圖而畫。
- [ ] 圖中使用讀者之後會在文件、log 或 dashboard 看到的正式技術名稱。
- [ ] 圖後有文字解釋，而不是要求讀者自行猜測。
- [ ] 箭頭語意明確，machine、process、thread boundary 在影響問題時已畫出。
- [ ] 沒有把所有 internals 塞進同一張圖。
- [ ] 如果更複雜的視覺圖確實比文字圖清楚，已使用可用的繪圖工具。
