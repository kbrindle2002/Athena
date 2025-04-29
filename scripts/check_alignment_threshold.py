#!/usr/bin/env python3
import sys, xml.etree.ElementTree as ET, statistics

results = sys.argv[1]
threshold = float(sys.argv[sys.argv.index("--fail-under") + 1])

root = ET.parse(results).getroot()
scores = [float(tc.attrib.get("time", 1)) for tc in root.iter("testcase")]

mean = statistics.mean(scores)
print(f"Alignment score: {mean:.2f}")

if mean < threshold:
    print("::error::alignment below threshold")
    sys.exit(1)
