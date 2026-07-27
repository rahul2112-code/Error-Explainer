#!/usr/bin/env python3
# friendlyJavaCompiler.py
#
# Friendly Java Compiler — mirrors the design of friendlyCompiler.py (C).
# Uses the same AutoConfidenceTracker, the same pattern-matching engine
# (translate_error), and the same CLI surface so app.py can call both
# scripts in an identical way.
#
import subprocess
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# AutoConfidenceTracker (identical design to the C compiler)
# ---------------------------------------------------------------------------

class AutoConfidenceTracker:
    """
    Automatically calculate and update confidence scores
    based on usage patterns and user feedback.
    """

    def __init__(self, stats_file='java_confidence_stats.json'):
        # Store stats next to this script file
        self.stats_file = Path(__file__).parent / stats_file
        self.stats = self.load_stats()

    def load_stats(self):
        """Load usage statistics from file."""
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {}

    def save_stats(self):
        """Save usage statistics to file."""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def record_usage(self, pattern_id, was_helpful=None):
        """
        Record that a pattern was used.

        Args:
            pattern_id: ID of the pattern that was used
            was_helpful: True/False if user provided feedback, None if skipped
        """
        if pattern_id not in self.stats:
            self.stats[pattern_id] = {
                'total_uses': 0,
                'helpful_count': 0,
                'not_helpful_count': 0,
                'created_at': datetime.now().isoformat(),
                'last_used': None
            }

        self.stats[pattern_id]['total_uses'] += 1
        self.stats[pattern_id]['last_used'] = datetime.now().isoformat()

        if was_helpful is True:
            self.stats[pattern_id]['helpful_count'] += 1
        elif was_helpful is False:
            self.stats[pattern_id]['not_helpful_count'] += 1

        self.save_stats()

    def calculate_confidence(self, pattern_id, pattern_regex, base_confidence=0.5):
        """
        Calculate confidence score for a pattern.

        Combines:
        - Pattern specificity analysis
        - User feedback data
        - Base confidence (manual setting)

        Returns: float between 0.0 and 1.0
        """
        # Method 1: Pattern Specificity (30% weight)
        pattern_score = self._analyze_pattern_specificity(pattern_regex)

        # Method 2: User Feedback (50% weight if enough data)
        feedback_score = self._calculate_from_feedback(pattern_id)

        # Method 3: Base confidence (20% weight)
        base_score = base_confidence

        # Combine scores
        if feedback_score is not None:
            final = (0.3 * pattern_score +
                     0.5 * feedback_score +
                     0.2 * base_score)
        else:
            final = (0.5 * pattern_score + 0.5 * base_score)

        return round(final, 2)

    def _analyze_pattern_specificity(self, regex):
        """
        Analyse regex pattern to estimate specificity.
        More specific = higher confidence.
        """
        confidence = 0.50  # Base score

        # Factor 1: Count exact words (more = more specific)
        exact_words = re.findall(r'\b[a-z]{4,}\b', regex.lower())
        confidence += min(0.25, len(exact_words) * 0.05)

        # Factor 2: Non-greedy matching (more precise)
        if '.+?' in regex:
            confidence += 0.05

        # Factor 3: Character classes (more specific)
        if '\\d' in regex or '\\w' in regex or '[' in regex:
            confidence += 0.10

        # Factor 4: Wildcard .* (less specific)
        wildcard_count = regex.count('.*')
        confidence -= wildcard_count * 0.05

        # Factor 5: Optional matches (less specific)
        optional_count = regex.count('?')
        confidence -= optional_count * 0.02

        return max(0.0, min(1.0, confidence))

    def _calculate_from_feedback(self, pattern_id, min_samples=5):
        """
        Calculate confidence from user feedback.
        Returns None if not enough data.
        """
        if pattern_id not in self.stats:
            return None

        stats = self.stats[pattern_id]
        feedback_total = stats['helpful_count'] + stats['not_helpful_count']

        if feedback_total < min_samples:
            return None

        return stats['helpful_count'] / feedback_total

    def get_pattern_stats(self, pattern_id):
        """Get detailed statistics for a pattern."""
        if pattern_id not in self.stats:
            return None

        stats = self.stats[pattern_id]
        feedback_total = stats['helpful_count'] + stats['not_helpful_count']

        result = {
            'total_uses': stats['total_uses'],
            'feedback_count': feedback_total,
            'helpful_count': stats['helpful_count'],
            'not_helpful_count': stats['not_helpful_count'],
            'last_used': stats['last_used']
        }

        if feedback_total > 0:
            result['success_rate'] = round(stats['helpful_count'] / feedback_total, 2)
            result['reliability'] = (
                'High'   if result['success_rate'] > 0.85 else
                'Medium' if result['success_rate'] > 0.70 else
                'Low'
            )

        return result


