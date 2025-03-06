##########################################################################
#         IO_ANALYZER.PY
###########################################################################
# """
# IO Analyzer for ETL Test Generation
# ==================================
#
# A. APPLICATION OVERVIEW
# ----------------------
# The IO Analyzer is a sophisticated static code analysis tool designed to prepare for automated ETL testing.
# It analyzes Python modules to extract detailed information about function signatures, input/output types,
# error handling patterns, validation checks, and function dependencies. This tool serves as the preparatory
# step for the ETL Test Generator (etl_test_gen_runner.py), gathering all necessary information without
# generating tests itself.
#
# Key capabilities include:
# 1. Function Signature Extraction:
#    - Captures function names, parameters, default values, and annotations
#    - Analyzes docstrings for additional type information
#    - Identifies class methods and their relationships
#
# 2. Input/Output Type Analysis:
#    - Tracks parameter types through type hints and inference
#    - Determines return types and possible return values
#    - Maps data flow between function inputs and outputs
#
# 3. Complexity and Dependency Analysis:
#    - Calculates cyclomatic complexity for each function
#    - Identifies function call patterns and dependencies
#    - Maps the execution flow across the codebase
#
# 4. Error Handling Pattern Detection:
#    - Identifies try-except blocks and error types
#    - Analyzes validation checks and assertions
#    - Detects error propagation patterns
#
# 5. Code Structure Analysis:
#    - Examines class hierarchies and inheritance
#    - Identifies module-level variables and constants
#    - Analyzes import patterns and external dependencies
#
# The analyzer traverses the Abstract Syntax Tree (AST) of Python code to perform its analysis,
# providing a comprehensive view of the codebase structure and behavior patterns.
#
# B. OUTPUT DETAILS
# ----------------
# The IO Analyzer produces a structured JSON report (unit_test_preparation.json) containing:
#
# 1. Function Metadata:
#    - Complete function signatures with parameter names and types
#    - Return type information extracted from annotations and docstrings
#    - Default parameter values and optional parameters
#    - Function complexity metrics and call patterns
#
# 2. Error Handling Information:
#    - Types of exceptions caught in try-except blocks
#    - Custom exception classes and their hierarchy
#    - Error propagation patterns across functions
#
# 3. Validation Patterns:
#    - Input validation checks (type checking, value validation)
#    - Assertions and their conditions
#    - Parameter constraints and requirements
#
# 4. Dependency Maps:
#    - Function call relationships (caller/callee)
#    - Data flow between functions
#    - Module dependencies and import relationships
#
# 5. Test Generation Hints:
#    - Identification of path-related parameters for file mocking
#    - XML-related parameters for structured data mocking
#    - Complexity indicators for test prioritization
#    - Error-prone functions requiring special test attention
#
# The output is designed to be consumed by the ETL Test Generator, which uses this information
# to create appropriate test environments, generate mock arguments, and execute tests with
# proper error handling and timeout protection.

##################################################
#  config.json
###############################################
# {
#   "documentation": {
#     "description": "Consolidated config file for both io_analyzer.py and main_consolidated.py",
#     "purpose": "Single source of truth for all configuration settings",
#     "replaces": "Separate config files previously in the root and etl_pipeline directories",
#     "last_updated": "2025-03-03",
#     "usage": "Pass this file to scripts using the --config parameter",
#     "example": "python io_analyzer.py --config path/to/consolidated_config.json",
#     "notes": "All paths use ${base_dir} for portability"
#   },
#
#   "base_dir": "C:/Users/samha/OneDrive/Desktop/EQ_SUBMITTED_AUTO_PDM",
#
#   "etl_pipeline": {
#     "input_files": {
#       "file_a": "${base_dir}/etl_pipeline/input/collection_n_schema.json",
#       "file_a_xml": "${base_dir}/etl_pipeline/input/collection_n_schema.xml",
#       "file_b": "${base_dir}/etl_pipeline/input/collection_b_schema.json"
#     },
#     "output_files": {
#       "scripts": {
#         "file_a": "${base_dir}/etl_pipeline/output/scripts/item_n.py",
#         "file_a_xml": "${base_dir}/etl_pipeline/output/scripts/item_n_xml.py",
#         "file_b": "${base_dir}/etl_pipeline/output/scripts/item_b.py"
#       },
#       "data": {
#         "json_flatout": "${base_dir}/etl_pipeline/output/data/json_n_flatout.json",
#         "xml_flatout": "${base_dir}/etl_pipeline/output/data/xml_n_flatout.json",
#         "pattern_analysis": "${base_dir}/etl_pipeline/output/data/pattern_analysis.json",
#         "memory_metrics": "${base_dir}/etl_pipeline/output/data/memory_metrics.log"
#       },
#       "comparison": {
#         "intersect_json": "${base_dir}/etl_pipeline/output/comparison/intersect_json_bn.json",
#         "intersect_xml": "${base_dir}/etl_pipeline/output/comparison/intersect_xml_bn.json",
#         "matched_fields_json": "${base_dir}/etl_pipeline/output/comparison/matched_fields_json.json",
#         "nonmatched_fields_json": "${base_dir}/etl_pipeline/output/comparison/nonmatched_fields_json.json",
#         "matched_fields_xml": "${base_dir}/etl_pipeline/output/comparison/matched_fields_xml.json",
#         "nonmatched_fields_xml": "${base_dir}/etl_pipeline/output/comparison/nonmatched_fields_xml.json"
#       }
#     },
#     "validation": {
#       "draft": 7,
#       "strict_mode": true,
#       "additional_properties": false
#     },
#     "model_generation": {
#       "type_mapping": {
#         "int": "int",
#         "float": "float",
#         "str": "str",
#         "bool": "bool",
#         "None": "Optional[Any]",
#         "list": "List[Any]",
#         "dict": "dict"
#       },
#       "indent": "    "
#     },
#     "transform_rules": {
#       "flatten_arrays": true,
#       "parse_json_strings": true,
#       "strip_prefixes": true
#     }
#   },
#
#   "io_analyzer": {
#     "input_files": {
#       "file_a": "${base_dir}/etl_pipeline/input/collection_n_schema.json",
#       "file_b": "${base_dir}/etl_pipeline/input/collection_b_schema.json",
#       "file_a_xml": "${base_dir}/etl_pipeline/input/collection_n_schema.xml"
#     },
#     "output_files": {
#       "pattern_analysis": "${base_dir}/etl_pipeline/output/data/pattern_analysis.json",
#       "memory_metrics": "${base_dir}/etl_pipeline/output/data/memory_metrics.log"
#     },
#     "analysis_settings": {
#       "depth_calculation": {
#         "max_depth": 10,
#         "track_changes": true
#       },
#       "data_quality_checks": {
#         "check_types": true,
#         "check_null": true,
#         "check_patterns": true
#       }
#     },
#     "analysis": {
#       "output_directory": "${base_dir}/etl_pipeline/output/analysis",
#       "data_quality": {
#         "enabled": true,
#         "check_types": true,
#         "check_null": true,
#         "check_patterns": true,
#         "output_file": "data_quality_report.json"
#       },
#       "performance": {
#         "track_memory": true,
#         "track_time": true,
#         "track_io": true,
#         "output_file": "performance_metrics.json"
#       },
#       "structure": {
#         "max_depth": 10,
#         "track_changes": true,
#         "analyze_patterns": true,
#         "output_file": "structure_analysis.json"
#       }
#     },
#     "target_file": "${base_dir}/main_consolidated.py",
#     "output_file": "${base_dir}/unit_test_preparation.json"
#   },
#
#   "test_generator": {
#     "validate_schema": true,
#     "paths": {
#       "input_files": {
#         "test": "${base_dir}/test_generator/test/input",
#         "test_file_path": "${base_dir}/test_generator/test/test_file_path.json"
#       },
#       "output_files": {
#         "test": "${base_dir}/test_generator/test/output"
#       }
#     }
#   },
#
#   "logging": {
#     "level": "INFO",
#     "path": "${base_dir}/etl_pipeline/logs/etl.log",
#     "handlers": ["file", "stream", "rotating"],
#     "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     "maxBytes": 10485760,
#     "backupCount": 5,



