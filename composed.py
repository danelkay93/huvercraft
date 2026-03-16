"""
Composed regex patterns built from atomic fragments.

Each pattern here is a complete, compilable regex that combines
atoms from `atoms.py` to match a specific linguistic structure.
Organised by what they match, not by how they're used.
"""

from . import atoms as a

# =============================================================================
# ESTABLISHMENT — any printing/publishing house term
# =============================================================================

# Full compound: prefix fused to nyomda as one word
# e.g., könyvnyomda, kőnyomda, gyorsnyomda, lithografnyomda, zeneműnyomda
COMPOUND_NYOMDA = rf"""
    \b
    {a.PREFIX_ANY}
    {a.NYOMDA_STEM}
    \b
"""

# Elliptical form: "kő- és könyvnyomda"
# The first prefix is truncated with a hyphen; nyomda appears only once at the end.
# The final element is always a full compound (prefix+nyomda fused).
ELLIPTICAL_NYOMDA = rf"""
    \b
    {a.PREFIX_ANY} {a.HYPHEN_FLEX}          # truncated prefix, e.g. "kő-"
    (?:{a.ES_CONJUNCTION})?                  # optional "és"
    (?:{a.PREFIX_ANY} {a.HYPHEN_FLEX})?      # optional second truncated prefix
    (?:{a.ES_CONJUNCTION})?                  # optional second "és"
    {a.PREFIX_ANY}?                           # optional final prefix (fused into compound)
    {a.NYOMDA_STEM}                           # always ends with full nyomda stem
"""

# Any nyomda reference (compound, elliptical, or standalone)
ANY_NYOMDA = rf"""
    (?:
        {COMPOUND_NYOMDA}
      | {ELLIPTICAL_NYOMDA}
      | \b{a.NYOMDA_STEM}\b
    )
"""

# Any establishment term: nyomda OR műintézet OR műkiadó OR litográfia etc.
ANY_ESTABLISHMENT = rf"""
    (?:
        {COMPOUND_NYOMDA}
      | {ELLIPTICAL_NYOMDA}
      | \b{a.ESTABLISHMENT}\b
    )
"""


# =============================================================================
# PRINTER NAMES — full name patterns
# =============================================================================

# Optional title prefix (lovag, ifj., id., özv.)
_OPT_TITLE = rf"(?:{a.TITLE}\s+)?"

# "Zahler [István/Miksa]" with optional title and -né suffix
ZAHLER_FULL = rf"""
    \b
    {_OPT_TITLE}
    {a.ZAHLER}
    (?:{a.NAME_SEP}(?:{a.ISTVÁN}|{a.MIKSA}){a.NÉ_SUFFIX}?)?
    \b
"""

# "Breuer [Mihály/Gyula/Lili]" with optional title, ownership, -né
BREUER_FULL = rf"""
    \b
    {_OPT_TITLE}
    {a.BREUER}
    (?:{a.NAME_SEP}{a.GIVEN_NAME}{a.NÉ_SUFFIX}?)?
    (?:{a.NAME_SEP}{a.NYOMDATULAJDONOS})?
    \b
"""

# Joint attribution: "Zahler–Breuer" or "Zahler és Breuer" (any separator style)
ZAHLER_BREUER_JOINT = rf"""
    \b
    {_OPT_TITLE}
    {a.ZAHLER}
    {a.NAME_SEP} (?:[-–—]|{a.ES_CONJUNCTION})? {a.NAME_SEP}
    {a.BREUER}
    \b
"""

# Partnership forms: "Zahler és Társa", "Breuer Testvérek"
PARTNERSHIP = rf"""
    \b
    (?:{a.ZAHLER}|{a.BREUER})
    {a.NAME_SEP}
    (?:{a.ÉS_TÁRSA}|{a.TESTVÉREK}|{a.RÉSZVÉNYTÁRSASÁG})
    \b
"""

# Any of the printer names (joint first for greedy precedence)
ANY_PRINTER = rf"""
    (?:
        {ZAHLER_BREUER_JOINT}
      | {PARTNERSHIP}
      | {ZAHLER_FULL}
      | {BREUER_FULL}
    )
"""


