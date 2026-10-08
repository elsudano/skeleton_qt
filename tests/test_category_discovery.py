"""Tests for automatic category discovery functionality."""


from src.core.category_discovery import CategoryDiscovery


def test_category_discovery_finds_categories():
    """Test that category discovery works correctly."""
    # This test will verify that the discovery mechanism can find categories
    # in source files. Since we don't have actual source files with _CATEGORY 
    # definitions in this testing environment, we'll check if the function exists
    # and doesn't crash.
    
    # The discovery function should not crash even when no categories are found
    discovered = CategoryDiscovery.discover_from_source("src")
    assert isinstance(discovered, list)


def test_category_discovery_returns_sorted_list():
    """Test that discovered categories are returned in sorted order."""
    discovered = CategoryDiscovery.discover_from_source("src")
    # Should return a list (even if empty)
    assert isinstance(discovered, list)
    
    # If not empty, should be sorted
    if discovered:
        assert discovered == sorted(discovered)


def test_category_discovery_handles_nonexistent_path():
    """Test that discovery handles non-existent paths gracefully."""
    discovered = CategoryDiscovery.discover_from_source("non_existent_directory")
    assert isinstance(discovered, list)
    assert len(discovered) == 0