#
# C. LIMITATIONS
# ------------
# The IO Analyzer has several limitations in its current implementation:
#
# 1. Static Analysis Constraints:
#    - Limited ability to analyze dynamically generated code (eval, exec)
#    - Cannot fully resolve runtime type information for dynamic typing
#    - May miss complex metaprogramming patterns (decorators, metaclasses)
#    - Limited understanding of duck typing and protocol implementations
#
# 2. Type Inference Limitations:
#    - Relies heavily on explicit type hints, which may be absent
#    - Cannot always determine types for variables with multiple possible types
#    - Limited ability to infer types from external library functions
#    - May not correctly handle complex generic types or unions
#
# 3. Dependency Resolution Issues:
#    - Cannot fully resolve dynamic imports (importlib.import_module)
#    - Limited ability to track dependencies across module boundaries
#    - May miss indirect dependencies through container objects
#    - Cannot track dependencies through reflection (getattr, setattr)
#
# 4. Error Handling Analysis Gaps:
#    - Cannot determine all possible runtime exceptions
#    - Limited understanding of exception propagation across modules
#    - May not identify all error conditions in complex expressions
#    - Cannot analyze error handling in external libraries
#
# 5. Performance Considerations:
#    - May be memory-intensive for large codebases
#    - AST parsing can be slow for very large files
#    - Limited parallelization capabilities for multi-file analysis
#
# D. AREAS FOR IMPROVEMENT
# ----------------------
# Several areas could be enhanced in future versions:
#
# 1. Type Analysis Enhancements:
#    - Integration with type checkers like mypy or pyright
#    - Runtime type collection through instrumented execution
#    - Better inference for container types and their contents
#    - Support for more complex typing constructs (Protocols, TypedDict)
#
# 2. Dynamic Analysis Integration:
#    - Combine static analysis with limited runtime execution
#    - Collect actual types during sample executions
#    - Track actual function call patterns during execution
#    - Validate static analysis findings with runtime behavior
#
# 3. Dependency Analysis Improvements:
#    - Better cross-module dependency tracking
#    - Analysis of external library dependencies
#    - Visualization of dependency graphs
#    - Detection of circular dependencies
#
# 4. Code Coverage Integration:
#    - Identify untested or partially tested functions
#    - Highlight high-risk areas with low coverage
#    - Suggest test priorities based on complexity and coverage
#    - Track historical test results for regression analysis
#
# 5. Performance Optimizations:
#    - Incremental analysis for changed files only
#    - Parallel processing of independent modules
#    - Caching of intermediate analysis results
#    - Memory-efficient representations of large ASTs
#
# 6. User Experience Enhancements:
#    - Interactive visualization of analysis results
#    - IDE integration for real-time analysis
#    - Better error reporting and suggestions
#    - Configuration options for analysis depth and focus
#
# E. LINUX DEPLOYMENT CONSIDERATIONS
# --------------------------------
# When deploying and running the IO Analyzer on Linux systems:
#
# 1. Environment Setup:
#    - Ensure Python 3.7+ is installed (3.8+ recommended)
#    - Install required dependencies: ast, inspect, json, logging
#    - Consider using a virtual environment for isolation
#    - Set PYTHONPATH to include all necessary modules
#
# 2. File System Considerations:
#    - Use absolute paths or paths relative to a known base directory
#    - Be aware of case sensitivity in file paths (unlike Windows)
#    - Ensure proper file permissions for reading source files
#    - Use os.path.join() or pathlib.Path for cross-platform compatibility
#
# 3. Performance Tuning:
#    - Set appropriate process priority (nice) for background analysis
#    - Consider memory limits for large codebases
#    - Use tmpfs for temporary files to improve I/O performance
#    - Monitor CPU and memory usage during analysis
#
# 4. Error Handling:
#    - Implement proper logging to system logs or dedicated log files
#    - Set up monitoring for long-running analyses
#    - Consider implementing timeout mechanisms for large files
#    - Handle file encoding issues (use utf-8 with error handling)
#
# 5. Integration Options:
#    - Set up as a service using systemd for scheduled analysis
#    - Configure as part of CI/CD pipelines
#    - Consider containerization with Docker for consistent environments
#    - Implement proper exit codes for script integration
#
# F. EXECUTION TRACE EXAMPLE
# ------------------------
# Below is a typical execution trace of the IO Analyzer:
# $ python io_analyzer.py --config "/path/to/config.json"
#
# [INFO] IO Analyzer starting up [INFO] Loading configuration from /path/to/config.json
# [INFO] Base path set to /path/to/project [INFO] Discovered 42 Python modules for analysis
# [INFO] NumPy version: 1.21.5 [INFO] Pandas version: 1.3.5
#
# [INFO] Analyzing module: main.py [INFO] Found 4 functions in main.py
# [DEBUG] Analyzing function: setup_basic_logging [DEBUG] Input Types: {'debug': 'bool'} [DEBUG] Output Type: Any
# [DEBUG] Complexity: 2 [DEBUG] Error Handlers: ['ImportError']
#
# [INFO] Analyzing module: core/config_handler.py [INFO] Found 8 functions in config_handler.py
# [DEBUG] Analyzing function: _load_config [DEBUG] Input Types: {} [DEBUG] Output Type: Dict [DEBUG] Complexity: 12
# [DEBUG] Validation Checks: 6 found [DEBUG] Function Calls: 25 found
#
# [INFO] Analyzing module: core/platform_utils.py [INFO] Found 4 functions in platform_utils.py
# [DEBUG] Analyzing function: _get_platform_info [DEBUG] Input Types: {} [DEBUG] Output Type: Dict
# [DEBUG] Complexity: 5 [DEBUG] Error Handlers: ['Exception'] [DEBUG] Validation Checks: 2 found
#
# [INFO] Analyzing module: etl/processor.py [INFO] Found 13 functions in processor.py
# [DEBUG] Analyzing function: process_data
# [DEBUG] Input Types: {'file_path': 'Path', 'data_type': 'str', 'schema_keys': 'Set'}
# [DEBUG] Output Type: List [DEBUG] Complexity: 18
# [DEBUG] Error Handlers: ['Exception', 'FileNotFoundError', 'IOError', 'PermissionError']
# [DEBUG] Validation Checks: 6 found [DEBUG] Function Calls: 42 found
#
# [INFO] Analyzing module: models/schema_handler.py [INFO] Found 10 functions in schema_handler.py
# [DEBUG] Analyzing function: load_schema [DEBUG] Input Types: {'schema_path': 'str'}
# [DEBUG] Output Type: Dict [DEBUG] Complexity: 15 [DEBUG] Error Handlers: ['IOError']
# [DEBUG] Validation Checks: 8 found [DEBUG] Function Calls: 35 found
#
# [INFO] Analyzing module: output/scripts/item_n.py [INFO] Found 1 functions in item_n.py
# [DEBUG] Analyzing function: decode_json_strings [DEBUG] Input Types: {'cls': 'Any', 'v': 'Any'}
# [DEBUG] Output Type: Any [DEBUG] Complexity: 3 [DEBUG] Validation Checks: 1 found [DEBUG] Function Calls: 5 found
#
# [INFO] Analysis complete [INFO] Total functions analyzed: 40 [INFO] Average function complexity: 9.8
# [INFO] Functions with high complexity (>10): 15 [INFO] Functions with error handlers: 22
# [INFO] Writing analysis results to unit_test_preparation.json [INFO] Analysis completed in 12.4 seconds
#
# This trace shows the analyzer processing each module, extracting function information,
# and calculating metrics before writing the final analysis to the output JSON file.
# The detailed function-level information helps the test generator create appropriate
# test environments and mock data. Usage: python io_analyzer.py --config "/path/to/config.json" """
#
# run..

# # 2. Run the IO Analyzer
# python io_analyzer.py --config C:/Users/samha/PycharmProjects/EQ_FINAL_03_04/consolidated_config.json
#

