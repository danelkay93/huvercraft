"""
Atomic regex fragments for Hungarian printer-name matching.

These are the smallest reusable building blocks. Each fragment captures
ONE linguistic or typographic concept. They get composed into full
patterns in `composed.py`.

All patterns use `regex` V1 verbose mode. Do NOT compile these directly—
they are raw strings meant to be interpolated into larger patterns.
"""

# =============================================================================
# NYOMDA (printing house) — the shared suffix
# =============================================================================

# Core word with optional possessive/locative/agentive suffixes
# nyomda, nyomdája, nyomdájában, nyomdai, nyomdász, nyomdáját
NYOMDA_STEM = r"nyomd[aáâ](?:j[aá])?(?:b[ae]n|i|sz|[ij]?[aá]t)?"

# Abbreviated form — requires period to avoid matching inside "könyv"
NYOMDA_ABBREV = r"ny\."

# Any form of the nyomda stem
NYOMDA = rf"(?:{NYOMDA_STEM}|{NYOMDA_ABBREV})"


# =============================================================================
# ESTABLISHMENT TERMS — alternatives to "nyomda"
# =============================================================================

# műintézet: "art institute" — high-end lithographic shops
# intézete (possessive: "his/her institute")
MŰINTÉZET = r"m[űu]int[ée]zet[eé]?"

# műkiadó: "art publisher" — prestige term for litho/postcard/poster houses
MŰKIADÓ = r"m[űu]kiad[oó](?:j[aá])?"

# nyomat: "a print/impression" (the product, not the shop)
NYOMAT = r"nyomat(?:ai?|ok)?"

# litográfia / lithographia: direct loanwords
LITOGRÁFIA = r"l[iy]th?ogr[aá](?:phi|fi)[aá](?:i|j[aá])?"

# typographia: letterpress loanword
TYPOGRAPHIA = r"typ?ogr[aá](?:phi|fi)[aá](?:i|j[aá])?"

# fióknyomda: branch printing office
FIÓKNYOMDA = rf"fi[oó]k{NYOMDA_STEM}"

# Any establishment term (including nyomda itself)
ESTABLISHMENT = rf"""(?:
    {NYOMDA_STEM}
  | {MŰINTÉZET}
  | {MŰKIADÓ}
  | {LITOGRÁFIA}
  | {TYPOGRAPHIA}
  | {FIÓKNYOMDA}
)"""

# Ownership descriptor
NYOMDATULAJDONOS = r"nyomdatulajdonos"

# "nyomdász" — printer (the person, agentive)
NYOMDÁSZ = r"nyomd[aá]sz"


# =============================================================================
# PREFIXES — what kind of printing house
# =============================================================================

# Lithographic / stone printing (kő-, litho-, lithográf-)
PREFIX_LITHO = r"(?:k[őöo]|litho(?:gr(?:[aá]f)?)?)"

# Book printing (könyv-)
PREFIX_BOOK = r"(?:k[öo]nyv)"

# Music printing (zenemű-)
PREFIX_MUSIC = r"(?:zenem[űu])"

# Quick printing (gyors-)
PREFIX_QUICK = r"(?:gyors)"

# Advertising printing (reklám-)
PREFIX_ADVERT = r"(?:rekl[aá]m)"

# Colour printing (színes-)
PREFIX_COLOUR = r"(?:sz[ií]nes)"

# "Magyar" national branding prefix
PREFIX_MAGYAR = r"(?:Magyar)"

# Any prefix for compound nyomda forms
PREFIX_ANY = rf"(?:{PREFIX_LITHO}|{PREFIX_BOOK}|{PREFIX_MUSIC}|{PREFIX_QUICK}|{PREFIX_ADVERT}|{PREFIX_COLOUR}|{PREFIX_MAGYAR})"


# =============================================================================
# CONNECTORS — how words join in Hungarian compounds
# =============================================================================

