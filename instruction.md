# SQL Query Optimizer Advisor

## Task Description

You are a database performance expert. Your task is to analyze slow SQL queries and provide optimization recommendations. The repository contains several SQL queries that are experiencing performance issues in production.

You need to:
1. Analyze each slow query in the `queries/` directory
2. Identify performance bottlenecks (missing indexes, inefficient joins, full table scans, etc.)
3. Provide specific optimization recommendations
4. Generate an optimization report in JSON format

**Implementation:** Create an analysis script named `analyze.py`, `analyze.sh`, `optimizer.py`, or `solve.sh` that reads the queries and generates the report. The test suite will execute your script to verify it works correctly.

## Input

The `queries/` directory contains:
- `schema.sql` - Database schema definition
- `slow_queries.sql` - Queries that need optimization (numbered Q1, Q2, Q3, etc.)
- `sample_data.sql` - Sample data for testing (optional)

## Output

Create a file called `optimization_report.json` in the working directory with the following structure:

```json
{
  "queries": [
    {
      "query_id": "Q1",
      "issues": [
        {
          "type": "missing_index",
          "description": "Query performs full table scan on sensors table",
          "severity": "high",
          "recommendation": "Create index on sensors(location_zone) column"
        },
        {
          "type": "inefficient_join",
          "description": "Using SELECT * fetches unnecessary columns",
          "severity": "medium",
          "recommendation": "Select only required columns instead of SELECT *"
        }
      ],
      "optimized_query": "SELECT s.sensor_id, s.device_type FROM sensors s WHERE s.location_zone = ?",
      "expected_improvement": "10x faster with index"
    }
  ],
  "summary": {
    "total_queries": 3,
    "high_priority_issues": 2,
    "medium_priority_issues": 1,
    "low_priority_issues": 0
  }
}
```

## Issue Types to Detect

1. **missing_index** - Queries that would benefit from an index
   - WHERE clauses on non-indexed columns
   - JOIN conditions on non-indexed columns
   - ORDER BY on non-indexed columns

2. **inefficient_join** - Suboptimal join patterns
   - Using SELECT * with JOINs
   - Missing join conditions (cartesian products)
   - Unnecessary joins

3. **full_table_scan** - Queries scanning entire tables
   - No WHERE clause on large tables
   - Functions on indexed columns (e.g., WHERE YEAR(date) = 2023)

4. **n_plus_one** - N+1 query pattern indicators
   - Queries in loops (detectable by similar query patterns)

5. **subquery_inefficiency** - Inefficient subqueries
   - Correlated subqueries that could be JOINs
   - IN with subquery vs EXISTS

## Severity Levels

- **high**: Will cause significant performance issues in production (full table scans on large tables, missing critical indexes)
- **medium**: Noticeable performance impact (inefficient joins, unnecessary columns)
- **low**: Minor optimizations (query formatting, minor rewrites)

## Guidelines

- Be specific in your recommendations
- Provide actual SQL for suggested indexes
- Include optimized query versions when applicable
- Estimate improvement when possible
- Focus on practical, implementable suggestions

## Testing

Your solution will be validated by:
1. Checking that `optimization_report.json` exists and is valid JSON
2. Verifying all queries from `slow_queries.sql` are analyzed
3. Confirming recommendations are syntactically valid SQL (for indexes)
4. Ensuring severity levels are appropriate
5. Checking that optimized queries are valid SQL

## Success Criteria

- All queries in `slow_queries.sql` must be analyzed
- Each query must have at least one identified issue
- Recommendations must be actionable and specific
- JSON output must match the specified schema
- At least 80% of high-severity issues must be correctly identified