##############################################################
#
# Comprehensive Trace Execution Analysis for IO Analyzer
# (Current Implementation - 2025)
# ##############################################################
#
# 1. Entry Point and Initialization
#   - Begins at if __name__ == "__main__" block
#     • sys.exit(main())
#   - Creates argument parser for command-line options
#     • Command-line parsing: --config flag detection
#     • config_path = sys.argv[2] if appropriate command-line args present
#   - Loads configuration from specified JSON file
#     • with open(config_path, 'r', encoding='utf-8') as f:
#     • config = json.load(f)
#     • Error handling for missing or malformed config
#   - Sets up logging environment
#     • logging.basicConfig() with specified level from config
#     • console_handler = logging.StreamHandler()
#     • logger.addHandler(console_handler)
#   - Initializes module-level variables and data structures
#     • _currently_analyzing = set()  # Prevent infinite recursion
#     • data_analyzers and flow_analyzers initialization
#
# 2. Configuration Parsing and Project Setup
#   - Resolves configuration paths with variable substitution
#     • base_dir = config.get('base_dir', '')
#     • target_file_path = config.get('io_analyzer', {}).get('target_file', '')
#     • target_file = Path(target_file_path.replace('${base_dir}', base_dir))
#   - Validates target file existence
#     • if not target_file.exists():
#     • logger.error(f"Target file not found: {target_file}")
#   - Sets up output directories and paths
#     • output_path = Path('unit_test_preparation.json')
#     • Path(output_dir).mkdir(parents=True, exist_ok=True)
#   - Initializes analyzer instances
#     • io_analyzer = IOAnalyzer()
#     • data_analyzer = EnhancedDataAnalyzer()
#   - Prepares custom print/output handlers for filtered logging
#     • filtered_print() function to suppress excessive output
#     • filtered_write() function for stdout
#
# 3. Module Analysis Process
#   - For the target source file:
#     * Reads file content with encoding handling
#       • with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
#       • source = f.read()
#     * Parses source into Abstract Syntax Tree (AST)
#       • tree = ast.parse(source)
#       • Validates if tree contains functions or classes
#     * Creates execution namespace for analysis
#       • module_namespace = {...} with standard imports and types
#       • exec(mod, module_namespace)
#     * Tracks already processed functions to avoid duplicates
#       • processed_functions = set()
#       • processed_functions.add(func_name)
#     * Handles circular references with analysis tracking
#       • _currently_analyzing.add(file_key)
#       • _currently_analyzing.discard(file_key) in finally block
#
# 4. Function Discovery and Extraction
#   - Scans module AST for function definitions:
#     * Identifies user-defined functions (excluding special methods)
#       • if isinstance(node, ast.FunctionDef) and is_user_defined(node, source):
#       • func_name = node.name
#     * Extracts function source code with proper indentation handling
#       • func_source = ast.get_source_segment(source, node)
#       • lines = func_source.split('\n')
#       • indent = len(lines[0]) - len(lines[0].lstrip())
#       • unindented_source = '\n'.join(line[indent:] if len(line) >= indent else line for line in lines)
#     * Creates AST for individual function analysis
#       • func_tree = ast.parse(unindented_source)
#     * Prints diagnostic information for debugging
#       • Debug output of first 5 lines of each function
#       • Control structure identification in functions
#
# 5. Class Method Discovery and Extraction
#   - Scans module AST for class definitions:
#     * Identifies class definitions and their methods
#       • for class_node in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:
#       • class_name = class_node.name
#     * Processes each method within the class
#       • for method_node in [n for n in class_node.body if isinstance(n, ast.FunctionDef)]:
#       • method_name = method_node.name
#       • full_method_name = f"{class_name}.{method_name}"
#     * Extracts method source code with accurate indentation handling
#       • method_source = ast.get_source_segment(source, method_node)
#       • method_lines = method_source.split('\n')
#       • method_indent = len(method_lines[0]) - len(method_lines[0].lstrip())
#     * Creates AST for individual method analysis
#       • method_tree = ast.parse(unindented_source)
#     * Uses placeholder methods for analysis when function objects aren't available
#       • def placeholder_method(*args, **kwargs): pass
#       • placeholder_method.__name__ = method_name
#
# 6. Function Analysis
#   - For each discovered function:
#     * Analyzes function signature and parameters
#       • signature = inspect.signature(function)
#       • Input parameter type extraction with fallbacks:
#         - Extracts parameter types from annotations when available
#         - Handles special case for 'self' parameter in methods
#         - Defaults to 'Any' when type information is unavailable
#       • Return type extraction with fallbacks:
#         - Extracts return type from annotation when available
#         - Handles complex return type annotations
#         - Defaults to 'Any' when return type is unspecified
#     * Calculates cyclomatic complexity
#       • Starting with base complexity of 1
#       • Adds complexity for conditionals (if/elif statements)
#       • Adds complexity for loops (for/while)
#       • Adds complexity for exception handlers (try/except)
#       • Adds complexity for boolean operations
#       • Adds complexity for ternary expressions and comprehensions
#     * Identifies error handling mechanisms
#       • Finds try/except blocks and extracts exception types
#       • Records handler types for each exception block
#     * Detects validation patterns
#       • Extracts conditional statements for validation analysis
#       • Identifies assertion patterns
#     * Maps function call dependencies
#       • Identifies direct function calls (func())
#       • Identifies method calls (obj.method())
#       • Records function call relationships
#
# 7. Test Generation Hint Creation
#   - Constructs test generation metadata:
#     * Path-related parameters identification
#       • Identifies parameters likely representing file paths
#       • path_types = [param for param in input_types.keys() if 'path' in param.lower()]
#     * XML-related parameters identification
#       • Identifies parameters likely representing XML data
#       • xml_types = [param for param in input_types.keys() if 'xml' in param.lower()]
#     * Complexity-based criticality assessment
#       • critical_complexity = analysis.complexity > 10
#     * Error-proneness assessment
#       • error_prone = len(analysis.error_handlers) > 0
#     * Stores test generation hints with function analysis:
#       • test_generation_hints = {
#           'path_types': path_types,
#           'xml_types': xml_types,
#           'critical_complexity': critical_complexity,
#           'error_prone': error_prone
#         }
#
# 8. Results Collection and Structuring
#   - Builds unified results dictionary:
#     * Organizes results by file path
#       • results[str(target_file)] = { 'functions': {} }
#     * For each analyzed function, stores:
#       • Input parameter types: analysis.input_types
#       • Output/return types: analysis.output_type
#       • Error handling mechanisms: analysis.error_handlers
#       • Validation patterns: analysis.validation_checks
#       • Complexity metrics: analysis.complexity
#       • Function call dependencies: analysis.function_calls
#       • Test generation hints: test_generation_hints
#     * Enhanced output filtering for readability:
#       • Suppresses large data dumps with filtered_print
#       • Shows progress messages while hiding excess content
#       • Focuses output on analysis metrics and completion status
#
# 9. Output Generation
#   - Writes analysis results to JSON file:
#     * Creates structured JSON representation:
#       • with open(output_path, 'w') as f:
#       • json.dump(results, f, indent=2, cls=CustomJSONEncoder)
#     * Uses custom JSON encoder for special types:
#       • Path objects serialized to strings
#       • Custom analysis objects with to_json method support
#     * Provides formatted console display of results:
#       • Display paths for output files
#       • Shows function count and analysis metrics
#       • Restores original print/output functions after completion
#     * Logs completion status:
#       • logger.info(f"Unit test preparation data saved to {output_path}")
#     * Displays content of generated file:
#       • print("\n" + "=" * 50)
#       • print("CONTENTS OF unit_test_preparation.json:")
#
# 10. Error Handling and Cleanup
#   - Provides comprehensive error handling:
#     * File-level error handling
#       • try/except blocks for file operations
#       • Error reporting for missing or inaccessible files
#     * AST parsing error handling
#       • SyntaxError handling with fallback parsing
#       • Stripped whitespace as alternative parsing strategy
#     * Function analysis error handling
#       • try/except for each function to prevent cascade failures
#       • Fallback to placeholder analysis for problematic functions
#     * Configuration error handling
#       • Validation of config file structure
#       • Default values for missing configuration options
#     * System-level exception management
#       • traceback printing for unhandled exceptions
#       • Non-zero exit code for error conditions
#     * Special handling for circular imports
#       • _currently_analyzing tracking set
#       • Proper cleanup in finally blocks
#
##############################################################


#########################################################

#########################################################
import ast
import inspect
import json
import logging
import sys
import os
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from functools import wraps
from pydantic import BaseModel, field_validator
import warnings
import sys
import time
import os
import builtins




# Configure logging and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger(__name__)

# Verify NumPy and Pandas dependencies
try:
    import numpy as np
    import pandas as pd
    logger.info(f"NumPy version: {np.__version__}")
    logger.info(f"Pandas version: {pd.__version__}")
