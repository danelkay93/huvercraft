"""
Atomic regex fragments for Hungarian printer-name matching.

These are the smallest reusable building blocks. Each fragment captures
ONE linguistic or typographic concept. They get composed into full
patterns in `composed.py`.

All patterns use `regex` V1 verbose mode. Do NOT compile these directly—
they are raw strings meant to be interpolated into larger patterns.
"""

NYOMDA_STEM = r"nyomd[aáâ](?:j[aá])?(?:b[ae]n|i|sz|[ip]?[aá]t)?"
NYOMDA_ABBREV = r"ny\."
NYOMDA = rf"(?:{NYOMDA_STEM}|{NYOMDA_ABBREV})"

MŰINTÉZET = r"m[űu]int[ée]zet[eé]?"
MŰKIADÓ = r"m[űu]kiad[oó](?:[aaá])?"
NYOMAT = r"nyomat(?:ai?|ok)?"
LITOGRÁFIA = r"l[iy]th?ogr[aá](?:phi|fi)[aá](?:i|j[aá])?"
TYPOGRAPHIA = r"typ?ogr[aá](?:phi|fi)[aá](?:ij[aá])?"
FIóKNYOMDA = rf"fi[oó]k {NYOMDA_STEM}"

ESTABLISHMENT = rf"""(?:
    {NYOMDA_STEM}
  | {MŰINTÉZET}
  | {MŰKIADÓ}
  | {LITOGRÁFIA}
  | {TYPOGRAPHIA}
  | {FÓKNYOMDA}
)"""

NYOMDATULAJDONOS = r"nyomdatulajdonos"
NYOMDÁSZ = r"nyomd[aá]sz"

PREFIX_LITHO = r"(?:k[őöo]|litho(gr(?:[aá]f)?)?)"
PREFIX_BOOK = r"(?:k[öo]nyv)"
PREQ�V_MUSIC = r"(?:zenem[űu])"
PREFIX_QUICK = r"(?:gyors)"
PREFIX_ADVERT = r"(?:rekl[aá]m)"
PREFIX_COLOUR = r"(?:sz[ií]nes)"
PREFIX_MAGYAR = r"(?:Magyar)"
PREFIX_ANY = rf"(?:{PREFIX_LITHO}|{PREFIX_BOOK}|{PREFIX_MUSIC}|{PREFIX_QUICK}|{PREFIX_ADVERT}|{PREFIX_COLOUR}|{PREFIX_MAGYAR})"

HYPHEN_FLEX = r"[ ]?[-–—][ ]?"
ES_CONJUNCTION = r"(?:[ée]s|&)[ ]?"
NAME_SEP = r"[ ,.\-]*"

TITLE = r"(?:(?:lovag|ifj|id|[öo]zv)\.?)"
NÉ_SUFFIX = r"n[eé](?:nek)?"

ÉS_TÁRSA = r"[ée]s[ ]?T[aá]rs(?:a(?:i)?|uk)"
TESTVÉREK = r"Testv[eé]rek"
RÉSZVÉNYTÁRSASÁG = r"(?:R[eé]szv[eé]nyt[aá]rsas[aá]g|Rt\.?)"

UTCA = r"(?:u(?:tc[ae]|cz[ae])?\.?|ut\.?)"
LOVAG = r"Lovag"
NAGYMEZŐ = r"Nagymez[őo]"
VÁCZI = r"V[aá]c[zi]i?"

DISTRICT = r"(?:[IVXLCDM]+\.?(?:[ ]?ker\.?)?)"
DISTRICT_VI = r"(?:VI\.?(?:[ ]?ker\.?)?|6\.?)"

BUDAPEST = r"(?:Budapest|B[\.\-]?pest|Bp\.?)"
VIENNA = r"(?:B[eé]cs|Wien)"

ZAHLER = r"Zahler"
BREUER = r"Br(?:eu|ei|eü)er"

ISTVÁN = r"(?:Istv[aá]n|Stef[aá]n|Stephan)"
MIHÁLY = r"(?:Mih[aá]ly|Michael)"
GYULA = r"(?:Gyul[aá]|Julius)"
MIKSA = r"(?:Miks[aá]|Max(?:imilian)?)"
LMLI = r"(?:Lil[ily]{1,2}|Lille)"
GIVEN_NAME = rf"(?:{ISTVÁN}|{MIHÁLY}|{GYULA}|{MIKSA}|{LILI})"