# =============================================================================
# MARRIED NAME — the -né pattern for identity resolution
# =============================================================================

# Captures "Surname Givenné" — e.g. "Zahler Istvánné"
# This is a relational marker: the person is the WIFE of [Surname Given]
MARRIED_NAME = rf"""
    \b
    {_OPT_TITLE}
    (?:{a.ZAHLER}|{a.BREUER})
    \s+
    {a.GIVEN_NAME}
    {a.NÉ_SUFFIX}
    \b
"""


# =============================================================================
# PRINTER + ESTABLISHMENT — a printer name appearing near an establishment term
# =============================================================================

PRINTER_NEAR_ESTABLISHMENT = rf"""
    {ANY_PRINTER}
    .{{0,80}}
    {ANY_ESTABLISHMENT}
"""

# Legacy alias — used in registry
PRINTER_NEAR_NYOMDA = PRINTER_NEAR_ESTABLISHMENT


# =============================================================================
# PRINTER + LOCATION — a printer name near a city (with or without establishment)
# Covers cases like "BREUER MIHÁLY BPEST"
# =============================================================================

PRINTER_NEAR_CITY = rf"""
    {ANY_PRINTER}
    .{{0,40}}                                # allow given name, commas, etc. between
    (?:{a.BUDAPEST}|{a.VIENNA})
"""


# =============================================================================
# ADDRESSES
# =============================================================================

# Generic street address: [District] Street-name utca/utcza/u. [number]
GENERIC_ADDRESS = rf"""
    (?:{a.DISTRICT} {a.NAME_SEP})?        # optional district
    \b[\p{{L}}][\p{{L}}\-]{{2,20}}\b       # street name (2-20 letter chars)
    [ \-]?
    {a.UTCA}                                # utca/utcza/u.
    (?:[ ]?\d{{1,3}}\.?)?                   # optional house number
"""

# Lovag utca with house number (2 or 16), optional district prefix
LOVAG_ADDRESS = rf"""
    (?:{a.DISTRICT_VI} {a.NAME_SEP})?
    {a.LOVAG}
    [ \-]?
    {a.UTCA}
    [ ]?
    (?:2|16)
    \b
"""

# Nagymező utca 43 (Breuer Mihály's lithography workshop)
NAGYMEZŐ_ADDRESS = rf"""
    {a.NAGYMEZŐ}
    [ \-]?
    {a.UTCA}
    [ ]?
    43
    \b
"""

# Generic "Budapest [District]" (when no street specified)
BUDAPEST_DISTRICT = rf"""
    \b
    {a.BUDAPEST}
    {a.NAME_SEP}
    {a.DISTRICT}
    \b
"""

# Specifically District VI (the most common for this network)
BUDAPEST_DISTRICT_VI = rf"""
    \b
    {a.BUDAPEST}
    {a.NAME_SEP}
    {a.DISTRICT_VI}
    \b
"""


# =============================================================================
# CONTEXTUAL / RELATIONAL
# =============================================================================

# Hungária bulletin context — publication name near a printer reference
HUNGÁRIA_CONTEXT = rf"""
    \b
    Hung[aá]ri[ao]a?
    \b
    .{{0,120}}
    (?:{BREUER_FULL} | {ANY_ESTABLISHMENT})
"""

# Ownership statement: "Breuer Mihály ... nyomdatulajdonos"
OWNER_STATEMENT = rf"""
    \b
    {a.BREUER}
    {a.NAME_SEP}
    {a.MIHÁLY}
    .{{0,40}}
    \b{a.NYOMDATULAJDONOS}\b
"""

# Fotoművészeti Hírek context (the 1923 publication from the title page)
FOTOMŰVÉSZETI_CONTEXT = rf"""
    \b
    [Ff]otom[űu]v[ée]szeti
    \b
    .{{0,80}}
    (?:{ANY_PRINTER} | {ANY_ESTABLISHMENT})
"""
