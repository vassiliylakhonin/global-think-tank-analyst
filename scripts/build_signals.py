#!/usr/bin/env python3
"""Auto-generate signal indexes (index.json, feed.json, latest.md)."""

import sys
from pathlib import Path

# Add scripts directory to path to import generator
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_policy_risk_signal as generator

def main():
    print("Building signal indexes...")
    generator.update_agent_indexes()
    
    # Also update the signals/README.md archive list
    entries = generator.collect_signal_entries()
    if entries:
        latest = entries[0]
        generator.update_archive(latest["date"], latest["path"], latest["title"])
        
    print("Signal indexes built successfully.")

if __name__ == "__main__":
    main()
