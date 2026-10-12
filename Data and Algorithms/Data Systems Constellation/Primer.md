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
