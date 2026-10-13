# Data Systems Primer

Bitesized definitions for the 80 concepts in `Constellation.html`, grouped by region.

## Storage engines
- **B-Tree**: The data structure behind almost every database index. Without an index, finding one row means scanning the whole table. A B-tree keeps keys sorted in a shallow, wide tree of disk pages, so the database can find any key, or any range of keys, by reading just three or four pages, even across billions of rows. It’s the default index in Postgres, MySQL and most relational databases.
- **LSM Tree**: A storage design built for heavy write traffic. Instead of finding each record on disk and updating it in place (slow, random I/O), an LSM tree collects writes in memory and periodically writes them out as sorted files that are never modified again. Writes become fast sequential appends; the trade-off is that a read may have to check several files. It powers Cassandra, RocksDB and other write-heavy stores.
- **Write-Ahead Logging (WAL)**: How databases avoid losing data when they crash. Before changing the actual data files, the database first appends a record of the change to a log on disk. If the power cuts out halfway through an update, the database replays the log on restart and finishes or undoes the work. This is what makes ‘committed’ mean durable, and the same log is reused for replication and backups.
- **Bloom Filter**: A tiny, memory-cheap structure that answers one question: ‘could this item be in the set?’ It replies either ‘definitely not’ or ‘probably yes’, and is only ever wrong in the ‘yes’ direction. Databases use it to avoid expensive disk reads for keys that don’t exist: if the filter says no, the file is skipped entirely.
- **Compaction**: Background housekeeping for LSM-tree databases. Because those databases never overwrite data in place, every update or delete leaves the old version behind in an older file. Compaction periodically merges files, keeps only the newest version of each key, and throws away deleted data. Without it, disk usage would grow forever and reads would slow down as they search more and more files.
- **Database Vacuuming**: Garbage collection for databases like Postgres. When you update or delete a row, Postgres doesn’t erase the old version straight away, because transactions already in progress might still need to see it. Vacuuming later removes those dead versions and frees their space for reuse. If it falls behind, tables bloat, queries slow down, and in extreme cases the database stops accepting writes to protect itself.
- **Write Amplification**: The gap between how much data your application asks to write and how much the database actually writes to disk. Change a 100-byte row and the database may rewrite the whole 8 KB page that holds it, record the change again in the write-ahead log, and rewrite it once more during background maintenance. That multiplier, often 10× to 100×, eats disk bandwidth and wears out SSDs, and it is one of the main trade-offs between storage engines.
- **Checkpointing**: A periodic save point for a database. Changes are first recorded in the write-ahead log and held in memory, and only written to the main data files later. A checkpoint forces all of those pending changes out to the data files and marks the spot in the log. After a crash, the database only replays the log from the last checkpoint rather than from the beginning, so recovery is fast.
- **Columnar Storage**: Storing a table column by column instead of row by row. Analytics queries such as ‘average order value last year’ read one or two columns across millions of rows. A columnar store reads only those columns and skips the rest, and because a column holds similar values it compresses extremely well. That’s why data warehouses are columnar, while apps that fetch whole records use row stores.
- **Secondary Index**: An extra index on a column other than the primary key, so you can find rows by something besides their ID. A users table is organised by user_id, but logins search by email; an index on email turns that into a fast lookup instead of a full table scan. The cost is that every insert or update must also update each index, so more indexes mean slower writes and more storage.
- **Index-Only Scan**: A query the database can answer entirely from an index, without visiting the table at all. Normally an index tells the database where a row lives, and it then fetches the row from the table. If the index already contains every column the query needs (a ‘covering’ index), that second trip is skipped, which can make the query several times faster.
- **Backups vs. PITR**: Two different ways to get data back. A backup is a full copy taken at one moment, so restoring it loses everything written since. Point-in-time recovery (PITR) combines a backup with the continuous log of every change made after it, so you can restore to any exact second, such as one second before someone ran DELETE without a WHERE clause.

