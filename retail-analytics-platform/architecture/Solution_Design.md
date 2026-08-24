# Solution Design
Landing zone preserves source data. Curated zone stores standardized Parquet partitioned by event_date and channel/store region. Redshift Serverless supports BI concurrency; Athena supports ad hoc analysis. Lake Formation grants data-product access. QuickSight is the executive BI layer.
