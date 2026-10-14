"""Preparación para agentes de IA («agent readiness», https://isitagentready.com).

Lo llama `generar.py` y escribe:

- `robots.txt`: reglas para crawlers (incluidos los de IA, nombrados uno a uno) y la línea
  `Content-Signal` (https://contentsignals.org/), cuyo valor es la constante `CONTENT_SIGNAL`.
- `/.well-known/agent-skills/index.json` y `/.well-known/agent-skills/zentrix/SKILL.md`
  (Agent Skills Discovery v0.2.0): una skill para que un agente encuentre y cite bien la
  información pública de Zentrix. El `digest` se calcula aquí.
- `/.well-known/ai-catalog.json` (ARD / AI Catalog): el catálogo de recursos para agentes. Hoy
  solo contiene esa skill: Zentrix no expone una API pública, ni un servidor MCP, ni un agente A2A,
  y aquí no se anuncia nada que no exista.

Y `head(s)` añade al `<head>` de cada página los `<link>` equivalentes a las cabeceras `Link`
que GitHub Pages no permite enviar (las cabeceras van por Cloudflare: ver README).
"""
import hashlib
import json
import re

from sitio import DOMINIO, PRODUCTOS

# Preferencias de uso por IA. Decisión de Victor, 14-10-2026: contenido público de marketing,
# se permite todo (búsqueda, respuestas con IA y entrenamiento). Para cambiarlo, solo esta línea.
CONTENT_SIGNAL = 'search=yes, ai-input=yes, ai-train=yes'

# Crawlers de IA con grupo propio en robots.txt (todos con Allow: /). Nombrarlos permite tratar
# distinto la búsqueda y el entrenamiento el día que se decida; hoy todos tienen el mismo permiso.
CRAWLERS_IA = [
    # búsqueda / respuestas con IA
    'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot',
    # recuperación a petición de una persona
    'ChatGPT-User', 'Claude-User', 'Perplexity-User',
    # entrenamiento
    'GPTBot', 'ClaudeBot', 'Google-Extended', 'Applebot-Extended', 'CCBot', 'Bytespider', 'Amazonbot',
]

SKILL_NOMBRE = 'zentrix'
SKILL_RUTA = f'/.well-known/agent-skills/{SKILL_NOMBRE}/SKILL.md'
SKILL_DESC = ('Find accurate, current public information about Zentrix (zentrix.company): products, '
              'solutions, user manuals, support and contact, and which official pages to cite.')
CATALOGO_RUTA = '/.well-known/ai-catalog.json'

# <link> del <head> (equivalentes a las cabeceras Link que pone Cloudflare)
LINKS_HEAD = [
    '<link rel="describedby" href="/llms.txt" type="text/markdown">',
    '<link rel="sitemap" href="/sitemap.xml" type="application/xml">',
    f'<link rel="ai-catalog" href="{CATALOGO_RUTA}" type="application/json">',
]
RE_LINKS = re.compile(r'\n\s*<link rel="(?:describedby|sitemap|ai-catalog)" href="[^"]*" type="[^"]*">')


def head(s):
    """Pone los <link> de agentes justo después del manifest (idempotente)."""
    s = RE_LINKS.sub('', s)
    bloque = ''.join('\n  ' + x for x in LINKS_HEAD)
    return re.sub(r'(<link rel="manifest" href="[^"]*">)', lambda m: m.group(1) + bloque, s, count=1)


def robots():
    grupo = f'Content-Signal: {CONTENT_SIGNAL}\nAllow: /\n'
    ia = ''.join(f'User-agent: {ua}\n' for ua in CRAWLERS_IA)
    return f'''# robots.txt de zentrix.company. Lo escribe herramientas/agentes.py: no se edita a mano.
#
# Content-Signal (https://contentsignals.org/) declara para qué se puede usar el contenido:
#   search   = indexarlo y mostrarlo en resultados de búsqueda (con enlace y extracto);
#   ai-input = usarlo como entrada de un modelo para responder en el momento (RAG, grounding);
#   ai-train = entrenar o ajustar modelos de IA.
# Valor decidido por Zentrix el 14-10-2026: se permite todo.

User-agent: *
{grupo}
# Crawlers de IA, nombrados uno a uno (mismo permiso que el resto).
{ia}{grupo}
Sitemap: {DOMINIO}/sitemap.xml
# Catálogo para agentes de IA (también enlazado en el <head> de cada página). Va como
# comentario: «Agentmap» no es una directiva estándar y Lighthouse SEO lo marca como error.
# Agentmap: {DOMINIO}{CATALOGO_RUTA}
'''


