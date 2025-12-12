"""
Pytest Configuration

Shared fixtures and configuration for tests.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

