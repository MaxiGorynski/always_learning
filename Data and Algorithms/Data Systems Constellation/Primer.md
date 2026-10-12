# Data Systems Primer

Bitesized definitions for the 80 concepts in `Constellation.html`, grouped by region.

## Storage engines
- **B-Tree**: Balanced tree of fixed-size pages, updated in place. Default index structure; read-optimised.
- **LSM Tree**: Buffer writes in memory, flush sorted immutable files, merge in background. Write-optimised.
- **Write-Ahead Logging (WAL)**: Append a change to a log before touching data files; replay it after a crash.
- **Bloom Filter**: Compact probabilistic set: "definitely not here" or "maybe here". Skips pointless disk reads.
- **Compaction**: Merge storage files, discarding overwritten or deleted entries.
- **Database Vacuuming**: Reclaim space from dead row versions; in Postgres also prevents transaction-ID wraparound.
- **Write Amplification**: One logical write becomes many physical writes (page rewrites, WAL, compaction).
- **Checkpointing**: Periodically flush dirty pages so recovery replays less log.
- **Columnar Storage**: Store each column contiguously; fast scans and strong compression for analytics.
- **Secondary Index**: An index on a non-primary-key column.
- **Index-Only Scan**: Answer a query from the index alone, never visiting the table.
- **Backups vs. PITR**: A backup is one moment frozen; point-in-time recovery restores a base backup then replays WAL to any instant.

## Transactions & isolation
- **ACID**: Atomicity, Consistency, Isolation, Durability.
- **MVCC**: Keep multiple row versions so readers see a snapshot and never block writers.
- **Snapshot Isolation**: Each transaction reads from a consistent snapshot taken at its start.
- **Serializability**: Strongest isolation: the outcome equals some serial order.
- **Dirty Read**: Reading another transaction's uncommitted writes.
- **Read Skew**: Seeing parts of the database at different moments, so totals don't add up.
- **Write Skew**: Two transactions read the same data, write different rows, and jointly break an invariant.
- **Phantom Read**: Re-running a range query returns rows another transaction just inserted.
- **Optimistic Locking**: No locks; check a version on write, retry on conflict.
- **Pessimistic Locking**: Lock first, then act; others wait.
- **Deadlock**: Transactions wait on each other's locks in a cycle; the database kills one.
- **Lock Escalation**: The database swaps many row locks for one table lock to save memory.

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
