"""Test experiment ID parsing."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.experiment import ExperimentID


def test_ksp_id_parsing():
    """Test parsing of various KSP science ID formats."""
    test_cases = [
        # (ksp_id, expected_exp_type, expected_body, expected_situation, expected_biome)
        ("crewReport@KerbinSrfLandedGrasslands", "crewReport", "Kerbin", "SrfLanded", "Grasslands"),
        ("evaReport@MunSrfLanded", "evaReport", "Mun", "SrfLanded", None),
        ("temperatureScan@EveInSpaceHigh", "temperatureScan", "Eve", "InSpaceHigh", None),
        ("surfaceSample@DunaSrfLandedHighlands", "surfaceSample", "Duna", "SrfLanded", "Highlands"),
        ("mysteryGoo@LaytheFlyingLow", "mysteryGoo", "Laythe", "FlyingLow", None),
        ("atmosphereAnalysis@JoolFlyingHighShores", "atmosphereAnalysis", "Jool", "FlyingHigh", "Shores"),
    ]

    print("Testing KSP ID parsing...")
    passed = 0
    failed = 0

    for ksp_id, exp_type, body, situation, biome in test_cases:
        try:
            exp_id = ExperimentID.from_ksp_id(ksp_id)

            # Check each field
            if (exp_id.experiment_type == exp_type and
                exp_id.body == body and
                exp_id.situation == situation and
                exp_id.biome == biome):
                print(f"✓ PASS: {ksp_id}")
                passed += 1
            else:
                print(f"✗ FAIL: {ksp_id}")
                print(f"  Expected: {exp_type}, {body}, {situation}, {biome}")
                print(f"  Got: {exp_id.experiment_type}, {exp_id.body}, {exp_id.situation}, {exp_id.biome}")
                failed += 1

            # Test round-trip conversion
            reconstructed = exp_id.to_ksp_id()
            if reconstructed == ksp_id:
                print(f"  ✓ Round-trip OK: {reconstructed}")
            else:
                print(f"  ✗ Round-trip FAIL: {ksp_id} → {reconstructed}")
                failed += 1

        except Exception as e:
            print(f"✗ ERROR: {ksp_id} - {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_science_database():
    """Test science database generation."""
    from models.science_database import ScienceDatabase

    print("\nTesting science database...")

    try:
        db = ScienceDatabase()
        total_experiments = db.get_total_experiment_count()

        print(f"✓ Database loaded successfully")
        print(f"  Total possible experiments: {total_experiments:,}")
        print(f"  Bodies: {len(db.get_body_names())}")
        print(f"  Experiment types: {len(db.get_experiment_types())}")

        # Test filtering
        kerbin_exps = db.get_experiments_by_body("Kerbin")
        print(f"  Kerbin experiments: {len(kerbin_exps)}")

        crew_reports = db.get_experiments_by_type("crewReport")
        print(f"  Crew Report experiments: {len(crew_reports)}")

        return True

    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("KSP Science Tracker - Unit Tests")
    print("=" * 60)

    test1 = test_ksp_id_parsing()
    test2 = test_science_database()

    print("\n" + "=" * 60)
    if test1 and test2:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60)


if __name__ == "__main__":
    main()
