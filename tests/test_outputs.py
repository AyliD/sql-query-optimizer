"""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""

import json
import os
import re


def test_agent_code_exists():
    """Test that agent created analysis code (not just hand-wrote JSON)."""
    # Check for evidence of code execution
    has_code = (
        os.path.exists('/app/analyze.py') or
        os.path.exists('/app/analyze.sh') or
        os.path.exists('/app/optimizer.py') or
        os.path.exists('/app/solve.sh')
    )
    assert has_code, \
        "Agent must create an analysis script. Hand-writing JSON without code is not acceptable."


def test_optimization_report_exists():
    """Test that the optimization report file exists."""
    assert os.path.exists('/app/optimization_report.json'), \
        "optimization_report.json must be created in the working directory"


def test_report_is_valid_json():
    """Test that the report is valid JSON."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    assert isinstance(report, dict), "Report must be a JSON object"


def test_report_structure():
    """Test that the report has the required structure."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    assert 'queries' in report, "Report must have 'queries' key"
    assert 'summary' in report, "Report must have 'summary' key"
    assert isinstance(report['queries'], list), "'queries' must be a list"
    assert isinstance(report['summary'], dict), "'summary' must be an object"


def test_all_queries_analyzed():
    """Test that all queries from slow_queries.sql are analyzed."""
    # Read the slow_queries.sql to count expected queries
    with open('/queries/slow_queries.sql', 'r') as f:
        content = f.read()
    
    # Count queries (look for -- Q patterns)
    expected_queries = re.findall(r'-- Q\d+:', content)
    expected_count = len(expected_queries)
    
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    actual_count = len(report['queries'])
    assert actual_count == expected_count, \
        f"Expected {expected_count} queries to be analyzed, but found {actual_count}"


def test_query_structure():
    """Test that each query has the required structure."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    for query in report['queries']:
        assert 'query_id' in query, "Each query must have 'query_id'"
        assert 'issues' in query, "Each query must have 'issues'"
        assert isinstance(query['issues'], list), "'issues' must be a list"
        assert len(query['issues']) > 0, "Each query must have at least one issue"
        
        # Check for optimized_query and expected_improvement fields
        assert 'optimized_query' in query, "Each query must have 'optimized_query' field"
        assert 'expected_improvement' in query, "Each query must have 'expected_improvement' field"
        assert isinstance(query['optimized_query'], str), "'optimized_query' must be a string"
        assert isinstance(query['expected_improvement'], str), "'expected_improvement' must be a string"
        assert len(query['optimized_query']) > 0, "'optimized_query' cannot be empty"
        
        for issue in query['issues']:
            assert 'type' in issue, "Each issue must have 'type'"
            assert 'description' in issue, "Each issue must have 'description'"
            assert 'severity' in issue, "Each issue must have 'severity'"
            assert 'recommendation' in issue, "Each issue must have 'recommendation'"
            
            assert issue['severity'] in ['high', 'medium', 'low'], \
                f"Severity must be high, medium, or low, got {issue['severity']}"
            
            assert issue['type'] in ['missing_index', 'inefficient_join', 'full_table_scan', 
                                      'n_plus_one', 'subquery_inefficiency'], \
                f"Invalid issue type: {issue['type']}"


def test_summary_structure():
    """Test that summary has required fields."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    summary = report['summary']
    assert 'total_queries' in summary, "Summary must have 'total_queries'"
    assert 'high_priority_issues' in summary, "Summary must have 'high_priority_issues'"
    assert 'medium_priority_issues' in summary, "Summary must have 'medium_priority_issues'"
    assert 'low_priority_issues' in summary, "Summary must have 'low_priority_issues'"
    
    # Verify counts match
    total_issues = summary['high_priority_issues'] + summary['medium_priority_issues'] + summary['low_priority_issues']
    actual_issues = sum(len(q['issues']) for q in report['queries'])
    assert total_issues == actual_issues, \
        f"Summary issue counts ({total_issues}) don't match actual issues ({actual_issues})"


def test_q1_analysis():
    """Test that Q1 is properly analyzed."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    q1 = next((q for q in report['queries'] if q['query_id'] == 'Q1'), None)
    assert q1 is not None, "Q1 must be analyzed"
    
    # Q1 should have relevant issues identified
    has_missing_index = any(
        issue['type'] == 'missing_index' and 'location_zone' in issue['recommendation'].lower()
        for issue in q1['issues']
    )
    assert has_missing_index, "Q1 should identify missing index on location_zone column"


