"""Tests for the KnowledgeBase module."""

import pytest

from encyclopedia.knowledge_base import KnowledgeBase, KnowledgeEntry


class TestKnowledgeEntry:
    def test_display_short(self):
        entry = KnowledgeEntry(
            title="Blockchain",
            category="Technology",
            summary="A distributed ledger.",
            tags=["crypto"],
        )
        display = entry.display()
        assert "Blockchain" in display
        assert "A distributed ledger." in display
        assert "crypto" in display

    def test_display_full_includes_details(self):
        entry = KnowledgeEntry(
            title="X",
            category="Cat",
            summary="Short.",
            details="Long details here.",
        )
        display = entry.display(full=True)
        assert "Long details here." in display

    def test_display_no_details_in_short(self):
        entry = KnowledgeEntry(
            title="X",
            category="Cat",
            summary="Short.",
            details="Long details here.",
        )
        display = entry.display(full=False)
        assert "Long details here." not in display

    def test_related_entries_shown(self):
        entry = KnowledgeEntry(
            title="X",
            category="Cat",
            summary="S",
            related_entries=["Y", "Z"],
        )
        display = entry.display()
        assert "Y" in display
        assert "Z" in display


class TestKnowledgeBase:
    def setup_method(self):
        self.kb = KnowledgeBase()

    def test_get_entry_existing(self):
        entry = self.kb.get_entry("Blockchain")
        assert entry is not None
        assert entry.title == "Blockchain"

    def test_get_entry_missing(self):
        assert self.kb.get_entry("Nonexistent Entry") is None

    def test_add_and_get_custom_entry(self):
        custom = KnowledgeEntry(
            title="Quantum Computing",
            category="Technology",
            summary="Computing with quantum bits.",
        )
        self.kb.add_entry(custom)
        retrieved = self.kb.get_entry("Quantum Computing")
        assert retrieved is custom

    def test_add_entry_overwrites_existing(self):
        new = KnowledgeEntry(
            title="Blockchain",
            category="Technology",
            summary="Updated summary.",
        )
        self.kb.add_entry(new)
        assert self.kb.get_entry("Blockchain").summary == "Updated summary."

    def test_remove_entry(self):
        result = self.kb.remove_entry("Blockchain")
        assert result is True
        assert self.kb.get_entry("Blockchain") is None

    def test_remove_nonexistent_entry(self):
        assert self.kb.remove_entry("Ghost") is False

    def test_search_finds_by_title(self):
        results = self.kb.search("Blockchain")
        titles = [e.title for e in results]
        assert "Blockchain" in titles

    def test_search_case_insensitive(self):
        results = self.kb.search("blockchain")
        assert len(results) > 0

    def test_search_finds_by_tag(self):
        results = self.kb.search("smart-contract")
        assert any("Smart Contract" == e.title for e in results)

    def test_search_no_results(self):
        results = self.kb.search("xyzzy_unique_string_that_matches_nothing")
        assert results == []

    def test_get_by_category(self):
        entries = self.kb.get_by_category("Technology")
        assert len(entries) > 0
        for e in entries:
            assert e.category == "Technology"

    def test_get_by_category_case_insensitive(self):
        entries = self.kb.get_by_category("technology")
        assert len(entries) > 0

    def test_get_by_tag(self):
        entries = self.kb.get_by_tag("blockchain")
        assert len(entries) > 0

    def test_list_categories_sorted(self):
        cats = self.kb.list_categories()
        assert cats == sorted(cats)
        assert len(cats) > 1

    def test_list_all_titles_sorted(self):
        titles = self.kb.list_all_titles()
        assert titles == sorted(titles)
        assert len(titles) >= 7  # built-in entries

    def test_summarize_contains_header(self):
        summary = self.kb.summarize()
        assert "Knowledge Base" in summary

    def test_summarize_contains_entry_titles(self):
        summary = self.kb.summarize()
        assert "Blockchain" in summary
        assert "Robotics" in summary