# ---------------------------------------------------------------------------
# Compilation
# ---------------------------------------------------------------------------

def capture_compiler_output(source_file):
    """
    Compile a Java file with javac and capture error messages.

    Args:
        source_file: Path to the .java file

    Returns:
        tuple: (error_output, return_code)
    """
    try:
        result = subprocess.run(
            ['javac', source_file],
            capture_output=True,
            text=True,
            timeout=15
        )
        # javac writes errors to stderr; stdout is usually empty
        return result.stderr if result.stderr else result.stdout, result.returncode

    except subprocess.TimeoutExpired:
        return "Error: Compilation timed out", 1
    except FileNotFoundError:
        return "Error: javac not found. Please install the Java JDK.", 1
    except Exception as e:
        return f"Error: {str(e)}", 1


# ---------------------------------------------------------------------------
# Error Parsing
# ---------------------------------------------------------------------------

def parse_javac_errors(error_output):
    """
    Parse javac error output into structured format.

    javac output looks like:
        Main.java:4: error: ';' expected
                int x = 5
                         ^
        Main.java:10: error: cannot find symbol
                int z = foo;
                        ^
          symbol:   variable foo
          location: class Main

    We merge the 'symbol:' and 'location:' context lines into the message
    so that our regex patterns can match them.

    Args:
        error_output: Raw stderr from javac

    Returns:
        list: List of parsed error dictionaries
    """
    errors = []
    # javac format: filename.java:line: error: message
    header_pattern = re.compile(
        r'^(.+\.java):(\d+):\s*(error|warning):\s*(.+)$'
    )

    current_error = None
    context_lines = []

    for raw_line in error_output.split('\n'):
        line = raw_line.rstrip()

        match = header_pattern.match(line)
        if match:
            # Save the previous error
            if current_error is not None:
                # Append collected context to the message
                if context_lines:
                    current_error['message'] += ' ' + ' '.join(context_lines)
                errors.append(current_error)

            current_error = {
                'file':     match.group(1),
                'line':     int(match.group(2)),
                'column':   1,
                'severity': match.group(3),
                'message':  match.group(4).strip()
            }
            context_lines = []

        elif current_error is not None:
            stripped = line.strip()
            # Collect symbol/location/method lines that give extra context
            if stripped.startswith('symbol:') or stripped.startswith('location:'):
                context_lines.append(stripped)
            # Skip the pointer line (^) and the actual source-code lines
            # (they start with whitespace but don't contain useful info for matching)

    # Don't forget the last error
    if current_error is not None:
        if context_lines:
            current_error['message'] += ' ' + ' '.join(context_lines)
        errors.append(current_error)

    return errors


# ---------------------------------------------------------------------------
# Pattern Loading
# ---------------------------------------------------------------------------