# Flexible hyphen/dash with optional surrounding space
HYPHEN_FLEX = r"[ ]?[-–—][ ]?"

# "és" (and) / ampersand with flexible spacing
ES_CONJUNCTION = r"(?:[ée]s|&)[ ]?"

# Separator between name parts (space, comma, period, hyphen)
NAME_SEP = r"[ ,.\-]*"


# =============================================================================
# HUNGARIAN TITLES & HONORIFICS
# =============================================================================

# Pre-name titles found in printing records
# lovag (Knight), ifj. (Junior), id. (Senior), özv. (Widow)
TITLE = r"(?:(?:lovag|ifj|id|[öo]zv)\.?)"


# =============================================================================
# THE -NÉ SUFFIX — married-name marker
# =============================================================================

# -né / -neé: appended to husband's given name to form wife's legal name
# "Zahler Istvánné" = "Mrs. István Zahler"
NÉ_SUFFIX = r"n[eé](?:nek)?"


# =============================================================================
# PARTNERSHIP TERMS
# =============================================================================

# "és Társa" / "és Társai" — "and Partner(s)"
ÉS_TÁRSA = r"[ée]s[ ]?T[aá]rs(?:a(?:i)?|uk)"

# "Testvérek" — "Brothers" (e.g., Légrády Testvérek)
TESTVÉREK = r"Testv[eé]rek"

# Részvénytársaság — "Joint-stock company" (Rt.)
RÉSZVÉNYTÁRSASÁG = r"(?:R[eé]szv[eé]nyt[aá]rsas[aá]g|Rt\.?)"


# =============================================================================
# STREET NAME ATOMS
# =============================================================================

# "utca" with historical spelling variants (utca, utcza, u., ut)
UTCA = r"(?:u(?:tc[ae]|cz[ae])?\.?|ut\.?)"

# Known streets for this printer network
LOVAG = r"Lovag"
NAGYMEZŐ = r"Nagymez[őo]"
VÁCZI = r"V[aá]c[zi]i?"

# District in Roman numerals with optional "ker." (kerület)
DISTRICT = r"(?:[IVXLCDM]+\.?(?:[ ]?ker\.?)?)"

# District VI specifically
DISTRICT_VI = r"(?:VI\.?(?:[ ]?ker\.?)?|6\.?)"


# =============================================================================
# CITY / LOCATION ATOMS
# =============================================================================

# Budapest with common abbreviations found in historical prints
# Budapest, Bpest, Bp., Bp, B-pest, BPEST, B.pest
BUDAPEST = r"(?:Budapest|B[\.\-]?pest|Bp\.?)"

# Vienna equivalents (for cross-border tracking)
VIENNA = r"(?:B[eé]cs|Wien)"


# =============================================================================
# PRINTER NAME ATOMS — surnames with OCR/orthographic tolerance
# =============================================================================

# Zahler — stable across records
ZAHLER = r"Zahler"

# Breuer / Breier — eu↔ei vowel swap common in Germanic-Jewish names
BREUER = r"Br(?:eu|ei|eü)er"


# =============================================================================
# FIRST NAMES — Hungarian ↔ Germanic cross-border equivalences
# =============================================================================

# István / Stefan / Stephan
ISTVÁN = r"(?:Istv[aá]n|Stef[aá]n|Stephan)"

# Mihály / Michael
MIHÁLY = r"(?:Mih[aá]ly|Michael)"

# Gyula / Julius
GYULA = r"(?:Gyul[aá]|Julius)"

# Miksa / Max / Maximilian
MIKSA = r"(?:Miks[aá]|Max(?:imilian)?)"

# Lili / Lilly / Lily / Lille / Lilli
LILI = r"(?:Lil[ily]{1,2}|Lille)"

# Any known first name in this network
GIVEN_NAME = rf"(?:{ISTVÁN}|{MIHÁLY}|{GYULA}|{MIKSA}|{LILI})"