except ImportError as e:
    logger.error(f"Import error: {e}")
    # Decide if you want to raise an exception or continue
    # raise RuntimeError(f"Required dependency missing: {e}")


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for our analysis classes"""
    def default(self, obj):
        # Add custom serialization logic for your specific types
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        if isinstance(obj, Path):
            return str(obj)
        # Add more custom type handling as needed
        return super().default(obj)


class ConfigurationError(Exception):
    """Raised when there is a configuration error"""
    pass


class AnalysisError(Exception):
    """Raised when there is an analysis error"""
    pass


# Base Models and Data Classes
class ItemModel(BaseModel):
    @field_validator('*', mode='before')
    @classmethod
    def decode_json_strings(cls, v):
        if isinstance(v, str) and v.strip().startswith('{'):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v


@dataclass
class AnalysisMetrics:
    structure: Dict[str, Any] = field(default_factory=dict)
    quality: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    patterns: Dict[str, Any] = field(default_factory=dict)
    test_cases: Dict[str, Any] = field(default_factory=dict)
    coverage: Dict[str, Any] = field(default_factory=dict)
    anomalies: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataMetrics:
    """Metrics for data quality analysis"""
    completeness: float = 0.0  # % of required fields present
    validity: float = 0.0  # % of fields matching expected type/format
    consistency: float = 0.0  # % of fields matching schema rules
    field_counts: Dict[str, int] = field(default_factory=dict)
    error_counts: Dict[str, int] = field(default_factory=dict)


@dataclass
class SchemaValidation:
    """Schema validation results"""
    required_fields: Set[str]
    optional_fields: Set[str]
    field_types: Dict[str, str]
    constraints: Dict[str, Any]
    metrics: DataMetrics


@dataclass
class TransformationRecord:
    """Record of data transformations"""
    source_field: str
    target_field: str
    transform_type: str
    validation_rules: List[str]
    dependencies: List[str]


@dataclass
class DataAnalysis:
    """Analysis results for input/output data"""
    schema: Dict[str, Any]
    validations: List[str]
    transformations: List[str]
    field_types: Dict[str, str]
    input_types: Dict[str, str] = field(default_factory=dict)  # Added for compatibility
    output_type: str = "Any"  # Added for compatibility


@dataclass
class FunctionAnalysis:
    """Analysis results for a single function"""
    input_types: Dict[str, str]
    output_type: str
    error_handlers: List[str]
    validation_checks: List[str]
    complexity: int
    function_calls: List[str] = field(default_factory=list)
    data_dependencies: List[str] = field(default_factory=list)
    transforms: List[str] = field(default_factory=list)


class Config:
    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.base_path = self.config.get('base_path', '')

    def _load_config(self, path: Path) -> Dict[str, Any]:
        try:
            with open(path) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load config: {e}")

    def get_input_files(self) -> List[Dict[str, str]]:
        input_files = self.config.get('io_analyzer', {}).get('input_files', {})
        return [
            {
                'path': input_files.get(f'file_{k}', '').replace('${base_path}', self.base_path),
                'type': 'json' if not k.endswith('_xml') else 'xml'
            }
            for k in ['a', 'b', 'a_xml']
            if input_files.get(f'file_{k}')
        ]

    def get_output_files(self) -> Dict[str, List[str]]:
        output_files = self.config.get('io_analyzer', {}).get('output_files', {})
        return {
            'json': [output_files.get('pattern_analysis', '').replace('${base_path}', self.base_path)],
            'xml': [output_files.get('memory_metrics', '').replace('${base_path}', self.base_path)]
        }

    def get_logging_config(self) -> Dict[str, Any]:
        return self.config.get('logging', {})


# Utility Functions
def is_user_defined(node: ast.FunctionDef, source: str) -> bool:
    """Check if a function is user-defined and not a special method."""
    if node.name.startswith('__'):
        return False
    try:
        func_source = ast.get_source_segment(source, node)
        return bool(func_source)
    except:
        return False


# Main Analyzer Classes
class DataAnalyzer:
    """Base data analyzer class"""

    def _extract_class_schema(self, node: ast.ClassDef) -> Dict:
        """Extract schema from class definition with better type handling"""
        schema = {}
        for child in node.body:
            if isinstance(child, ast.AnnAssign):
                name = child.target.id
                if hasattr(child.annotation, 'id'):
                    schema[name] = {
                        'type': child.annotation.id,
                        'required': True  # Default to required
                    }
            elif isinstance(child, (ast.Assign, ast.Call)):
                # Handle default values and field declarations
                for target in getattr(child, 'targets', []):
                    if isinstance(target, ast.Name):
                        schema[target.id] = {
                            'type': 'Any',
                            'required': False
                        }
        return schema

    def analyze_input(self, file_path: Path) -> DataAnalysis:
        """Analyze input with improved error handling"""
        try:
            if file_path.name == '__init__.py':
                return DataAnalysis({}, [], [], {})

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()

            tree = ast.parse(data)
            validations = []
            transformations = []
            schema = {}

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    schema.update(self._extract_class_schema(node))
                if isinstance(node, ast.Assert):
                    validations.append(ast.unparse(node.test))

            # Create schema validation
            validation = self._validate_schema(schema)
            metrics = self._calculate_metrics(validation)

            return DataAnalysis(
                schema={
                    'validation': validation,
                    'metrics': metrics,
                    'fields': schema
                },
                validations=validations,
                transformations=transformations,
                field_types=validation.field_types
            )

        except Exception as e:
            logger.error(f"Failed to analyze input file {file_path}: {e}")
            return DataAnalysis({}, [], [], {})

    def analyze_output(self, file_path: Path) -> DataAnalysis:
        return self.analyze_input(file_path)  # Reuse input analysis for now

    def _validate_schema(self, schema: Dict) -> SchemaValidation:
        """Default schema validation implementation"""
        # Implement a basic version that will be overridden by EnhancedDataAnalyzer
        return SchemaValidation(
            required_fields=set(),
            optional_fields=set(),
            field_types={},
            constraints={},
            metrics=DataMetrics()
        )

    def _calculate_metrics(self, validation: SchemaValidation) -> DataMetrics:
        """Default metrics calculation implementation"""
        # Implement a basic version that will be overridden by EnhancedDataAnalyzer
        return DataMetrics()

    def _infer_types(self, schema: Dict) -> Dict[str, str]:
        type_map = {}
        for field, value in schema.items():
            if isinstance(value, str):
                type_map[field] = value
            else:
                type_map[field] = type(value).__name__
        return type_map


class ModuleLoader:
    """Handles loading and validating Python modules"""

    @staticmethod
    def validate_module_file(file_path: Path) -> bool:
        """Validate Python module file before importing"""
        try:
            print(f"DEBUG: Validating module file: {file_path}")
            # Read and validate file content
            with open(file_path, 'rb') as f:
                content = f.read()

            # Check for null bytes
            null_count = content.count(b'\x00')
            print(f"DEBUG: Found {null_count} null bytes in {file_path}")

            # Remove null bytes if present
            if b'\x00' in content:
                print(f"DEBUG: Cleaning {null_count} null bytes from {file_path}")
                content = content.replace(b'\x00', b'')
                # Clean up other potential issues
                content = content.replace(b'\r\n', b'\n')

                # Write cleaned content back
                print(f"DEBUG: Writing cleaned content back to {file_path}")
                with open(file_path, 'wb') as f:
                    f.write(content)

                # Verify file was written correctly
                with open(file_path, 'rb') as f:
                    new_content = f.read()
                    new_null_count = new_content.count(b'\x00')
                    print(f"DEBUG: After cleaning, file has {new_null_count} null bytes")

            # Try to decode and compile
            try:
                text_content = content.decode('utf-8', errors='ignore')
                print(f"DEBUG: Successfully decoded file content, length: {len(text_content)}")
                print(f"DEBUG: First 100 characters: {text_content[:100]}")
                compile(text_content, str(file_path), 'exec')
                print(f"DEBUG: Successfully compiled content")
            except Exception as e:
                print(f"DEBUG: Error during decode/compile: {e}")
                raise

            return True
        except Exception as e:
            logger.error(f"Module validation failed for {file_path}: {e}")
            print(f"DEBUG: Exception in validate_module_file: {str(e)}")
            return False


class EnhancedDataAnalyzer(DataAnalyzer):
    """Enhanced analyzer with better schema validation and metrics"""

    def analyze_input(self, file_path: Path) -> DataAnalysis:
        """Analyze input data with enhanced validation"""
        try:
            analysis = super().analyze_input(file_path)

            # Add schema validation
            validation = self._validate_schema(analysis.schema)
            metrics = self._calculate_metrics(validation)
            transformations = self._track_transformations(analysis.schema)

            # Update analysis with enhanced data
            analysis.schema.update({
                'validation': validation,
                'metrics': metrics,
                'transformations': transformations
            })

            return analysis

        except Exception as e:
            logger.error(f"Enhanced input analysis failed: {e}")
            return DataAnalysis({}, [], [], {})

    def _validate_schema(self, schema: Dict) -> SchemaValidation:
        """Validate schema with better type handling"""
        if isinstance(schema, str):
            # Handle string inputs
            return SchemaValidation(
                required_fields=set(),
                optional_fields=set(),
                field_types={},
                constraints={},
                metrics=DataMetrics()
            )

        required = set()
        optional = set()
        types = {}
        constraints = {}

        for field, props in schema.items():
            if isinstance(props, dict):
                # Handle dictionary schema
                if props.get('required', True):
                    required.add(field)
                else:
                    optional.add(field)
                types[field] = props.get('type', 'Any')
                if 'constraints' in props:
                    constraints[field] = props['constraints']
            else:
                # Handle direct type specification
                required.add(field)
                types[field] = str(props)

        return SchemaValidation(
            required_fields=required,
            optional_fields=optional,
            field_types=types,
            constraints=constraints,
            metrics=DataMetrics()
        )

    def _calculate_metrics(self, validation: SchemaValidation) -> DataMetrics:
        """Calculate data quality metrics"""
        metrics = DataMetrics()

        # Calculate completeness
        total_required = len(validation.required_fields)
        present_required = sum(1 for f in validation.required_fields
                               if f in validation.field_types)
        metrics.completeness = present_required / total_required if total_required > 0 else 1.0

        # Calculate validity
        valid_fields = sum(1 for f, t in validation.field_types.items()
                           if self._is_valid_type(f, t))
        total_fields = len(validation.field_types)
        metrics.validity = valid_fields / total_fields if total_fields > 0 else 1.0

        # Calculate consistency
        consistent_fields = sum(1 for f in validation.field_types
                                if self._meets_constraints(f, validation.constraints))
        metrics.consistency = consistent_fields / total_fields if total_fields > 0 else 1.0

        return metrics

    def _track_transformations(self, schema: Dict) -> List[TransformationRecord]:
        """Track data transformations"""
        transforms = []

        for field, props in schema.items():
            if 'derived_from' in props:
                transforms.append(
                    TransformationRecord(
                        source_field=props['derived_from'],
                        target_field=field,
                        transform_type=props.get('transform_type', 'unknown'),
                        validation_rules=props.get('validations', []),
                        dependencies=props.get('dependencies', [])
                    )
                )

        return transforms

    def _is_valid_type(self, field: str, expected_type: str) -> bool:
        """Check if field value matches expected type"""
        try:
            # Add type validation logic
            return True
        except:
            return False

    def _meets_constraints(self, field: str, constraints: Dict) -> bool:
        """Check if field meets defined constraints"""
        try:
            if field not in constraints:
                return True
            # Add constraint validation logic
            return True
        except:
            return False


class FlowAnalyzer:
    """Analyzes data flow through the ETL pipeline"""

    def analyze(self, function_analysis: Dict[str, FunctionAnalysis]) -> Dict[str, Any]:
        flow_data = {
            'dependencies': self._analyze_dependencies(function_analysis),
            'critical_paths': self._find_critical_paths(function_analysis),
            'data_flow': self._analyze_data_flow(function_analysis)
        }
        return flow_data

    def _analyze_dependencies(self, func_analysis: Dict[str, FunctionAnalysis]) -> Dict[str, List[str]]:
        deps = {}
        for func_name, analysis in func_analysis.items():
            deps[func_name] = analysis.function_calls
        return deps

    def _find_critical_paths(self, func_analysis: Dict[str, FunctionAnalysis]) -> List[str]:
        critical = []
        for func_name, analysis in func_analysis.items():
            if analysis.complexity > 10 or len(analysis.function_calls) > 5:
                critical.append(func_name)
        return critical

    def _analyze_data_flow(self, func_analysis: Dict[str, FunctionAnalysis]) -> Dict[str, List[str]]:
        flows = {}
        for func_name, analysis in func_analysis.items():
            flows[func_name] = {
                'inputs': list(analysis.input_types.keys()),
                'transforms': analysis.transforms,
                'output': analysis.output_type
            }
        return flows


class EnhancedFlowAnalyzer(FlowAnalyzer):
    """Enhanced flow analyzer with better dependency tracking"""

    def analyze(self, function_analysis: Dict[str, FunctionAnalysis]) -> Dict[str, Any]:
        """Enhanced flow analysis"""
        flow_data = super().analyze(function_analysis)

        # Add enhanced analysis
        flow_data.update({
            'lineage': self._generate_lineage(function_analysis),
            'transformations': self._track_transformations(function_analysis),
            'state_transitions': self._analyze_state_transitions(function_analysis)
        })

        return flow_data

    def _generate_lineage(self, func_analysis: Dict[str, FunctionAnalysis]) -> Dict:
        """Generate data lineage graph"""
        lineage = {
            'nodes': [],
            'edges': []
        }

        # Track data flow between functions
        for func_name, analysis in func_analysis.items():
            lineage['nodes'].append({
                'id': func_name,
                'type': 'function',
                'inputs': list(analysis.input_types.keys()),
                'outputs': [analysis.output_type]
            })

            # Add edges for data dependencies
            for dep in analysis.data_dependencies:
                lineage['edges'].append({
                    'source': dep,
                    'target': func_name,
                    'type': 'data_dependency'
                })

        return lineage

    def _track_transformations(self, func_analysis: Dict[str, FunctionAnalysis]) -> List[Dict]:
        """Track data transformations across pipeline stages"""
        transforms = []

        for func_name, analysis in func_analysis.items():
            # Track function-level transformations
            for transform in analysis.transforms:
                transforms.append({
                    'function': func_name,
                    'transform': transform,
                    'inputs': list(analysis.input_types.keys()),
                    'output': analysis.output_type
                })

        return transforms

    def _analyze_state_transitions(self, func_analysis: Dict[str, FunctionAnalysis]) -> Dict:
        """Analyze data state transitions"""
        transitions = {}

        for func_name, analysis in func_analysis.items():
            # Track state changes
            transitions[func_name] = {
                'initial_state': self._get_input_state(analysis),
                'final_state': self._get_output_state(analysis),
                'transformations': analysis.transforms
            }

        return transitions

    def _get_input_state(self, analysis: FunctionAnalysis) -> Dict:
        """Get input data state"""
        return {
            'types': analysis.input_types,
            'validations': analysis.validation_checks
        }

    def _get_output_state(self, analysis: FunctionAnalysis) -> Dict:
        """Get output data state"""
        return {
            'type': analysis.output_type,
            'dependencies': analysis.data_dependencies
        }


class IOAnalyzer:
    """Analyzes function I/O patterns to assist test generation"""
    _currently_analyzing = set()

    def run_tests(self, io_analyzer_results_path: Optional[Path] = None) -> Dict[str, Dict[str, Dict]]:
        """Run tests with optional IO_Analyzer metadata integration"""
        # Load IO_Analyzer results if path is provided
        if io_analyzer_results_path and io_analyzer_results_path.exists():
            try:
                with open(io_analyzer_results_path, 'r') as f:
                    io_analyzer_data = json.load(f)

                # Extend type handlers based on IO_Analyzer insights
                for module_path, module_info in io_analyzer_data.items():
                    for func_name, func_details in module_info.get('functions', {}).items():
                        # Enhance type handlers based on input types
                        for param, param_type in func_details.get('input_types', {}).items():
                            if param_type not in self.type_handlers:
                                # Add custom handler for specific types
                                if 'path' in param.lower():
                                    self.type_handlers[param_type] = lambda: str(
                                        self.project_root / 'test' / f'test_{param}.json')
                                elif 'xml' in param.lower():
                                    self.type_handlers[param_type] = self._create_test_xml_element

            except Exception as e:
                self.logger.error(f"Error loading IO_Analyzer results: {e}")

    def analyze_function(self, function) -> FunctionAnalysis:
        """Analyze a function with improved source extraction and complexity calculation"""
        try:
            # Get function source and create AST
            source = inspect.getsource(function)

            # Clean up source indentation
            lines = source.split('\n')
            if lines:
                # Calculate the indentation of the first line
                indent = len(lines[0]) - len(lines[0].lstrip())
                # Remove that indentation from all lines
                source = '\n'.join(line[indent:] if len(line) >= indent else line for line in lines)

            # Parse the clean source into an AST for analysis
            try:
                func_tree = ast.parse(source)
                print(f"DEBUG: Successfully parsed function source ({len(source)} chars)")
            except SyntaxError as e:
                print(f"DEBUG: Syntax error parsing function source: {e}")
                # Try a more forgiving approach
                func_tree = ast.parse("\n".join(line for line in source.split('\n') if line.strip()))
                print(f"DEBUG: Parsed with stripped empty lines")

            # Extract function signature
            signature = inspect.signature(function)

            # Extract input types
            input_types = {}
            for name, param in signature.parameters.items():
                if name != 'self':  # Skip self parameter for methods
                    try:
                        if param.annotation != inspect.Parameter.empty:
                            if hasattr(param.annotation, '__name__'):
                                type_name = param.annotation.__name__
                            else:
                                type_name = str(param.annotation).replace('typing.', '')
                        else:
                            type_name = 'Any'
                    except AttributeError:
                        type_name = 'Any'
                    input_types[name] = type_name

            # Extract output type
            try:
                if signature.return_annotation != inspect.Parameter.empty:
                    if hasattr(signature.return_annotation, '__name__'):
                        output_type = signature.return_annotation.__name__
                    else:
                        output_type = str(signature.return_annotation).replace('typing.', '')
                else:
                    output_type = 'Any'
            except AttributeError:
                output_type = 'Any'

            # Calculate complexity with detailed debug info
            complexity = self._calculate_complexity(func_tree)

            # Find error handlers, validations, function calls
            error_handlers = self._find_error_handlers(func_tree)
            validation_checks = self._find_validations(func_tree)
            function_calls = self._find_function_calls(func_tree)

            # Create analysis result
            analysis = FunctionAnalysis(
                input_types=input_types,
                output_type=output_type,
                error_handlers=error_handlers,
                validation_checks=validation_checks,
                complexity=complexity,
                function_calls=function_calls
            )

            # Add additional analyses
            analysis.data_dependencies = self._find_data_dependencies(func_tree)
            analysis.transforms = self._find_transformations(func_tree)

            return analysis

        except Exception as e:
            print(f"DEBUG: Function analysis failed: {str(e)}")
            return FunctionAnalysis(
                input_types={},
                output_type='Any',
                error_handlers=[],
                validation_checks=[],
                complexity=1,
                function_calls=[],
                data_dependencies=[],
                transforms=[]
            )

    def export_function_metadata(self, file_path: Path) -> Dict:
        """Export comprehensive function metadata for test generation"""
        analysis = self.analyze_file(file_path)
        enhanced_metadata = {}

        for func_name, func_details in analysis.items():
            enhanced_metadata[func_name] = {
                'input_types': func_details.input_types,
                'output_type': func_details.output_type,
                'complexity': func_details.complexity,
                'error_handlers': func_details.error_handlers,
                'validation_checks': func_details.validation_checks,
                'dependencies': func_details.function_calls
            }

        return enhanced_metadata

    def _find_error_handlers(self, tree: ast.AST) -> List[str]:
        handlers = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if isinstance(handler.type, ast.Name):
                        handlers.append(handler.type.id)
        return handlers

    def _find_validations(self, tree: ast.AST) -> List[str]:
        validations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                test = ast.unparse(node.test)
                validations.append(test)
        return validations

    # 1. Replace the _calculate_complexity method in the IOAnalyzer class with this enhanced version:

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity with comprehensive rules"""
        complexity = 1  # Start with base complexity

        # For debugging
        control_structures_found = []

        for node in ast.walk(tree):
            # Control flow statements
            if isinstance(node, ast.If):
                complexity += 1
                control_structures_found.append("if")

                # Count elif branches (they appear as If nodes in orelse)
                if node.orelse:
                    for orelse_item in node.orelse:
                        if isinstance(orelse_item, ast.If):
                            complexity += 1
                            control_structures_found.append("elif")

            elif isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
                complexity += 1
                control_structures_found.append("for/asyncfor")

            elif isinstance(node, ast.While):
                complexity += 1
                control_structures_found.append("while")

            # Try blocks add complexity for each handler
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
                control_structures_found.append(f"try with {len(node.handlers)} handlers")

            # Boolean operations can create branch points
            elif isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
                complexity += len(node.values) - 1
                control_structures_found.append(f"boolean op with {len(node.values)} values")

            # Conditional expressions (ternary operators)
            elif isinstance(node, ast.IfExp):
                complexity += 1
                control_structures_found.append("ternary if")

            # List/dict/set comprehensions with conditionals
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                for generator in node.generators:
                    complexity += len(generator.ifs)
                    if generator.ifs:
                        control_structures_found.append(f"comprehension with {len(generator.ifs)} conditions")

        # Print debug info if control structures were found
        if control_structures_found:
            print(f"DEBUG: Found control structures: {control_structures_found}, complexity = {complexity}")

        return complexity

    # 2. Replace the analyze_function method with this enhanced version:

    def analyze_function(self, function) -> FunctionAnalysis:
        """Analyze a function with improved source extraction and complexity calculation"""
        try:
            # Get function source and create AST
            source = inspect.getsource(function)

            # Clean up source indentation
            lines = source.split('\n')
            if lines:
                # Calculate the indentation of the first line
                indent = len(lines[0]) - len(lines[0].lstrip())
                # Remove that indentation from all lines
                source = '\n'.join(line[indent:] if len(line) >= indent else line for line in lines)

            # Parse the clean source into an AST for analysis
            try:
                func_tree = ast.parse(source)
                print(f"DEBUG: Successfully parsed function source ({len(source)} chars)")
            except SyntaxError as e:
                print(f"DEBUG: Syntax error parsing function source: {e}")
                # Try a more forgiving approach
                func_tree = ast.parse("\n".join(line for line in source.split('\n') if line.strip()))
                print(f"DEBUG: Parsed with stripped empty lines")

            # Extract function signature
            signature = inspect.signature(function)

            # Extract input types
            input_types = {}
            for name, param in signature.parameters.items():
                if name != 'self':  # Skip self parameter for methods
                    try:
                        if param.annotation != inspect.Parameter.empty:
                            if hasattr(param.annotation, '__name__'):
                                type_name = param.annotation.__name__
                            else:
                                type_name = str(param.annotation).replace('typing.', '')
                        else:
                            type_name = 'Any'
                    except AttributeError:
                        type_name = 'Any'
                    input_types[name] = type_name

            # Extract output type
            try:
                if signature.return_annotation != inspect.Parameter.empty:
                    if hasattr(signature.return_annotation, '__name__'):
                        output_type = signature.return_annotation.__name__
                    else:
                        output_type = str(signature.return_annotation).replace('typing.', '')
                else:
                    output_type = 'Any'
            except AttributeError:
                output_type = 'Any'

            # Calculate complexity with detailed debug info
            complexity = self._calculate_complexity(func_tree)

            # Find error handlers, validations, function calls
            error_handlers = self._find_error_handlers(func_tree)
            validation_checks = self._find_validations(func_tree)
            function_calls = self._find_function_calls(func_tree)

            # Create analysis result
            analysis = FunctionAnalysis(
                input_types=input_types,
                output_type=output_type,
                error_handlers=error_handlers,
                validation_checks=validation_checks,
                complexity=complexity,
                function_calls=function_calls
            )

            # Add additional analyses
            analysis.data_dependencies = self._find_data_dependencies(func_tree)
            analysis.transforms = self._find_transformations(func_tree)

            return analysis

        except Exception as e:
            print(f"DEBUG: Function analysis failed: {str(e)}")
            return FunctionAnalysis(
                input_types={},
                output_type='Any',
                error_handlers=[],
                validation_checks=[],
                complexity=1,
                function_calls=[],
                data_dependencies=[],
                transforms=[]
            )

    def _find_function_calls(self, tree: ast.AST) -> List[str]:
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(f"{ast.unparse(node.func.value)}.{node.func.attr}")
        return list(set(calls))

    def _find_data_dependencies(self, tree: ast.AST) -> List[str]:
        deps = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                deps.append(node.id)
        return list(set(deps))

    def _find_transformations(self, tree: ast.AST) -> List[str]:
        transforms = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                transforms.append(ast.unparse(node))
        return transforms

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        # Add these lines at the beginning
        file_key = str(file_path)
        if file_key in self._currently_analyzing:
            logger.debug(f"Already analyzing {file_path}, skipping")
            return {}

        self._currently_analyzing.add(file_key)

        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return {}

            # Skip __init__.py files
            if file_path.name == '__init__.py':
                logger.info(f"Skipping {file_path} - __init__ file")
                return {}

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    source = f.read()

                tree = ast.parse(source)
                has_functions = any(isinstance(node, (ast.FunctionDef, ast.ClassDef)) for node in ast.walk(tree))
                if not has_functions:
                    logger.info(f"Skipping {file_path} - no functions or classes found")
                    return {}

                project_root = file_path.parent.parent
                if str(project_root) not in sys.path:
                    sys.path.insert(0, str(project_root))

                module_namespace = {
                    'Path': Path,
                    'Dict': Dict,
                    'List': List,
                    'Optional': Optional,
                    'Any': Any,
                    'Set': Set,
                    'ET': ET,
                    'validator': lambda *args, **kwargs: lambda x: x,
                    'field_validator': lambda *args, **kwargs: lambda x: x,
                    'ioe': lambda x: x,
                    '__file__': str(file_path),
                    '__name__': '__main__',
                    'field': lambda *args, **kwargs: lambda x: x,
                    'BaseModel': type('BaseModel', (), {
                        'model_config': {},
                        'decode_json_strings': classmethod(lambda cls, v: v)
                    }),
                    'property': property,
                    'dataclass': lambda x: x,
                    'Field': lambda *args, **kwargs: None
                }

                try:
                    mod = compile(tree, filename=str(file_path), mode='exec')
                    exec(mod, module_namespace)
                except Exception as e:
                    logger.debug(f"Module level execution failed: {e}")

                analyses = {}

                # Track processed function names to avoid duplicates
                processed_functions = set()

                # First process top-level functions
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and is_user_defined(node, source):
                        try:
                            # Get the function name
                            func_name = node.name
                            if func_name in processed_functions:
                                continue

                            processed_functions.add(func_name)
                            print(f"DEBUG: Analyzing function {func_name}")

                            # Extract only this function's source
                            func_source = ast.get_source_segment(source, node)
                            if func_source:
                                # Get the function's lines
                                lines = func_source.split('\n')
                                # Calculate indentation of first line
                                indent = len(lines[0]) - len(lines[0].lstrip())
                                # Remove indentation from all lines
                                unindented_source = '\n'.join(
                                    line[indent:] if len(line) >= indent else line
                                    for line in lines
                                )

                                # Print first few lines of the function for debugging
                                print(f"DEBUG: Function {func_name} source start (first 5 lines):")
                                for i, line in enumerate(unindented_source.split('\n')[:5]):
                                    print(f"  {i + 1}: {line}")

                                # Create AST for just this function
                                try:
                                    func_tree = ast.parse(unindented_source)
                                    print(
                                        f"DEBUG: Successfully parsed function {func_name} source ({len(unindented_source)} chars)")

                                    # Print AST structure for debugging
                                    control_nodes = [n for n in ast.walk(func_tree) if
                                                     isinstance(n, (ast.If, ast.For, ast.While, ast.Try))]
                                    if control_nodes:
                                        print(f"DEBUG: Control structures in {func_name}:")
                                        for i, node in enumerate(control_nodes):
                                            print(f"  Control node {i + 1}: {type(node).__name__}")
                                    else:
                                        print(f"DEBUG: No control structures found in {func_name}")
                                except SyntaxError as e:
                                    print(f"DEBUG: Syntax error parsing function {func_name}: {e}")
                                    # Try with stripped empty lines as fallback
                                    unindented_source = '\n'.join(
                                        line for line in unindented_source.split('\n') if line.strip())
                                    func_tree = ast.parse(unindented_source)
                                    print(f"DEBUG: Parsed {func_name} with stripped empty lines")

                                # Get the function object
                                func = module_namespace.get(func_name)
                                if func is None:
                                    print(f"DEBUG: Function object for {func_name} not found in namespace")

                                    # Create a placeholder function for analysis
                                    def placeholder_function(*args, **kwargs):
                                        pass

                                    placeholder_function.__name__ = func_name
                                    func = placeholder_function

                                # Use our custom AST-based analysis instead of function object analysis
                                # This will use the proper function source code and tree
                                analysis = self.analyze_function_ast(func, func_tree, unindented_source)
                                analyses[func_name] = analysis
                            else:
                                print(f"DEBUG: Could not extract source for function {func_name}")
                        except Exception as e:
                            logger.error(f"Failed to analyze function {node.name}: {e}")
                            print(f"DEBUG: Error analyzing function {node.name}: {e}")

                # Now process class methods
                for class_node in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:
                    try:
                        class_name = class_node.name
                        print(f"DEBUG: Analyzing class {class_name}")

                        # Get indentation for the class
                        class_source = ast.get_source_segment(source, class_node)
                        class_lines = class_source.split('\n')
                        class_indent = len(class_lines[0]) - len(class_lines[0].lstrip())

                        # Process each method in the class
                        for method_node in [n for n in class_node.body if isinstance(n, ast.FunctionDef)]:
                            try:
                                method_name = method_node.name
                                full_method_name = f"{class_name}.{method_name}"

                                # Skip if already processed to avoid duplicates
                                if method_name in processed_functions or full_method_name in processed_functions:
                                    continue

                                processed_functions.add(full_method_name)
                                print(f"DEBUG: Analyzing method {full_method_name}")

                                # Extract method source
                                method_source = ast.get_source_segment(source, method_node)
                                if method_source:
                                    # Get method lines
                                    method_lines = method_source.split('\n')
                                    # Calculate method indentation
                                    method_indent = len(method_lines[0]) - len(method_lines[0].lstrip())
                                    # Remove indentation (accounting for class indent + method indent)
                                    unindented_source = '\n'.join(
                                        line[method_indent:] if len(line) >= method_indent else line
                                        for line in method_lines
                                    )

                                    print(f"DEBUG: Method {full_method_name} source start (first 5 lines):")
                                    for i, line in enumerate(unindented_source.split('\n')[:5]):
                                        print(f"  {i + 1}: {line}")

                                    # Create AST for just this method
                                    try:
                                        method_tree = ast.parse(unindented_source)
                                        print(
                                            f"DEBUG: Successfully parsed method {full_method_name} source ({len(unindented_source)} chars)")

                                        # Print AST structure for debugging
                                        control_nodes = [n for n in ast.walk(method_tree) if
                                                         isinstance(n, (ast.If, ast.For, ast.While, ast.Try))]
                                        if control_nodes:
                                            print(f"DEBUG: Control structures in {full_method_name}:")
                                            for i, node in enumerate(control_nodes):
                                                print(f"  Control node {i + 1}: {type(node).__name__}")
                                        else:
                                            print(f"DEBUG: No control structures found in {full_method_name}")
                                    except SyntaxError as e:
                                        print(f"DEBUG: Syntax error parsing method {full_method_name}: {e}")
                                        continue

                                    # Create a placeholder function for analysis
                                    def placeholder_method(*args, **kwargs):
                                        pass

                                    placeholder_method.__name__ = method_name

                                    # Use our custom AST-based analysis for the method
                                    analysis = self.analyze_function_ast(placeholder_method, method_tree,
                                                                         unindented_source)
                                    analyses[full_method_name] = analysis
                                else:
                                    print(f"DEBUG: Could not extract source for method {full_method_name}")
                            except Exception as e:
                                logger.error(f"Failed to analyze method {class_name}.{method_node.name}: {e}")
                                print(f"DEBUG: Error analyzing method {class_name}.{method_node.name}: {e}")
                    except Exception as e:
                        logger.error(f"Failed to analyze class {class_node.name}: {e}")
                        print(f"DEBUG: Error analyzing class {class_node.name}: {e}")

                # Process local functions defined in module-level code (not in classes or functions)
                # This would require deeper inspection of function bodies to find nested function defs

                return analyses

            except Exception as e:
                logger.error(f"Failed to parse {file_path}: {e}")
                return {}
        finally:
            # Always remove from the set when done
            self._currently_analyzing.discard(file_key)

    # Add a new method to analyze functions based on AST
    def analyze_function_ast(self, function, func_tree: ast.AST, source: str) -> FunctionAnalysis:
        """Analyze a function with AST-based source analysis"""
        try:
            func_name = function.__name__

            # Extract function signature
            signature = inspect.signature(function)

            # Extract input types
            input_types = {}
            for name, param in signature.parameters.items():
                if name != 'self':  # Skip self parameter for methods
                    try:
                        if param.annotation != inspect.Parameter.empty:
                            if hasattr(param.annotation, '__name__'):
                                type_name = param.annotation.__name__
                            else:
                                type_name = str(param.annotation).replace('typing.', '')
                        else:
                            type_name = 'Any'
                    except AttributeError:
                        type_name = 'Any'
                    input_types[name] = type_name

            # Extract output type
            try:
                if signature.return_annotation != inspect.Parameter.empty:
                    if hasattr(signature.return_annotation, '__name__'):
                        output_type = signature.return_annotation.__name__
                    else:
                        output_type = str(signature.return_annotation).replace('typing.', '')
                else:
                    output_type = 'Any'
            except AttributeError:
                output_type = 'Any'

            # Calculate complexity with detailed debug info
            print(f"DEBUG: Calculating complexity for {func_name}")
            complexity = self._calculate_complexity(func_tree)
            print(f"DEBUG: Final complexity for {func_name}: {complexity}")

            # Find error handlers, validations, function calls
            error_handlers = self._find_error_handlers(func_tree)
            validation_checks = self._find_validations(func_tree)
            function_calls = self._find_function_calls(func_tree)

            print(
                f"DEBUG: Function {func_name} analysis complete: complexity={complexity}, error_handlers={len(error_handlers)}, validations={len(validation_checks)}, calls={len(function_calls)}")

            # Create analysis result
            analysis = FunctionAnalysis(
                input_types=input_types,
                output_type=output_type,
                error_handlers=error_handlers,
                validation_checks=validation_checks,
                complexity=complexity,
                function_calls=function_calls
            )

            # Add additional analyses
            analysis.data_dependencies = self._find_data_dependencies(func_tree)
            analysis.transforms = self._find_transformations(func_tree)

            return analysis

        except Exception as e:
            print(f"DEBUG: Function AST analysis failed for {function.__name__}: {str(e)}")
            return FunctionAnalysis(
                input_types={},
                output_type='Any',
                error_handlers=[],
                validation_checks=[],
                complexity=1,
                function_calls=[],
                data_dependencies=[],
                transforms=[]
            )