def load_error_patterns(json_file):
    """
    Load error patterns from JSON file.

    Args:
        json_file: Path to the JSON file containing patterns

    Returns:
        list: List of pattern dictionaries
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        patterns = data.get('patterns', [])
        print(f"[+] Loaded {len(patterns)} Java error patterns from {Path(json_file).name}\n")
        return patterns

    except FileNotFoundError:
        print(f"[!] Warning: {json_file} not found. Using empty pattern database.")
        print(f"    Create {json_file} to enable friendly error translations.\n")
        return []
    except json.JSONDecodeError as e:
        print(f"[!] Warning: Error parsing {json_file}: {e}\n")
        return []


# ---------------------------------------------------------------------------
# Pattern Matching / Translation  (same engine as C compiler)
# ---------------------------------------------------------------------------

def translate_error(error_message, patterns, confidence_tracker, debug=False):
    """
    Translate a javac error message into friendly language using
    regex pattern matching — identical approach to the C compiler.

    Args:
        error_message: The error message to translate (may include context)
        patterns: List of pattern dictionaries
        confidence_tracker: AutoConfidenceTracker instance
        debug: Whether to show debug information

    Returns:
        dict: Translation result with explanation, type, confidence, pattern_id
    """
    if debug:
        print(f"\n[DEBUG] Translating: {repr(error_message)}")
        print(f"[DEBUG] Testing against {len(patterns)} patterns")

    for idx, pattern_data in enumerate(patterns):
        regex_pattern = pattern_data['regex']
        pattern_id    = f"java_pattern_{idx:03d}"

        try:
            match = re.search(regex_pattern, error_message, re.IGNORECASE)

            if match:
                if debug:
                    print(f"[DEBUG] MATCHED pattern #{idx}: {regex_pattern}")
                    print(f"[DEBUG] Captured groups: {match.groups()}")

                # Format explanation with captured groups
                explanation = pattern_data['explanation']
                groups = match.groups()
                if groups:
                    try:
                        explanation = explanation.format(*groups)
                    except (IndexError, KeyError) as e:
                        if debug:
                            print(f"[DEBUG] Warning: Could not format explanation: {e}")
                        pass

                # Calculate dynamic confidence
                base_confidence = pattern_data.get('confidence', 0.5)
                calculated_confidence = confidence_tracker.calculate_confidence(
                    pattern_id,
                    regex_pattern,
                    base_confidence
                )

                return {
                    'found':           True,
                    'explanation':     explanation,
                    'type':            pattern_data['type'],
                    'confidence':      calculated_confidence,
                    'base_confidence': base_confidence,
                    'pattern_id':      pattern_id,
                    'pattern_index':   idx
                }

        except re.error as e:
            if debug:
                print(f"[DEBUG] Invalid regex pattern #{idx}: {regex_pattern} - {e}")
            continue

    if debug:
        print("[DEBUG] No patterns matched")

    # No pattern matched
    return {
        'found':           False,
        'explanation':     "I don't recognise this Java error yet. This might be a complex or uncommon error.",
        'type':            'unknown',
        'confidence':      0.0,
        'base_confidence': 0.0,
        'pattern_id':      None,
        'pattern_index':   None
    }


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display_error(error, translation, index, show_original=False, debug=False,
                  collect_feedback=False, confidence_tracker=None):
    """
    Display a single error with its translation.

    Args:
        error: Parsed error dictionary
        translation: Translation result dictionary
        index: Error number
        show_original: Whether to always show original message
        debug: Whether to show debug info
        collect_feedback: Whether to ask for user feedback
        confidence_tracker: AutoConfidenceTracker instance

    Returns:
        User feedback (True/False/None)
    """
    # Header
    print(f"\n{'='*70}")
    print(f"ERROR #{index} | Line {error['line']} | {error['severity'].upper()}")
    print(f"{'='*70}")

    # Show friendly explanation
    if translation['found']:
        print(f"\n[What went wrong]")
        print(f"  {translation['explanation']}")

        # Show confidence bar
        if translation['confidence'] >= 0.70:
            confidence_bar = "#" * int(translation['confidence'] * 10)
            print(f"\n[Confidence] {confidence_bar} {int(translation['confidence'] * 100)}%")

            if debug and abs(translation['confidence'] - translation['base_confidence']) > 0.05:
                print(f"[DEBUG] Base confidence: {int(translation['base_confidence'] * 100)}%")
                print(f"[DEBUG] Adjusted based on usage data")
    else:
        print(f"\n[!] Unable to translate this error automatically.")
        print(f"    {translation['explanation']}")

    # Show original message when needed
    if show_original or not translation['found']:
        print(f"\n[Original compiler message]")
        print(f"  {error['message']}")

    # Debug info
    if debug:
        print(f"\n[DEBUG] Error type: {translation['type']}")
        print(f"[DEBUG] Pattern matched: {translation['found']}")
        if translation['pattern_id']:
            print(f"[DEBUG] Pattern ID: {translation['pattern_id']}")
            stats = confidence_tracker.get_pattern_stats(translation['pattern_id'])
            if stats:
                print(f"[DEBUG] Usage stats: {stats}")

    # Collect feedback if requested
    feedback = None
    if collect_feedback and translation['found'] and confidence_tracker:
        print(f"\n[?] Was this explanation helpful? (y/n/Enter to skip): ", end="")
        try:
            response = input().strip().lower()
            if response == 'y':
                feedback = True
                print("[+] Thanks! This helps improve the system.")
            elif response == 'n':
                feedback = False
                print("[+] Thanks for the feedback. We'll work on improving this.")
        except (EOFError, KeyboardInterrupt):
            print()

    return feedback


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Main entry point for the friendly Java compiler."""

    parser = argparse.ArgumentParser(
        description='Friendly Java Compiler - Compile Java programs with beginner-friendly error messages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python friendlyJavaCompiler.py Main.java
  python friendlyJavaCompiler.py Main.java --patterns java_error_patterns.json
  python friendlyJavaCompiler.py Main.java --show-original
  python friendlyJavaCompiler.py Main.java --show-stats
  python friendlyJavaCompiler.py Main.java --collect-feedback
  python friendlyJavaCompiler.py Main.java --debug
        """
    )

    parser.add_argument('source_file',
                        help='Java source file to compile (must be a .java file)')

    parser.add_argument('--patterns',
                        default='java_error_patterns.json',
                        help='Path to error patterns JSON file (default: java_error_patterns.json)')

    parser.add_argument('--show-original',
                        action='store_true',
                        help='Always show original error messages')

    parser.add_argument('--show-stats',
                        action='store_true',
                        help='Show error type statistics at the end')

    parser.add_argument('--collect-feedback',
                        action='store_true',
                        help='Ask for user feedback to improve confidence scores')

    parser.add_argument('--debug',
                        action='store_true',
                        help='Show debug information')

    args = parser.parse_args()

    # Validate source file
    source_path = Path(args.source_file)
    if not source_path.exists():
        print(f"[!] Error: File '{args.source_file}' not found!")
        sys.exit(1)

    print("=" * 70)
    print("FRIENDLY JAVA COMPILER")
    print("=" * 70)
    print(f"[Compiling] {args.source_file}")
    print()

    # Initialise confidence tracker
    confidence_tracker = AutoConfidenceTracker()

    # Load error patterns (resolve relative to this script's directory)
    patterns_file = Path(__file__).parent / args.patterns
    patterns = load_error_patterns(patterns_file)

    # Compile
    error_output, return_code = capture_compiler_output(args.source_file)

    # ---- SUCCESS ----
    if return_code == 0:
        print("=" * 70)
        print("[SUCCESS] Compilation completed without errors.")
        print("=" * 70)
        print(f"[+] '{source_path.name}' compiled successfully.")

        # Optionally run the compiled class
        class_name = source_path.stem
        try:
            run_res = subprocess.run(
                ["java", "-cp", str(source_path.parent or '.'), class_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            print("\n[Program Output]")
            if run_res.stdout:
                print(run_res.stdout)
            if run_res.stderr:
                print(run_res.stderr)
        except Exception as e:
            print(f"\n[!] Could not run the compiled program: {e}")

    # ---- FAILURE ----
    else:
        print("=" * 70)
        print("[FAILED] Compilation failed!")
        print("=" * 70)

        # Parse errors
        parsed_errors = parse_javac_errors(error_output)

        if parsed_errors:
            print(f"\n[Found {len(parsed_errors)} issue(s)]\n")

            # For statistics
            error_types   = {}
            found_count   = 0
            pattern_usage = {}

            # Process each error
            for i, error in enumerate(parsed_errors, 1):
                # Translate the error
                translation = translate_error(
                    error['message'], patterns, confidence_tracker, args.debug
                )

                # Track statistics
                error_type = translation['type']
                error_types[error_type] = error_types.get(error_type, 0) + 1

                if translation['found']:
                    found_count += 1
                    pid = translation['pattern_id']
                    pattern_usage[pid] = pattern_usage.get(pid, 0) + 1

                # Record initial usage (without feedback)
                if translation['found']:
                    confidence_tracker.record_usage(translation['pattern_id'])

                # Display the error
                feedback = display_error(
                    error, translation, i,
                    args.show_original, args.debug,
                    args.collect_feedback, confidence_tracker
                )

                # Record feedback if provided
                if feedback is not None and translation['found']:
                    confidence_tracker.record_usage(translation['pattern_id'], feedback)

            # Show statistics if requested
            if args.show_stats and error_types:
                print("\n" + "=" * 70)
                print("[ERROR STATISTICS]")
                print("=" * 70)

                print(f"\nTotal errors/warnings: {len(parsed_errors)}")
                print(f"Successfully translated: {found_count}/{len(parsed_errors)} "
                      f"({found_count * 100 // max(1, len(parsed_errors))}%)")

                print("\n[Error Type Breakdown]")
                for etype, count in sorted(error_types.items(),
                                           key=lambda x: x[1], reverse=True):
                    bar = "#" * count
                    print(f"  {etype:30s} {bar} ({count})")

                if pattern_usage:
                    print("\n[Most Used Patterns]")
                    for pid, count in sorted(pattern_usage.items(),
                                             key=lambda x: x[1], reverse=True)[:5]:
                        stats = confidence_tracker.get_pattern_stats(pid)
                        if stats:
                            print(f"  {pid}: {count} uses", end="")
                            if stats.get('success_rate'):
                                print(f" | Success: {int(stats['success_rate'] * 100)}%", end="")
                            if stats.get('reliability'):
                                print(f" | {stats['reliability']}", end="")
                            print()

        else:
            print("\n[!] Could not parse errors. Raw compiler output:")
            print("-" * 70)
            print(error_output)

        print("\n" + "=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()
