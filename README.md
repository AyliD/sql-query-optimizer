# SQL Query Optimizer Advisor

A T-Bench task for analyzing slow SQL queries and providing optimization recommendations.

## Task Description

This task tests an AI agent's ability to:
- Analyze SQL queries for performance issues
- Identify missing indexes, inefficient JOINs, and full table scans
- Generate specific optimization recommendations
- Create structured JSON reports

## Taxonomy

- **Use Case:** Perf Optimization
- **Domain:** data_science  
- **Languages:** SQL, Python
- **Difficulty:** Medium

## Problem Statement

Given 6 slow SQL queries from an IoT sensor monitoring database, the agent must analyze each query and generate an optimization report identifying:

1. **Missing indexes** - Columns used in WHERE, JOIN, or ORDER BY without indexes
2. **Inefficient JOINs** - SELECT * with JOINs, cartesian products
3. **Full table scans** - Functions on indexed columns, leading wildcards in LIKE
4. **Query structure issues** - Suboptimal patterns that hurt performance

## Input Files

The task provides:
- `queries/schema.sql` - Database schema (IoT: sensors, readings, alerts, maintenance logs)
- `queries/slow_queries.sql` - 6 slow queries labeled Q1-Q6
- `queries/sample_data.sql` - Sample data for testing

## Expected Output

Agent must create `optimization_report.json` with:
```json
{
  "queries": [
    {
      "query_id": "Q1",
      "issues": [...],
      "optimized_query": "SELECT ...",
      "expected_improvement": "..."
    }
  ],
  "summary": {...}
}
```

## Queries to Analyze

1. **Q1:** Sensor lookup by location_zone (missing index on sensors.location_zone)
2. **Q2:** Temperature readings by device type with SELECT * and JOIN
3. **Q3:** Alerts in date range (missing index on alert_history.triggered_at)
4. **Q4:** Sensor readings with alert history and maintenance logs (3 JOINs with SELECT *)
5. **Q5:** Sensor search with LOWER() function (prevents index usage)
6. **Q6:** Sensor readings with ORDER BY (missing composite index)

## Validation

Tests verify:
- All 6 queries are analyzed
- Each query has identified issues with proper severity (high/medium/low)
- Recommendations include specific SQL (e.g., CREATE INDEX statements)
- optimized_query and expected_improvement fields are present
- High-severity issues are correctly identified (location_zone lookup, date ranges)

## Running the Task

```bash
# Agent should create an analysis script (analyze.py, analyze.sh, etc.)
# Or implement solution in solve.sh

# The test runner will execute the agent's code and validate output
```

## Reference Solution

A Python-based analyzer is provided in `solution/solve.sh` that demonstrates:
- Parsing SQL files to extract queries
- Pattern matching to identify performance issues
- Generating structured JSON reports

## Coverage Gap Rationale

This task fills important taxonomy gaps:
- **data_science domain** - Underrepresented vs web_frontend
- **SQL language** - Critical for backend/data engineering
- **Perf Optimization** - Practical real-world skill for production systems
- **Database expertise** - Essential for full-stack developers

Unlike algorithm puzzles, this mirrors real production debugging work that engineers do daily.