def print_analysis_results(results: Dict[str, Any]):
    """Print analysis results, handling both function and data analysis"""
    for file_path, file_analyses in results.items():
        print(f"\n{'=' * 50}")
        print(f"File: {file_path}")
        print(f"{'=' * 50}")

        if not file_analyses:
            print("No analyses found.")
            continue

        # Handle different sections of analysis
        if 'functions' in file_analyses:
            print("\nFunction Analysis:")
            for func_name, func_analysis in file_analyses['functions'].items():
                print(f"\nFunction: {func_name}")
                print(f"  Input Types: {func_analysis.input_types}")
                print(f"  Output Type: {func_analysis.output_type}")
                print(f"  Complexity: {func_analysis.complexity}")

                if func_analysis.error_handlers:
                    print(f"  Error Handlers: {func_analysis.error_handlers}")

                if func_analysis.validation_checks:
                    print("  Validation Checks:")
                    for check in func_analysis.validation_checks:
                        print(f"    - {check}")

                if func_analysis.function_calls:
                    print("  Function Calls:")
                    for call in func_analysis.function_calls:
                        print(f"    - {call}")
                print("-" * 40)

        if 'input_analysis' in file_analyses:
            print("\nInput Analysis:")
            input_analysis = file_analyses['input_analysis']
            print(f"  Schema: {input_analysis['schema']}")
            print(f"  Field Types: {input_analysis['field_types']}")
            if input_analysis['validations']:
                print("  Validations:")
                for validation in input_analysis['validations']:
                    print(f"    - {validation}")
            print("-" * 40)

        if 'output_analysis' in file_analyses:
            print("\nOutput Analysis:")
            output_analysis = file_analyses['output_analysis']
            print(f"  Schema: {output_analysis['schema']}")
            print(f"  Field Types: {output_analysis['field_types']}")
            print("-" * 40)

        if 'flow_analysis' in file_analyses:
            print("\nFlow Analysis:")
            flow = file_analyses['flow_analysis']
            if flow['critical_paths']:
                print("  Critical Paths:")
                for path in flow['critical_paths']:
                    print(f"    - {path}")
            if flow['dependencies']:
                print("  Dependencies:")
                for func, deps in flow['dependencies'].items():
                    print(f"    {func} -> {deps}")
            print("-" * 40)


