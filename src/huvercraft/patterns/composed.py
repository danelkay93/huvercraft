"""
Composed regex patterns built from atomic fragments.
"""

from . import atoms as a

COMPOUND_NYOMDA = rf"""
    \b
    {a.PREFIX_ANY}
    {a.NYOMDA_STEM}
    \b
"""

ELLIPTICAL_NYOMDA = rf"""
    \b
    {a.PREFIX_ANY} {a.HYPHEN_FLEX}
    (?:{a.ES_CONJUNCTION})?
    (?:{a.PREFIX_ANY} {a.HYPHEN_FLEX})?
    (?:{a.ES_CONJUNCTION})?
    {a.PREFIX_ANY}?
    {a.NYOMDA_STEM}
"""

ANY_NYOMDA = rf"""
    (?:
        {COMPOUND_NYOMDA}
      | {ELLIPTICAL_NYOMDA}
      | \b{a.NYOMDA_STEM}\b
    )
"""

ANY_ESTABLISHMENT = rf"""
    (?:
        {COMPOUND_NYOMDA}
      | {ELLIPTICAL_NYOMDA}
      | \b{a.ESTABLISHMENT}\b
    )
"""

_OPT_TITLE = rf"(?:{a.TITLE}\s+)?"

ZAHLER_FULL = rf"""
    \b
    {_OPT_TITLE}
    {a.ZAHLER}
    (?:{a.NAME_SEP}(?:{a.ISTVÁN}|{a.MIKSA}){a.NÉ_SUFFIX}?)?
    \b
"""

BREUER_FULL = rf"""
    \b
    {_OPT_TITLE}
    {a.BREUER}
    (?:{a.NAME_SEP}{a.GIVEN_NAME}{a.NÉ_SUFFIX}?)?
    (?:{a.NAME_SEP}{a.NYOMDATULAJDONOS})?
    \b
"""

ZAHLER_BREUER_JOINT = rf"""
    \b
    {_OPT_TITLE}
    {a.ZAHLER}
    {a.NAME_SEP} (?:[-–—]|{a.ES_CONJUNCTION})? {a.NAME_SEP}
    {a.BREUER}
    \b
"""

PARTNERSHIP = rf"""
    \b
    (?:{a.ZAHLER}|{a.BREUER})
    {a.NAME_SEP}
    (?:{a.ÉS_TÁRSA}|{a.TESTVÉREK}|{a.RÉSZVÉNYTÁRSASÁG})
    \b
"""

ANY_PRINTER = rf"""
    (?:
        {ZAHLER_BREUER_JOINT}
      | {PARTNERSHIP}
      | {ZAHLER_FULL}
      | {BREUER_FULL}
    )
"""

MARRIED_NAME = rf"""
    \b
    {_OPT_TITLE}
    (?:{a.ZAHLER}|{a.BREUER})
    \s+
    {a.GIVEN_NAME}
    {a.NÉ_SUFFIX}
    \b
"""

PRINTER_NEAR_ESTABLISHMENT = rf"""
    {ANY_PRINTER}
    .{{0,80}}
    {ANY_ESTABLISHMENT}
"""
PRINTER_NEAR_NYOMDA = PRINTER_NEAR_ESTABLISHMENT

PRINTER_NEAR_CITY = rf"""
    {ANY_PRINTER}
    .{{0,40}}
    (?:{a.BUDAPEST}|{a.VIENNA})
"""

GENERIC_ADDRESS = rf"""
    (?:{a.DISTRICT} {a.NAME_SEP})?
    \b[\p{{L}}][\p{{L}}\-]{{2,20}}\b
    [ \-]?
    {a.UTCA}
    (?:[ ]?\d{{1,3}}\.?)?
"""

LOVAG_ADDRESS = rf"""
    (?:{a.DISTRICT_VI} {a.NAME_SEP})?
    {a.LOVAG}
    [ \-]?
    {a.UTCA}
    [ ]?
    (?:2|16)
    \b
"""

NAGYMEZŐ_ADDRESS = rf"""
    {a.NAGYMEZŐ}
    [ \-]?
    {a.UTCA}
    [ ]?
    43
    \b
"""

BUDAPEST_DISTRICT = rf"""
    \b
    {a.BUDAPEST}
    {a.NAME_SEP}
    {a.DISTRICT}
    \b
"""

BUDAPEST_DISTRICT_VI = rf"""
    \b
    {a.BUDAPEST}
    {a.NAME_SEP}
    {a.DISTRICT_VI}
    \b
"""

HUNGÁRIA_CONTEXT = rf"""
    \b
    Hung[aá]ri[ao]a?
    \b
    .{{0,120}}
    (?:{BREUER_FULL} | {ANY_ESTABLISHMENT})
"""

OWNER_STATEMENT = rf"""
    \b
    {a.BREUER}
    {a.NAME_SEP}
    {a.MIHÁLY}
    .{{0,40}}
    \b{a.NYOMDATULAJDONOS}\b
"""

FOTOMŰVÉSZETI_CONTEXT = rf"""
    \b
    [Ff]otom[űu]v[ée]szeti
    \b
    .{{0,80}}
    (?:{ANY_PRINTER} | {ANY_ESTABLISHMENT})
"""