def test_q2_analysis():
    """Test that Q2 is properly analyzed."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    q2 = next((q for q in report['queries'] if q['query_id'] == 'Q2'), None)
    assert q2 is not None, "Q2 must be analyzed"
    
    # Q2 should have issues identified
    has_issue = any(
        issue['type'] in ['inefficient_join', 'missing_index']
        for issue in q2['issues']
    )
    assert has_issue, "Q2 should identify issues with SELECT * or missing index on device_type"


def test_q3_analysis():
    """Test that Q3 is properly analyzed."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    q3 = next((q for q in report['queries'] if q['query_id'] == 'Q3'), None)
    assert q3 is not None, "Q3 must be analyzed"
    
    # Q3 should have relevant issues identified
    has_index_issue = any(
        issue['type'] == 'missing_index' and 'triggered_at' in issue['recommendation'].lower()
        for issue in q3['issues']
    )
    assert has_index_issue, "Q3 should identify missing index on triggered_at"


def test_q4_analysis():
    """Test that Q4 is properly analyzed."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    q4 = next((q for q in report['queries'] if q['query_id'] == 'Q4'), None)
    assert q4 is not None, "Q4 must be analyzed"
    
    # Q4 should have issues identified
    assert len(q4['issues']) > 0, "Q4 should have at least one issue"
    
    # Should identify either inefficient_join or missing_index
    has_issue = any(
        issue['type'] in ['inefficient_join', 'missing_index']
        for issue in q4['issues']
    )
    assert has_issue, "Q4 should identify issues with JOINs or missing indexes"


def test_q5_analysis():
    """Test that Q5 is properly analyzed."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    q5 = next((q for q in report['queries'] if q['query_id'] == 'Q5'), None)
    assert q5 is not None, "Q5 must be analyzed"
    
    # Q5 should have issues identified
    assert len(q5['issues']) > 0, "Q5 should have at least one issue"
    
    # Should identify full_table_scan or missing_index issue
    has_issue = any(
        issue['type'] in ['full_table_scan', 'missing_index']
        for issue in q5['issues']
    )
    assert has_issue, "Q5 should identify issues with function on column or LIKE pattern"


def test_q6_analysis():
    """Test that Q6 is properly analyzed."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    q6 = next((q for q in report['queries'] if q['query_id'] == 'Q6'), None)
    assert q6 is not None, "Q6 must be analyzed"
    
    # Q6 should have issues identified
    assert len(q6['issues']) > 0, "Q6 should have at least one issue"
    
    # Q6 should identify either missing_index or inefficient_join issues
    # (related to ORDER BY and user_id filtering)
    has_relevant_issue = any(
        issue['type'] in ['missing_index', 'inefficient_join', 'full_table_scan']
        for issue in q6['issues']
    )
    assert has_relevant_issue, "Q6 should identify index or join related issues"


def test_recommendations_are_specific():
    """Test that recommendations contain actionable SQL."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    for query in report['queries']:
        for issue in query['issues']:
            if issue['type'] == 'missing_index':
                # Recommendation should mention CREATE INDEX or index
                rec = issue['recommendation'].lower()
                assert 'index' in rec, \
                    f"Missing index recommendation should mention 'index': {issue['recommendation']}"


def test_high_severity_issues():
    """Test that high-severity issues are properly identified."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    # At least Q1 (sensor lookup) and Q3 (date range) should be high severity
    high_issues = [
        issue 
        for query in report['queries'] 
        for issue in query['issues'] 
        if issue['severity'] == 'high'
    ]
    
    assert len(high_issues) >= 2, \
        f"Expected at least 2 high-severity issues, found {len(high_issues)}"


def test_optimized_queries_valid():
    """Test that optimized queries are valid SQL strings."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    for query in report['queries']:
        opt_query = query['optimized_query']
        # Basic validation - should be a non-empty string with SQL keywords
        assert len(opt_query) > 10, f"Optimized query too short for {query['query_id']}"
        assert 'SELECT' in opt_query.upper(), f"Optimized query should contain SELECT for {query['query_id']}"
        
        # Check for balanced parentheses (basic SQL syntax check)
        assert opt_query.count('(') == opt_query.count(')'), \
            f"Unbalanced parentheses in optimized query for {query['query_id']}"
        
        # Should not contain obvious syntax errors
        assert ';;' not in opt_query, \
            f"Double semicolon in optimized query for {query['query_id']}"


def test_index_recommendations_valid():
    """Test that CREATE INDEX recommendations are syntactically valid."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    for query in report['queries']:
        for issue in query['issues']:
            if issue['type'] == 'missing_index':
                rec = issue['recommendation']
                # If recommendation contains CREATE INDEX, validate basic syntax
                if 'CREATE INDEX' in rec.upper():
                    assert 'ON' in rec.upper(), \
                        f"CREATE INDEX should specify ON clause: {rec}"
                    # Should have table and column references
                    assert '(' in rec and ')' in rec, \
                        f"CREATE INDEX should have column list: {rec}"


def test_expected_improvement_present():
    """Test that expected_improvement field is meaningful."""
    with open('/app/optimization_report.json', 'r') as f:
        report = json.load(f)
    
    for query in report['queries']:
        improvement = query['expected_improvement']
        assert len(improvement) > 0, f"expected_improvement cannot be empty for {query['query_id']}"
        assert len(improvement) < 500, f"expected_improvement too long for {query['query_id']}"
