"""
Tests demonstrating advanced pytest features.
"""
import pytest
from data_processor import DataProcessor, ProcessingMode

# Test data for parameterization
VALID_INPUTS = [
    ([1, 2, 3], [1.0, 2.0, 3.0]),
    (["1", "2", "3"], [1.0, 2.0, 3.0]),
    (["10%", "20%", "30%"], [0.1, 0.2, 0.3]),
]

INVALID_INPUTS = [
    ["invalid", 1, 2],
    ["10", "invalid", "30"],
    ["abc", "def", "ghi"],
]

@pytest.mark.data_processing
class TestDataProcessor:
    """Test class demonstrating different pytest features."""
    
    @pytest.mark.parametrize("input_data,expected", VALID_INPUTS)
    def test_process_numbers_valid(self, input_data, expected):
        """Test processing valid numbers with parameterization."""
        processor = DataProcessor()
        result = processor.process_numbers(input_data)
        assert result == expected
    
    @pytest.mark.parametrize("input_data", INVALID_INPUTS)
    def test_process_numbers_invalid_strict(self, input_data):
        """Test that invalid input raises ValueError in strict mode."""
        processor = DataProcessor(ProcessingMode.STRICT)
        with pytest.raises(ValueError):
            processor.process_numbers(input_data)
    
    @pytest.mark.parametrize("input_data", INVALID_INPUTS)
    def test_process_numbers_invalid_lenient(self, input_data):
        """Test that invalid input is handled in lenient mode."""
        processor = DataProcessor(ProcessingMode.LENIENT)
        result = processor.process_numbers(input_data)
        # Should only include valid numbers
        assert all(isinstance(x, float) for x in result)
    
    @pytest.mark.slow
    def test_calculate_statistics_all_modes(self, processor_mode, sample_datasets):
        """
        Test statistics calculation with different modes.
        Marked as slow because it processes multiple datasets.
        """
        processor = DataProcessor(processor_mode)
        
        for dataset in sample_datasets:
            try:
                stats = processor.calculate_statistics(dataset)
                if stats is not None:
                    assert isinstance(stats, dict)
                    assert all(key in stats for key in ["count", "sum", "average", "min", "max"])
                    assert stats["count"] > 0
                    assert stats["min"] <= stats["max"]
            except ValueError:
                # Should only raise in STRICT mode
                assert processor_mode == ProcessingMode.STRICT
    
    @pytest.mark.parametrize("input_data,expected_count", [
        ([1, 2, 3], 3),
        ([], None),
        (["10%", "20%"], 2),
    ])
    def test_statistics_count(self, input_data, expected_count):
        """Test the count field in statistics with different inputs."""
        processor = DataProcessor()
        stats = processor.calculate_statistics(input_data)
        
        if expected_count is None:
            assert stats is None
        else:
            assert stats["count"] == expected_count

# Custom marker usage example
pytestmark = pytest.mark.data_processing