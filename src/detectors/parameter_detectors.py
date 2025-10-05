from typing import List
import re
from .base_detector import BaseDetector, CodeSmell

class LargeParameterListDetector(BaseDetector):
    """Detects methods with too many parameters"""
    
    @property
    def smell_type(self) -> str:
        return "LargeParameterList"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        threshold = self.config.get('threshold_parameters', 5)
        
        methods = self._extract_methods(content)
        
        for method in methods:
            if method['parameter_count'] > threshold:
                smell = CodeSmell(
                    smell_type=self.smell_type,
                    file_path=file_path,
                    start_line=method['start_line'],
                    end_line=method['start_line'],  # Just highlight the method signature
                    description=f"Method '{method['name']}' has too many parameters ({method['parameter_count']} > {threshold})",
                    severity="Medium",
                    suggestion="Consider using parameter objects or builder pattern to reduce parameter count"
                )
                smells.append(smell)
        
        return smells



class MagicNumberDetector(BaseDetector):
    """Detects magic numbers in code"""

    @property
    def smell_type(self) -> str:
        return "MagicNumbers"

    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells: List[CodeSmell] = []

        # Same config keys you already use:
        exclude_common = bool(self.config.get('exclude_common', True))
        exclude_constants = bool(self.config.get('exclude_constants', True))
        # Optional (defaults to True if not provided): flag numbers used as loop bounds in for(...) conditions
        flag_loop_bounds = bool(self.config.get('flag_loop_bounds', True))

        # --- 1) Remove block comments once (/* ... */) across the whole file ---
        # This prevents numbers inside block comments from being flagged, even if comments span lines.
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.S)

        # Work line-by-line
        lines = content.split('\n')

        # --- 2) Common numbers to ignore when exclude_common=True (kept identical to yours) ---
        common_numbers: Set[int] = {0, 1, -1, 2, 10, 100, 1000} if exclude_common else set()

        # --- 3) Rich numeric literal pattern (handles hex/bin/oct, underscores, floats, exponents, leading '.', and Java suffixes) ---
        number_re = re.compile(r"""
            (?<![A-Za-z_])                     # not inside identifier (left)
            -?(
                0[xX][0-9A-Fa-f_]+             # hex (e.g., 0xFF, 0Xdead_beef)
              | 0[bB][01_]+                    # binary (e.g., 0b1010)
              | 0[oO][0-7_]+                   # octal (e.g., 0o755)
              | \d[\d_]* (?:\.\d[\d_]*)? (?:[eE][+\-]?\d[\d_]*)?  # 12, 12.3, 1_000, 1e-3
              | \.\d[\d_]+                     # leading dot floats: .5
            )
            ([fFdDlL])?                        # optional numeric suffix (float/double/long)
            (?![A-Za-z_])                      # not inside identifier (right)
        """, re.VERBOSE)

        # --- 4) Helpers: strip strings/chars and canonicalize literals for "common" check ---
        def strip_strings_and_chars(s: str) -> str:
            """
            Replace the contents of "..." and '...' with quotes so indices stay aligned.
            Prevents numbers inside strings/chars from being matched.
            """
            s = re.sub(r'"(?:\\.|[^"\\])*"', '""', s)
            s = re.sub(r"'(?:\\.|[^'\\])*'", "''", s)
            return s

        def to_number_for_common_check(lit: str):
            """
            Convert a literal text (e.g., 0xFF, 1_000, .5f) into a Python int/float where possible,
            so we can compare to the common_numbers set. If parsing fails, return None.
            """
            core = re.sub(r'[fFdDlL]$', '', lit)  # drop Java suffix
            core = core.replace('_', '')          # drop underscores

            try:
                if core.lower().startswith('0x'):
                    return int(core, 16)
                if core.lower().startswith('0b'):
                    return int(core, 2)
                if core.lower().startswith('0o'):
                    return int(core, 8)

                # normalize leading '.' forms: ".5" -> "0.5", "-.5" -> "-0.5"
                if core.startswith('-.'):
                    core = '-0' + core[1:]
                elif core.startswith('.'):
                    core = '0' + core

                # Prefer int when possible so "1" and "1.0" both map to 1
                if re.fullmatch(r'-?\d+', core):
                    return int(core)
                return float(core)
            except Exception:
                return None

        # --- 5) Scan lines ---
        for line_num, raw in enumerate(lines, 1):
            # (a) Skip constant declarations entirely when exclude_constants=True
            #     Example: "static final int MAX = 10;" — numbers here are named, not magic.
            if exclude_constants and re.search(r'\b(final|static|const)\b[^=\n]*=', raw, re.IGNORECASE):
                continue

            # (b) Strip string/char literals so numbers inside quotes aren't matched
            line = strip_strings_and_chars(raw)

            # (c) Remove trailing // comments after stripping strings (so '//' inside quotes is ignored)
            line = line.split('//', 1)[0]

            # (d) Quick empty check
            if not line.strip():
                continue

            # (e) If the line has a classic for-header, compute init/cond/incr spans (used below)
            #     We want to ignore numbers in init/increment, but (optionally) flag numbers in the condition (loop bound).
            for_match = re.search(r'\bfor\s*\((.*?)\)', line)
            header_start = header_end = None
            init_start = init_end = cond_start = cond_end = incr_start = incr_end = None

            if for_match:
                header_start, header_end = for_match.span(1)  # indexes (in 'line') of the inside of (...)
                header = for_match.group(1)
                parts = [p.strip() for p in header.split(';')]

                if len(parts) == 3:
                    init, cond, incr = parts
                    # Compute absolute spans of init;cond;incr inside the line
                    init_start = header_start
                    init_end   = init_start + len(init)

                    cond_start = init_end + 1  # skip ';'
                    cond_end   = cond_start + len(cond)

                    incr_start = cond_end + 1
                    incr_end   = incr_start + len(incr)
                # If we can't split into 3 parts, we won't apply special for-handling (we'll just treat literals normally)

            # (f) Find numeric literals
            for m in number_re.finditer(line):
                literal = m.group(0)
                pos = m.start()

                # Skip array indices like arr[10] — often not "magic" in practice
                around = line[max(0, pos - 2): m.end() + 2]
                if re.search(r'\[\s*-?\d[\d_]*\s*\]', around):
                    continue

                # If we have a parsed for-header, skip numbers in init/increment,
                # and (optionally) FLAG numbers in the condition as potential magic loop bounds.
                if init_start is not None:
                    in_init = (init_start <= pos < init_end)
                    in_cond = (cond_start <= pos < cond_end)
                    in_incr = (incr_start <= pos < incr_end)

                    if in_init or in_incr:
                        # typical "i = 0" or "i++/i+=2" — usually fine to ignore
                        continue
                    if in_cond and not flag_loop_bounds:
                        # user opted not to flag loop bounds
                        continue
                    # if in_cond and flag_loop_bounds=True -> we let it be reported below

                # Skip "common" numbers if configured (e.g., 0, 1, 2, 10, 100)
                val_for_common = to_number_for_common_check(literal)
                if exclude_common and (val_for_common in common_numbers):
                    continue

                # Emit a finding (same shape & severity as your original implementation)
                smells.append(CodeSmell(
                    smell_type=self.smell_type,
                    file_path=file_path,
                    start_line=line_num,
                    end_line=line_num,
                    description=f"Magic number '{literal}' found at line {line_num}",
                    severity="Low",
                    suggestion="Consider extracting this number into a named constant"
                ))

        return smells
