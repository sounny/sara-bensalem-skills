"""
tests/tier1_features/test_vector_downsampling.py
Feature 6: Scale-aware vector downsampling
Authoritative Source: ORIGINAL_REQUEST.md §R4, spec_miner_skills/report.md §4
"""

import unittest

def downsample_stroke(w_native_mm: float, scale_factor: float, min_clamp_mm: float = 0.08) -> float:
    """Clamps effective stroke weight to prevent dropped hairline strokes."""
    scaled = w_native_mm * scale_factor
    return max(scaled, min_clamp_mm)

def downsample_hatch(native_spacing_mm: float, scale_factor: float) -> dict:
    """
    Decimates or replaces dense hatch patterns when resized:
    - s' >= 0.75mm: retain lines
    - 0.35mm <= s' < 0.75mm: decimate by 2 (2s')
    - s' < 0.35mm: replace with flat 10% tint poché
    """
    scaled_spacing = round(native_spacing_mm * scale_factor, 4)
    if scaled_spacing >= 0.75:
        return {"action": "RETAIN", "spacing_mm": scaled_spacing, "fill": "none"}
    elif scaled_spacing >= 0.35:
        return {"action": "DECIMATE_2X", "spacing_mm": scaled_spacing * 2.0, "fill": "none"}
    else:
        return {"action": "POCHE_REPLACE", "spacing_mm": None, "fill": "#F1F1EB"}

def filter_annotations(scale_factor: float) -> str:
    """Returns annotation level allowed at given viewport scale factor."""
    if scale_factor >= 0.75:
        return "FULL_ANNOTATIONS"
    elif scale_factor >= 0.40:
        return "MAJOR_DIMENSIONS_ONLY"
    else:
        return "GRAPHIC_SCALE_BAR_ONLY"

class TestVectorDownsampling(unittest.TestCase):
    """
    Validates scale-aware stroke clamping, hatch decimation, and annotation filtering.
    """

    def test_01_scale_1_0_preserves_stroke(self):
        """Verify scale factor 1.0 preserves original ISO 128 stroke weight."""
        self.assertAlmostEqual(downsample_stroke(0.50, 1.0), 0.50)
        self.assertAlmostEqual(downsample_stroke(0.13, 1.0), 0.13)

    def test_02_scale_0_5_clamps_to_minimum_threshold(self):
        """Verify 0.13mm stroke scaled at 0.5 (0.065mm) is clamped to 0.08mm."""
        clamped = downsample_stroke(0.13, 0.5, min_clamp_mm=0.08)
        self.assertEqual(clamped, 0.08, "Stroke must be clamped to 0.08mm minimum print threshold")

    def test_03_hatch_retention_above_threshold(self):
        """Verify hatch with scaled spacing >= 0.75mm is retained without decimation."""
        res = downsample_hatch(native_spacing_mm=1.5, scale_factor=0.8) # 1.2mm
        self.assertEqual(res["action"], "RETAIN")
        self.assertEqual(res["spacing_mm"], 1.2)
        self.assertEqual(res["fill"], "none")

    def test_04_hatch_decimation_middle_threshold(self):
        """Verify hatch with scaled spacing between 0.35mm and 0.75mm is decimated by 2x."""
        res = downsample_hatch(native_spacing_mm=1.0, scale_factor=0.5) # 0.5mm
        self.assertEqual(res["action"], "DECIMATE_2X")
        self.assertEqual(res["spacing_mm"], 1.0) # 0.5 * 2 = 1.0mm

    def test_05_hatch_poche_replacement_below_threshold(self):
        """Verify hatch with scaled spacing < 0.35mm is replaced by a flat 10% poché fill."""
        res = downsample_hatch(native_spacing_mm=0.8, scale_factor=0.3) # 0.24mm
        self.assertEqual(res["action"], "POCHE_REPLACE")
        self.assertIsNone(res["spacing_mm"])
        self.assertEqual(res["fill"], "#F1F1EB")

    def test_06_annotation_level_filtering(self):
        """Verify annotations are filtered hierarchically based on viewport scale."""
        self.assertEqual(filter_annotations(1.0), "FULL_ANNOTATIONS")
        self.assertEqual(filter_annotations(0.8), "FULL_ANNOTATIONS")
        self.assertEqual(filter_annotations(0.5), "MAJOR_DIMENSIONS_ONLY")
        self.assertEqual(filter_annotations(0.25), "GRAPHIC_SCALE_BAR_ONLY")

if __name__ == "__main__":
    unittest.main()