def is_user_defined(node, source):
    """Check if a function is user-defined (not imported)."""
    try:
        source_segment = ast.get_source_segment(source, node)
        if not source_segment:
            return False

        # Check if function has a decorator that might indicate it's not user-defined
        if hasattr(node, 'decorator_list') and node.decorator_list:
            for decorator in node.decorator_list:
                decorator_name = None
                if isinstance(decorator, ast.Name):
                    decorator_name = decorator.id
                elif isinstance(decorator, ast.Attribute):
                    decorator_name = decorator.attr
                elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                    decorator_name = decorator.func.id

                if decorator_name in ['staticmethod', 'classmethod', 'property']:
                    return True  # These are common Python decorators

                # Skip functions with custom decorators that might indicate framework functions
                if decorator_name and decorator_name.startswith('_'):
                    return False

        # Simplistic but effective for most cases
        return not node.name.startswith('_') or node.name in ['__init__', '__call__']
    except Exception:
        return False


def main():
    try:
        # Parse command line args for config
        config_path = None
        if len(sys.argv) > 2 and sys.argv[1] == "--config":
            config_path = sys.argv[2]

        # Default target file
        target_file = Path(r"C:\Users\samha\OneDrive\Desktop\EQ_SUBMITTED_AUTO_PDM\main_consolidated.py")

        # Get target file from config if provided
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    base_dir = config.get('base_dir', '')
                    target_file_path = config.get('io_analyzer', {}).get('target_file', '')
                    if target_file_path and '${base_dir}' in target_file_path:
                        target_file = Path(target_file_path.replace('${base_dir}', base_dir))
            except Exception as e:
                logger.error(f"Error loading config: {e}")

        if not target_file.exists():
            logger.error(f"Target file not found: {target_file}")
            return 1

        io_analyzer = IOAnalyzer()
        results = {}

        # HOOK INTO THE ETL PIPELINE OUTPUT
        # Save original functions that will be patched
        original_builtins_print = builtins.print
        original_sys_stdout_write = sys.stdout.write

        # Define a custom print function that filters out detailed file content
        def filtered_print(*args, **kwargs):
            if len(args) == 0:
                original_builtins_print(*args, **kwargs)
                return

            text = ' '.join(str(arg) for arg in args)
            # Allow progress messages to pass through
            if any(msg in text for msg in [
                "ETL process started",
                "Saved data to",
                "JSON Pydantic model generated",
                "XML Pydantic model generated",
                "Combined output saved",
                "Validating output data",
                "JSON output contains",
                "All JSON records",
                "XML output contains",
                "All XML records",
                "Performance metrics",
                "Unit test preparation data saved",
                "Process finished",
                "Failed to analyze",
                "Schema Processing",
                "JSON Processing",
                "XML Processing",
                "Model Generation",
                "Data Validation",
                "Output Verification",
                "Total execution time"
            ]):
                original_builtins_print(*args, **kwargs)
            # Suppress file content sections but show headers
            elif "Output Files:" in text:
                original_builtins_print("Output Files: [Content suppressed]", **kwargs)
            elif text.startswith("File: json_n_flatout.json"):
                original_builtins_print("File: json_n_flatout.json [Content suppressed]", **kwargs)
            elif text.startswith("File: xml_n_flatout.json"):
                original_builtins_print("File: xml_n_flatout.json [Content suppressed]", **kwargs)
            elif text.startswith("Pydantic Model: item_n.py"):
                original_builtins_print("Pydantic Model: item_n.py [Content suppressed]", **kwargs)
            elif text.startswith("Pydantic Model: item_n_xml.py"):
                original_builtins_print("Pydantic Model: item_n_xml.py [Content suppressed]", **kwargs)
            # Suppress content lines that contain large amounts of data
            elif text.startswith("  {") or text.startswith("  [") or text.startswith(
                    "  \"") or "additional_data_blob" in text:
                pass  # Suppress these lines completely
            else:
                original_builtins_print(*args, **kwargs)

        # Define a custom stdout.write function
        def filtered_write(text):
            # Filter large chunks of data
            if (len(text) > 200 and (
                    ("_key" in text and "type" in text) or
                    ("additional_data_blob" in text) or
                    ("properties__" in text) or
                    ("class JsonModel" in text)
            )):
                pass  # Suppress large data chunks
            else:
                original_sys_stdout_write(text)

        # Replace the print and write functions with our filtered versions
        builtins.print = filtered_print
        sys.stdout.write = filtered_write

        # Analyze the file
        try:
            print("ETL process started")
            file_analysis = io_analyzer.analyze_file(target_file)

            # Prepare structured report
            results[str(target_file)] = {
                'functions': {
                    func_name: {
                        'input_types': analysis.input_types,
                        'output_type': analysis.output_type,
                        'error_handlers': analysis.error_handlers,
                        'validation_checks': analysis.validation_checks,
                        'complexity': analysis.complexity,
                        'function_calls': analysis.function_calls,
                        'test_generation_hints': {
                            'path_types': [param for param, type_name in analysis.input_types.items() if
                                           'path' in param.lower()],
                            'xml_types': [param for param, type_name in analysis.input_types.items() if
                                          'xml' in param.lower()],
                            'critical_complexity': analysis.complexity > 10,
                            'error_prone': len(analysis.error_handlers) > 0
                        }
                    } for func_name, analysis in file_analysis.items()
                }
            }

        except Exception as e:
            logger.error(f"Failed to analyze {target_file}: {e}")
            print(f"Failed to analyze {target_file}: {e}")
            traceback.print_exc()

        # Save results in a clean, focused JSON
        output_path = Path('unit_test_preparation.json')
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, cls=CustomJSONEncoder)

        print(f"\nUnit test preparation data saved to {output_path}")

        # Restore original print and write functions before displaying JSON
        builtins.print = original_builtins_print
        sys.stdout.write = original_sys_stdout_write

        # Display the contents of the unit_test_preparation.json file
        print("\n" + "=" * 50)
        print("CONTENTS OF unit_test_preparation.json:")
        print("=" * 50)

        try:
            with open(output_path, 'r') as f:
                json_content = f.read()
                print(json_content)
        except Exception as e:
            print(f"Error reading JSON file: {e}")

        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    main()
