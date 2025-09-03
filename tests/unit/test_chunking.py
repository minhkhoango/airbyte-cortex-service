# Pylance strict mode
import pytest

from cortex_service.chunking import chunk_by_fixed_size, chunk_by_paragraph


class TestChunkByParagraph:
    """Test suite for chunk_by_paragraph function."""

    def test_chunk_by_paragraph_success(self) -> None:
        """Tests that paragraph chunking splits correctly."""
        text = "First paragraph.\n\nSecond paragraph."
        chunks = chunk_by_paragraph(text, min_chunk_size=1)
        assert len(chunks) == 2
        assert chunks[0] == "First paragraph."
        assert chunks[1] == "Second paragraph."

    def test_chunk_by_paragraph_min_size_filter(self) -> None:
        """Tests the min_chunk_size filter."""
        text = "Short.\n\nThis is a much longer paragraph."
        chunks = chunk_by_paragraph(text, min_chunk_size=10)
        assert len(chunks) == 1
        assert chunks[0] == "This is a much longer paragraph."

    def test_chunk_by_paragraph_empty_text(self) -> None:
        """Tests handling of empty text."""
        text = ""
        chunks = chunk_by_paragraph(text, min_chunk_size=1)
        assert len(chunks) == 0

    def test_chunk_by_paragraph_whitespace_only(self) -> None:
        """Tests handling of whitespace-only text."""
        text = "   \n\n\t\n  "
        chunks = chunk_by_paragraph(text, min_chunk_size=1)
        assert len(chunks) == 0

    def test_chunk_by_paragraph_single_paragraph(self) -> None:
        """Tests single paragraph without line breaks."""
        text = "This is a single paragraph without any line breaks."
        chunks = chunk_by_paragraph(text, min_chunk_size=1)
        assert len(chunks) == 1
        assert chunks[0] == "This is a single paragraph without any line breaks."

    def test_chunk_by_paragraph_multiple_line_breaks(self) -> None:
        """Tests multiple consecutive line breaks."""
        text = "First.\n\n\n\nSecond.\n\n\nThird."
        chunks = chunk_by_paragraph(text, min_chunk_size=1)
        assert len(chunks) == 3
        assert chunks[0] == "First."
        assert chunks[1] == "Second."
        assert chunks[2] == "Third."

    def test_chunk_by_paragraph_high_min_size(self) -> None:
        """Tests when min_chunk_size is higher than all paragraphs."""
        text = "Short.\n\nAlso short.\n\nTiny."
        chunks = chunk_by_paragraph(text, min_chunk_size=20)
        assert len(chunks) == 0

    def test_chunk_by_paragraph_exact_min_size(self) -> None:
        """Tests when paragraph length exactly matches min_chunk_size."""
        text = "Exactly 10.\n\nLonger paragraph here."
        chunks = chunk_by_paragraph(text, min_chunk_size=10)
        assert len(chunks) == 2
        assert chunks[0] == "Exactly 10."
        assert chunks[1] == "Longer paragraph here."

    def test_chunk_by_paragraph_zero_min_size(self) -> None:
        """Tests with zero min_chunk_size."""
        text = "First.\n\nSecond.\n\nThird."
        chunks = chunk_by_paragraph(text, min_chunk_size=0)
        assert len(chunks) == 3

    def test_chunk_by_paragraph_negative_min_size(self) -> None:
        """Tests with negative min_chunk_size."""
        text = "First.\n\nSecond.\n\nThird."
        chunks = chunk_by_paragraph(text, min_chunk_size=-5)
        assert len(chunks) == 3