## Transactions & isolation
- **ACID**: The four guarantees a database transaction gives you. Atomicity: all of its changes happen, or none do. Consistency: rules like ‘a balance can’t go negative’ hold before and after. Isolation: concurrent transactions don’t trip over each other’s half-finished work. Durability: once committed, data survives crashes. Together they let you write correct code without reasoning about every possible failure.
- **MVCC**: The technique most databases use so that reads and writes don’t block each other. Instead of overwriting a row, the database keeps the old version and adds a new one. Each transaction sees the versions that were committed when it started, so a long-running report reads a stable picture while other users keep writing. The cost is cleaning up old versions later.
- **Snapshot Isolation**: An isolation level where every transaction works from a frozen picture of the database as it was when the transaction began. You never see others’ half-finished changes, and reading the same data twice always gives the same answer. Many databases default to it because it’s fast and intuitive, but it still allows one subtle bug: write skew.
- **Serializability**: The strongest isolation level. The database guarantees the result is the same as if transactions had run one at a time, in some order, with no overlap. Every concurrency anomaly disappears, so you can reason about each transaction as if it were alone. The price is lower throughput, and transactions that sometimes get aborted and must be retried.
- **Dirty Read**: Reading data that another transaction has written but not yet committed. If that transaction then rolls back, you’ve made a decision based on data that never officially existed. It’s the weakest possible guarantee, and almost every database prevents it by default, so you’ll mostly meet it as the first rung on the ladder of isolation levels.
- **Read Skew**: When a transaction reads related pieces of data at slightly different moments and sees a combination that never actually existed. Each value it read was real and committed, but another transaction changed things between the reads. The classic case is checking two bank accounts during a transfer and seeing money missing or duplicated. Snapshot isolation prevents it.
- **Write Skew**: A sneaky concurrency bug. Two transactions read the same data, each makes a decision based on it, and each writes to a different row. Neither overwrites the other, so the database sees no conflict, yet together they break a rule that each on its own would have kept. It slips past snapshot isolation and needs serializable isolation or explicit locks.
- **Phantom Read**: When a transaction runs the same search twice and the second time new rows appear, or rows vanish, because another transaction inserted or deleted matching rows in between. Locking existing rows can’t prevent it, because the new rows didn’t exist yet to be locked. It matters for checks like ‘is this time slot free?’ just before booking it.
- **Optimistic Locking**: A strategy for concurrent updates that assumes conflicts are rare. Instead of locking a record while you work on it, you note its version number, and when you save you tell the database ‘only update if the version hasn’t changed’. If someone else changed it first, your update fails and you retry. There’s no waiting and no deadlock, but many retries if conflicts become common.
- **Pessimistic Locking**: A strategy for concurrent updates that assumes conflicts are likely. You lock the record before reading or changing it, and anyone else who wants it waits until you finish. Nobody can change the data underneath you, which suits contested resources like seats or stock, but waiting transactions reduce throughput and can deadlock.
- **Deadlock**: When two or more transactions are each waiting for a lock the other holds, so none of them can ever proceed. A holds row 1 and wants row 2; B holds row 2 and wants row 1. Databases detect the cycle and kill one transaction so the other can finish, so your application must be ready to retry the one that was killed.
- **Lock Escalation**: When a database decides it is tracking too many small locks and replaces them with one big lock. Locking 10,000 individual rows uses a lot of memory, so the database (notably SQL Server) may lock the whole table instead. That saves memory but blocks everyone else who wanted any row in the table, causing surprise slowdowns and deadlocks.

