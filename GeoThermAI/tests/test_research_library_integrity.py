#!/usr/bin/env python3
"""
Unit and Integration Tests for GeoThermAI Research Library Integrity
Verifies SHA-256 matching, index schemas, duplicate audit, and missing references.
"""

import os
import csv
import hashlib
from pathlib import Path

REPO_ROOT = Path('/Users/knight/Development/CoreX').resolve()
LIBRARY_ROOT = REPO_ROOT / 'research_library'
INDEX_DIR = LIBRARY_ROOT / '00_INDEX'

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def test_library_structure():
    expected_categories = [
        '00_INDEX',
        '01_GEOTHERMAL_FAVORABILITY_AND_PFA',
        '02_AI_ML_AND_STATISTICAL_METHODS',
        '03_SPATIAL_CV_PU_AND_UNCERTAINTY',
        '04_THAILAND_GEOSCIENCE_AND_GEOPHYSICS',
        '05_HYDROGEOLOGY_GEOCHEMISTRY_AND_HEAT_FLOW',
        '06_SATELLITE_REMOTE_SENSING_AND_GIS',
        '07_ENERGY_POLICY_PDP2026_AND_DATACENTER',
        '08_ENVIRONMENT_ECONOMICS_AND_SOCIAL_IMPACT',
        '09_PROJECT_RESEARCH_REPORTS_AND_PROTOCOLS',
        '10_SUPPLEMENTARY_AND_CITATIONS'
    ]
    for cat in expected_categories:
        cat_path = LIBRARY_ROOT / cat
        assert cat_path.exists() and cat_path.is_dir(), f"Missing category directory: {cat}"
    print("[PASS] test_library_structure")

def test_index_files_exist():
    expected_files = [
        'README_TH.md',
        'RESEARCH_MASTER_INDEX.csv',
        'RESEARCH_MASTER_INDEX.md',
        'DUPLICATES_AND_VERSIONS.csv',
        'MISSING_REFERENCES.md',
        'DATASET_POINTERS.csv',
        'SOURCE_AND_LICENSE_NOTES.md',
        'COLLECTION_EXECUTION_LOG.md'
    ]
    for fname in expected_files:
        p = INDEX_DIR / fname
        assert p.exists() and p.is_file(), f"Missing index file: {fname}"
        assert p.stat().st_size > 0, f"Empty index file: {fname}"
    print("[PASS] test_index_files_exist")

def test_master_index_schema_and_hashes():
    csv_path = INDEX_DIR / 'RESEARCH_MASTER_INDEX.csv'
    expected_cols = [
        'id', 'category', 'filename', 'library_relative_path', 'source_local_path',
        'sha256', 'size_bytes', 'file_type', 'title', 'authors', 'year', 'doi',
        'publication_or_agency', 'topic_tags', 'relevance_to_geothermai',
        'research_track', 'evidence_status', 'license_status',
        'redistribution_status', 'metadata_confidence', 'notes'
    ]

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == expected_cols, f"Column mismatch in CSV: {reader.fieldnames}"
        rows = list(reader)

    assert len(rows) >= 80, f"Expected at least 80 rows, found {len(rows)}"

    verified_count = 0
    missing_count = 0

    for r in rows:
        status = r['evidence_status']
        if status == 'SOURCE_VERIFIED':
            verified_count += 1
            lib_file = REPO_ROOT / r['library_relative_path']
            assert lib_file.exists(), f"Indexed file does not exist: {lib_file}"
            actual_hash = calculate_sha256(lib_file)
            assert actual_hash == r['sha256'], f"Hash mismatch for {r['filename']}: expected {r['sha256']} got {actual_hash}"
            assert lib_file.stat().st_size == int(r['size_bytes']), f"Size mismatch for {r['filename']}"
        elif status == 'MISSING_LOCAL_FILE':
            missing_count += 1
            assert r['sha256'] == 'MISSING_LOCAL_FILE_HASH', "Missing file should have missing hash sentinel"

    assert verified_count >= 70, f"Expected at least 70 verified files, got {verified_count}"
    assert missing_count >= 8, f"Expected at least 8 missing files, got {missing_count}"
    print(f"[PASS] test_master_index_schema_and_hashes ({verified_count} verified, {missing_count} missing logged)")

def test_duplicates_and_dataset_pointers():
    dup_path = INDEX_DIR / 'DUPLICATES_AND_VERSIONS.csv'
    with open(dup_path, 'r', encoding='utf-8') as f:
        dups = list(csv.DictReader(f))
    assert len(dups) >= 8, f"Expected at least 8 duplicate findings, got {len(dups)}"

    ptr_path = INDEX_DIR / 'DATASET_POINTERS.csv'
    with open(ptr_path, 'r', encoding='utf-8') as f:
        ptrs = list(csv.DictReader(f))
    assert len(ptrs) >= 10, f"Expected at least 10 dataset pointers, got {len(ptrs)}"
    print("[PASS] test_duplicates_and_dataset_pointers")

def test_symlink_and_gitignore():
    symlink_path = REPO_ROOT / 'GeoThermAI' / 'research_library'
    assert symlink_path.exists(), "Symlink GeoThermAI/research_library missing"
    assert (symlink_path / '00_INDEX').exists(), "Symlink does not resolve to research_library"

    gitignore_path = REPO_ROOT / '.gitignore'
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        gi_txt = f.read()
    assert 'research_library/**/*.pdf' in gi_txt, "Gitignore missing research_library pdf exclusion"
    print("[PASS] test_symlink_and_gitignore")

def run_all_tests():
    print("=" * 60)
    print("Running GeoThermAI Research Library Integrity Tests")
    print("=" * 60)
    test_library_structure()
    test_index_files_exist()
    test_master_index_schema_and_hashes()
    test_duplicates_and_dataset_pointers()
    test_symlink_and_gitignore()
    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! (5/5 suites passing)")
    print("=" * 60)

if __name__ == '__main__':
    run_all_tests()