class TestChunkByFixedSize:
    """Test suite for chunk_by_fixed_size function."""

    def test_chunk_by_fixed_size_basic(self) -> None:
        """Tests basic fixed-size chunking."""
        text = "This is a test string with multiple words."
        chunks = chunk_by_fixed_size(text, chunk_size=10, chunk_overlap=2)
        assert len(chunks) == 6
        assert chunks[0] == "This is a "
        assert chunks[1] == "a test str"
        assert chunks[2] == "tring with"
        assert chunks[3] == "th multipl"
        assert chunks[4] == "ple words."
        assert chunks[5] == "s."

    def test_chunk_by_fixed_size_no_overlap(self) -> None:
        """Tests chunking without overlap."""
        text = "abcdefghijklmnop"
        chunks = chunk_by_fixed_size(text, chunk_size=4, chunk_overlap=0)
        assert len(chunks) == 4
        assert chunks[0] == "abcd"
        assert chunks[1] == "efgh"
        assert chunks[2] == "ijkl"
        assert chunks[3] == "mnop"

    def test_chunk_by_fixed_size_with_overlap(self) -> None:
        """Tests chunking with overlap."""
        text = "abcdefghijklmnop"
        chunks = chunk_by_fixed_size(text, chunk_size=4, chunk_overlap=2)
        assert len(chunks) == 8
        assert chunks[0] == "abcd"
        assert chunks[1] == "cdef"
        assert chunks[2] == "efgh"
        assert chunks[3] == "ghij"
        assert chunks[4] == "ijkl"
        assert chunks[5] == "klmn"
        assert chunks[6] == "mnop"
        assert chunks[7] == "op"

    def test_chunk_by_fixed_size_empty_text(self) -> None:
        """Tests handling of empty text."""
        text = ""
        chunks = chunk_by_fixed_size(text, chunk_size=5, chunk_overlap=1)
        assert len(chunks) == 0

    def test_chunk_by_fixed_size_text_shorter_than_chunk(self) -> None:
        """Tests when text is shorter than chunk size."""
        text = "abc"
        chunks = chunk_by_fixed_size(text, chunk_size=5, chunk_overlap=1)
        assert len(chunks) == 1
        assert chunks[0] == "abc"

    def test_chunk_by_fixed_size_text_exactly_chunk_size(self) -> None:
        """Tests when text length exactly matches chunk size."""
        text = "abcdef"
        chunks = chunk_by_fixed_size(text, chunk_size=6, chunk_overlap=2)
        assert len(chunks) == 2
        assert chunks[0] == "abcdef"
        assert chunks[1] == "ef"

    def test_chunk_by_fixed_size_overlap_larger_than_chunk(self) -> None:
        """Tests when overlap is larger than chunk size."""
        text = "abcdefghij"
        chunks = chunk_by_fixed_size(text, chunk_size=3, chunk_overlap=5)
        assert len(chunks) == 10
        assert chunks[0] == "abc"
        assert chunks[1] == "bcd"
        assert chunks[2] == "cde"
        assert chunks[3] == "def"
        assert chunks[4] == "efg"
        assert chunks[5] == "fgh"
        assert chunks[6] == "ghi"
        assert chunks[7] == "hij"
        assert chunks[8] == "ij"
        assert chunks[9] == "j"

    def test_chunk_by_fixed_size_overlap_equal_to_chunk(self) -> None:
        """Tests when overlap equals chunk size."""
        text = "abcdefghij"
        chunks = chunk_by_fixed_size(text, chunk_size=3, chunk_overlap=3)
        assert len(chunks) == 10
        assert chunks[0] == "abc"
        assert chunks[1] == "bcd"
        assert chunks[2] == "cde"
        assert chunks[3] == "def"
        assert chunks[4] == "efg"
        assert chunks[5] == "fgh"
        assert chunks[6] == "ghi"
        assert chunks[7] == "hij"
        assert chunks[8] == "ij"
        assert chunks[9] == "j"

    def test_chunk_by_fixed_size_whitespace_text(self) -> None:
        """Tests chunking of whitespace-only text."""
        text = "   \t\n  "  # Length 7: 3 spaces, tab, newline, 2 spaces
        chunks = chunk_by_fixed_size(text, chunk_size=3, chunk_overlap=1)
        # step_size = 3-1 = 2, so positions: 0, 2, 4, 6
        assert len(chunks) == 4
        assert chunks[0] == "   "  # pos 0-2
        assert chunks[1] == " \t\n"  # pos 2-4
        assert chunks[2] == "\n  "  # pos 4-6
        assert chunks[3] == " "  # pos 6-6 (partial)

    def test_chunk_by_fixed_size_zero_chunk_size(self) -> None:
        """Tests that zero chunk_size raises ValueError."""
        with pytest.raises(ValueError, match="chunk_size must be a positive integer."):
            chunk_by_fixed_size("test", chunk_size=0, chunk_overlap=0)

    def test_chunk_by_fixed_size_negative_chunk_size(self) -> None:
        """Tests that negative chunk_size raises ValueError."""
        with pytest.raises(ValueError, match="chunk_size must be a positive integer."):
            chunk_by_fixed_size("test", chunk_size=-5, chunk_overlap=0)

    def test_chunk_by_fixed_size_negative_overlap(self) -> None:
        """Tests chunking with negative overlap."""
        text = "abcdefghij"  # Length 10
        chunks = chunk_by_fixed_size(text, chunk_size=4, chunk_overlap=-2)
        # step_size = 4-(-2) = 6, so positions: 0, 6
        assert len(chunks) == 2
        assert chunks[0] == "abcd"  # pos 0-3
        assert chunks[1] == "ghij"  # pos 6-9

    def test_chunk_by_fixed_size_unicode_text(self) -> None:
        """Tests chunking of unicode text."""
        text = "Hello 世界! 🌍"
        chunks = chunk_by_fixed_size(text, chunk_size=6, chunk_overlap=2)
        assert len(chunks) == 3
        assert chunks[0] == "Hello "
        assert chunks[1] == "o 世界! "
        assert chunks[2] == "! 🌍"