## Consensus & coordination
- **Distributed Transactions**: One atomic transaction across several nodes or services.
- **Two-Phase Commit (2PC)**: Coordinator says prepare, then commit. Blocks if the coordinator dies mid-way.
- **Three-Phase Commit (3PC)**: Adds a pre-commit phase to avoid blocking; unsafe under network partitions.
- **Saga Pattern**: A chain of local transactions, each with a compensating undo.
- **Two Generals Problem**: Proof that agreement over an unreliable channel can never be certain.
- **Raft**: Consensus via an elected leader replicating a log to a majority.
- **Leader Election**: Nodes agree on exactly one coordinator.
- **Quorum**: Require W + R > N acknowledgements so reads overlap the latest write.
- **Split-Brain**: Two nodes both believe they're leader; data diverges.
- **Distributed Locking**: Mutual exclusion across machines; needs leases and fencing tokens.
- **Idempotency**: Doing it twice has the same effect as once. Makes retries safe.
- **Exactly-Once Semantics**: Each message takes effect once; really at-least-once delivery plus deduplication.

## Replication & consistency
- **CAP Theorem**: During a network partition, choose consistency or availability.
- **Strong Consistency**: Every read sees the latest committed write.
- **Eventual Consistency**: Replicas converge once writes stop; reads may be stale meanwhile.
- **Consistent Reads**: Reads with a stated guarantee: read-your-writes, monotonic, or from the leader.
- **Leader–Follower Replication**: One node takes writes; followers copy its log.
- **Multi-Leader Replication**: Several nodes accept writes; conflicts must be resolved.
- **Read Replicas**: Followers that serve read-only traffic.
- **Physical Replication**: Ships byte-level page changes; exact clone, same version.
- **Logical Replication**: Ships row-level changes; selective and cross-version.
- **Geo-Replication**: Copies across regions for latency and disaster recovery.
- **Read Repair**: Fix stale replicas during a read.
- **Change Data Capture (CDC)**: Stream row changes out of the database log to other systems.
- **Failover**: Promote a standby when the primary dies.
- **High Availability**: Redundancy plus automatic recovery, measured in "nines".

## Partitioning & scale
- **Horizontal Scaling**: More machines, not bigger ones.
- **Database Sharding**: Split data across databases by a shard key.
- **Hash Partitioning**: Assign keys by hash; even spread, no range scans.
- **Range Partitioning**: Assign contiguous key ranges; fast range scans, hotspot risk.
- **Consistent Hashing**: Keys and nodes on a ring; a membership change moves only ~1/n of keys.
- **Hot Partition**: One partition gets a disproportionate share of traffic.
- **Data Skew**: Uneven data distribution across keys or partitions.
- **Resharding**: Changing shard count or boundaries while live.
- **Rebalancing**: Moving partitions between nodes to even out load.
- **Federation**: Split databases by function (users DB, orders DB).
- **Data Locality**: Keep related data together, and compute near the data.

## Traffic & resilience
- **Load Balancing**: Spread requests across instances.
- **Caching**: Keep hot data in faster storage; invalidation is the hard part.
- **Rate Limiting**: Cap requests per client per time window.
- **Backpressure**: Downstream tells upstream to slow down.
- **Circuit Breaker**: Stop calling a failing dependency; fail fast, probe later.
- **Retry Storm**: Mass retries pile load onto an already struggling service.
- **Thundering Herd**: Many clients wake at once and stampede a resource.
- **Connection Pooling**: Reuse open DB connections instead of opening one per request.
- **Connection Multiplexing**: Many logical streams share one physical connection.
- **Connection Leaks**: Connections borrowed and never returned until the pool runs dry.

## Modeling & querying
- **Normalization**: Each fact stored once; no redundancy.
- **Denormalization**: Duplicate data to avoid joins; faster reads, harder writes.
- **Materialized Views**: Precomputed query results stored as a table.
- **Denormalized Read Models**: Query-shaped projections built from the write side (CQRS).
- **Event Sourcing**: State is an immutable log of events; current state is a replay.
- **Schema Evolution**: Changing schemas while old and new readers and writers keep working.
- **Data Warehouse**: Central store built for big analytical queries.
- **Query Planner**: Turns SQL into an execution plan.
- **Cost-Based Optimization**: Estimates each candidate plan's cost from statistics; picks the cheapest.
