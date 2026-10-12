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
