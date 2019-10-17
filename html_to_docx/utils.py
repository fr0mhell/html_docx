import re

from docx.document import Document
from lxml import etree


def into_paragraphs(element):
    """Transforms Elements into paragraphs to convert them correctly. """
    if element_is_paragraph(element):
        return element

    if element.tag == 'div':
        if all([element_is_paragraph(el) for el in element.getchildren()]):
            return element
        element.tag = 'p'
        return element

    parent = etree.Element('p')
    parent.append(element)
    return parent


def element_is_paragraph(element):
    """Checks that HTML element is a paragraph."""
    return element.tag in [
        'p',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote',
        'li',
        'code',
    ]


def parse_style(element):
    """Parse `style` attribute of HTML element.

    Args:
        element (HtmlElement): HTML element which style need to be parsed.

    Returns:
        style (dict): Parsed style parameters.

    """
    style_string = element.attrib.get('style', '')

    style = dict()
    style.update(parse_font_size(style_string))

    return style


def parse_font_size(style_string):
    """Parse `font-size` from HTML.style attribute.

    Args:
        style_string (str): Value of `style` attribute of HTML element.

    Returns:
        style (dict): Font size defined in HTML element.

    """
    font_size_re = re.compile(r'font\-size:\s*(?P<font_size>\d*)px')
    match = font_size_re.match(style_string)

    if not match:
        return dict()

    style = match.groupdict()
    style['font_size'] = int(style['font_size'])
    return style


def get_document(container):
    """Get `Document` instance of any docx container."""
    if isinstance(container, Document):
        return container

    return get_document(container._parent)


def get_or_add_style(document, style_name, style_type):
    """Get existent or create new style for a document.

    Args:
        document (Document): DOCX document.
        style_name (str): Name of DOCX style.
        style_type (int): Type of DOCX style. Taken from
            `docx.enum.style.WD_STYLE_TYPE`.

    Returns:
        (_CharacterStyle or _ParagraphStyle): New or existent style.

    """
    # `get_by_id` returns default style if a style with defined name not found
    existent_style = document.styles.get_by_id(style_name, style_type)

    if style_name == existent_style.name:
        return existent_style, False

    return document.styles.add_style(style_name, style_type), True