################################################################################
#   current console output :  io_analyzer.py
#################################################################################
# (.venv) PS C:\Users\samha\PycharmProjects\EQ_FINAL_03_04> python io_analyzer.py --config C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\consolidated_config.json
# ETL process started
# ETL process started
# Saved data to C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\etl_pipeline\output\data\json_n_flatout.json
# Saved data to C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\etl_pipeline\output\data\xml_n_flatout.json
# JSON Pydantic model generated successfully
# XML Pydantic model generated successfully
# Combined output saved to C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\combined_output.json
# Validating output data...
# JSON output contains 3 records
# All JSON records have required fields
# XML output contains 3 records
# All XML records have required fields
# Output Files: [Content suppressed]
# ============
#
# File: json_n_flatout.json
# -------------------------
#
#
# File: xml_n_flatout.json
# ------------------------
#
# Pydantic Model: item_n.py
# -------------------------
#
#
# Pydantic Model: item_n_xml.py
# -----------------------------
# Performance metrics:
#   Schema Processing: 0.0010 seconds (3.6%)
#   JSON Processing: 0.0020 seconds (7.3%)
#   XML Processing: 0.0035 seconds (12.7%)
#   Model Generation: 0.0000 seconds (0.0%)
#   Data Validation: 0.0150 seconds (54.5%)
#   Output Verification: 0.0030 seconds (10.9%)
# Total execution time: 0.0275 seconds
# Process finished
# Failed to analyze function check_path: no binding for nonlocal 'path_exists' found (main_consolidated.py, line 2)
#
# Unit test preparation data saved to unit_test_preparation.json
#
# ==================================================
# CONTENTS OF unit_test_preparation.json:
# ==================================================
# (.venv) PS C:\Users\samha\PycharmProjects\EQ_FINAL_03_04> python io_analyzer.py --config C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\consolidated_config.json
# ETL process started
# ETL process started
# Saved data to C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\etl_pipeline\output\data\json_n_flatout.json
# Saved data to C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\etl_pipeline\output\data\xml_n_flatout.json
# JSON Pydantic model generated successfully
# XML Pydantic model generated successfully
# Combined output saved to C:\Users\samha\PycharmProjects\EQ_FINAL_03_04\combined_output.json
# Validating output data...
# JSON output contains 3 records
# All JSON records have required fields
# XML output contains 3 records
# All XML records have required fields
# Output Files: [Content suppressed]
# ============
#
# File: json_n_flatout.json
# -------------------------
#
#
# File: xml_n_flatout.json
# ------------------------
#
# Pydantic Model: item_n.py
# -------------------------
#
#
# Pydantic Model: item_n_xml.py
# -----------------------------
# Performance metrics:
#   Schema Processing: 0.0000 seconds (0.0%)
#   JSON Processing: 0.0025 seconds (9.4%)
#   XML Processing: 0.0030 seconds (11.4%)
#   Model Generation: 0.0010 seconds (3.9%)
#   Data Validation: 0.0138 seconds (52.5%)
#   Output Verification: 0.0030 seconds (11.4%)
# Total execution time: 0.0264 seconds
# Process finished
# Failed to analyze function check_path: no binding for nonlocal 'path_exists' found (main_consolidated.py, line 2)
#
# Unit test preparation data saved to unit_test_preparation.json
#
# ==================================================
# CONTENTS OF unit_test_preparation.json:
# ==================================================
# {
#   "C:\\Users\\samha\\PycharmProjects\\EQ_FINAL_03_04\\main_consolidated.py": {
#     "functions": {
#       "setup_logging": {
#         "input_types": {
#           "silent": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "print_with_checkmark": {
#         "input_types": {
#           "message": "str",
#           "success": "bool"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "print_with_tabs": {
#         "input_types": {
#           "label": "str",
#           "value": "str"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "verify_output_files": {
#         "input_types": {
#           "base_dir": "str",
#           "config": "dict"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "validate_network_path": {
#         "input_types": {
#           "path": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "ensure_directory_exists": {
#         "input_types": {
#           "directory_path": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "directory_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "save_with_retry": {
#         "input_types": {
#           "data": "Any",
#           "file_path": "Any",
#           "save_function": "Any",
#           "max_retries": "Any",
#           "initial_delay": "Any",
#           "log_success": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "file_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "load_file_with_retry": {
#         "input_types": {
#           "file_path": "Any",
#           "max_retries": "Any",
#           "initial_delay": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "file_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "save_combined_output": {
#         "input_types": {
#           "json_data": "Any",
#           "xml_data": "Any",
#           "model_code": "Any",
#           "output_path": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "output_path"
#           ],
#           "xml_types": [
#             "xml_data"
#           ],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "track_step": {
#         "input_types": {
#           "step_times": "Any",
#           "step_name": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "create_save_function": {
#         "input_types": {
#           "etl_processor": "Any",
#           "silent_mode": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "main": {
#         "input_types": {
#           "config_path": "str",
#           "args": "Namespace"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "config_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "format": {
#         "input_types": {
#           "record": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "__init__": {
#         "input_types": {
#           "config": "Dict"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "ensure_directories": {
#         "input_types": {
#           "paths": "Dict"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "paths"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "get_path": {
#         "input_types": {
#           "key": "str"
#         },
#         "output_type": "Path",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "get_config_value": {
#         "input_types": {
#           "key": "str",
#           "default": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "get_input_file_path": {
#         "input_types": {
#           "file_key": "str"
#         },
#         "output_type": "Path",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "get_output_file_path": {
#         "input_types": {
#           "category": "str",
#           "file_key": "str"
#         },
#         "output_type": "Path",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "get_app_paths": {
#         "input_types": {
#           "base_dir": "Optional"
#         },
#         "output_type": "Dict",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "process_data": {
#         "input_types": {
#           "file_path": "Path",
#           "data_type": "str",
#           "schema_keys": "Set"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "file_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "process_json_data": {
#         "input_types": {
#           "json_path": "Path"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "json_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "process_xml_data": {
#         "input_types": {
#           "xml_path": "Path",
#           "schema_keys": "Set"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "xml_path"
#           ],
#           "xml_types": [
#             "xml_path"
#           ],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "process_collection_n": {
#         "input_types": {
#           "data": "List"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "process_xml_root": {
#         "input_types": {
#           "root": "Element",
#           "schema_keys": "Set"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "xml_to_dict": {
#         "input_types": {
#           "element": "Element",
#           "parent_key": "str"
#         },
#         "output_type": "Dict",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "transform_value": {
#         "input_types": {
#           "value": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "parse_element_text": {
#         "input_types": {
#           "element": "Element",
#           "parent_key": "str"
#         },
#         "output_type": "Dict",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "flatten_data": {
#         "input_types": {
#           "data": "Any",
#           "parent_key": "str"
#         },
#         "output_type": "Dict",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "process_xml_content": {
#         "input_types": {
#           "root": "Element",
#           "schema_keys": "Set"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "create_matched_data": {
#         "input_types": {
#           "features": "List",
#           "schema_keys": "Set"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "strip_key_prefixes": {
#         "input_types": {
#           "data": "Dict"
#         },
#         "output_type": "Dict",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "save_json_file": {
#         "input_types": {
#           "data": "List",
#           "output_path": "Path"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "output_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "load_schema": {
#         "input_types": {
#           "schema_path": "str"
#         },
#         "output_type": "Dict",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "schema_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "generate_pydantic_model": {
#         "input_types": {
#           "data": "Dict",
#           "output_path": "Path",
#           "model_name": "str"
#         },
#         "output_type": "str",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "output_path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "get_schema_keys": {
#         "input_types": {
#           "schema_data": "List"
#         },
#         "output_type": "List",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "resolve_path": {
#         "input_types": {
#           "path": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "save_data": {
#         "input_types": {
#           "data": "Any",
#           "path": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       },
#       "save_combined_data": {
#         "input_types": {
#           "data": "Any",
#           "path": "Any"
#         },
#         "output_type": "Any",
#         "error_handlers": [],
#         "validation_checks": [],
#         "complexity": 1,
#         "function_calls": [
#           "sys.stderr.reconfigure",
#           "record.getMessage",
#           "logging.getLogger",
#           "sys.stdout.reconfigure"
#         ],
#         "test_generation_hints": {
#           "path_types": [
#             "path"
#           ],
#           "xml_types": [],
#           "critical_complexity": false,
#           "error_prone": false
#         }
#       }
#     }
#   }
# }
# (.venv) PS C:\Users\samha\PycharmProjects\EQ_FINAL_03_04>
