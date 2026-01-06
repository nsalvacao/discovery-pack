#!/usr/bin/env python3
"""Detect critical gates in discovery artifacts"""
import sys, yaml, re
from pathlib import Path

def extract_frontmatter(file_path):
    content = file_path.read_text()
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}

def detect_gates(discovery_dir):
    gates_found = []
    
    # Gate 1: Equivalent options in 03_
    option_file = list(discovery_dir.glob("03_*.md"))
    if option_file:
        data = extract_frontmatter(option_file[0])
        options = data.get('options', [])
        if len(options) >= 2:
            scores = [opt.get('weighted_total', 0) for opt in options]
            if max(scores) - min(scores) < 0.5:
                gates_found.append({
                    'type': 'equivalent_options',
                    'severity': 'critical',
                    'message': f"⚠️  GATE: Options tied (scores: {scores})",
                    'action': 'Ask user for decision criteria'
                })
    
    # Gate 2: Validation without metrics in 05_
    val_file = list(discovery_dir.glob("05_*.md"))
    if val_file:
        data = extract_frontmatter(val_file[0])
        experiments = data.get('experiments', [])
        for exp in experiments:
            criteria = exp.get('success_criteria', {})
            if not criteria.get('quantitative', {}).get('pass_if'):
                gates_found.append({
                    'type': 'unmeasurable_validation',
                    'severity': 'high',
                    'message': f"⚠️  GATE: Experiment '{exp.get('title')}' lacks quantitative metrics",
                    'action': 'Define measurable success criteria'
                })
    
    # Gate 3: Contradictory assumptions in 04_
    assump_file = list(discovery_dir.glob("04_*.md"))
    if assump_file:
        data = extract_frontmatter(assump_file[0])
        assumptions = [a.get('assumption', '') for a in data.get('assumptions', [])]
        # Simple keyword contradiction detection
        if any('offline' in a.lower() for a in assumptions) and any('real-time sync' in a.lower() for a in assumptions):
            gates_found.append({
                'type': 'contradictory_assumptions',
                'severity': 'high',
                'message': "⚠️  GATE: Potential contradiction (offline + real-time sync)",
                'action': 'Clarify priority: offline-first or real-time?'
            })
    
    if gates_found:
        print(f"\n🚨 {len(gates_found)} Critical Gates Detected\n")
        for gate in gates_found:
            print(f"{gate['message']}")
            print(f"   Action: {gate['action']}\n")
        return gates_found
    else:
        print("✅ No critical gates detected")
        return []

if __name__ == "__main__":
    detect_gates(Path(sys.argv[1]))