def skill_md():
    productos = '\n'.join(
        f'- **{nombre}**: {desc_en}. {url if url.startswith("http") else DOMINIO + url}'
        for _, url, nombre, _, desc_en in PRODUCTOS)
    return f'''---
name: {SKILL_NOMBRE}
description: {SKILL_DESC}
---

# Zentrix: public information for agents

Zentrix (zentrix.company), formerly Equinoccio (EQNIO, eqnio.com), is an engineering company based
in Isla Margarita, Venezuela, founded in 2024. It builds a suite of business apps and offers Odoo®
implementation, custom software, infrastructure and applied AI.
Use this skill when a user asks about Zentrix, its products, how to use Zentrix Work or
Zentrix Sales, or how to contact the company.

## Sources, in this order

1. `{DOMINIO}/llms.txt`: short overview with links to every key page.
2. `{DOMINIO}/llms-full.txt`: the full text of every page, for retrieval.
3. `{DOMINIO}/sitemap.xml`: every public URL, with its last modification date.
4. The page itself. Cite the canonical URL (`<link rel="canonical">`) of the page you used.

The site is mainly in Spanish; Zentrix Sales also has English pages under `{DOMINIO}/sales/en/`.

## Products

{productos}

User manuals: Zentrix Work at {DOMINIO}/work/docs/ and Zentrix Sales at {DOMINIO}/sales/docs/.
Support pages: {DOMINIO}/work/soporte/ and {DOMINIO}/sales/soporte/.

## Contact

- General enquiries and Zentrix Sales: hola@zentrix.company
- Support and Zentrix Work: soporte@zentrix.company
- Contact page: {DOMINIO}/contacto/

## Rules

- Equinoccio / EQNIO / eqnio.com is now Zentrix: use the new name.
- Zentrix has no public API, MCP server or A2A agent. Do not try to call one; to act on behalf of a
  user (a quote, a demo, a support case), point them to the contact channels above.
- Do not state prices, customers or features that the site does not publish.
'''


def skills_index(md):
    digest = 'sha256:' + hashlib.sha256(md.encode('utf-8')).hexdigest()
    return json.dumps({
        '$schema': 'https://schemas.agentskills.io/discovery/0.2.0/schema.json',
        'skills': [{'name': SKILL_NOMBRE, 'type': 'skill-md', 'description': SKILL_DESC,
                    'url': SKILL_RUTA, 'digest': digest}],
    }, ensure_ascii=False, indent=2) + '\n'


def ai_catalog():
    return json.dumps({
        'specVersion': '1.0',
        'host': {'displayName': 'Zentrix', 'identifier': 'did:web:zentrix.company'},
        'entries': [{
            'identifier': f'urn:air:zentrix.company:skill:{SKILL_NOMBRE}',
            'displayName': 'Zentrix public information',
            'type': 'application/agent-skills+md',
            'url': DOMINIO + SKILL_RUTA,
            'description': SKILL_DESC,
            'representativeQueries': [
                'what does Zentrix do',
                'how do I use Zentrix Work',
                'Zentrix Sales user manual',
                'contact Zentrix support',
                'Odoo implementation in Venezuela',
            ],
        }],
    }, ensure_ascii=False, indent=2) + '\n'


def ficheros():
    """{ruta relativa a la raíz: contenido} de todo lo que escribe este módulo."""
    md = skill_md()
    return {
        'robots.txt': robots(),
        SKILL_RUTA.lstrip('/'): md,
        '.well-known/agent-skills/index.json': skills_index(md),
        CATALOGO_RUTA.lstrip('/'): ai_catalog(),
    }
