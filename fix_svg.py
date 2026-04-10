import os
import xml.etree.ElementTree as ET
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def process(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception:
        logging.warning(f'{path}: parse failed')
        return
    if not root.tag.endswith('svg'):
        logging.warning(f'{path}: not svg root')
        return
    width = root.get('width')
    height = root.get('height')
    if width and height:
        logging.info(f'{path}: already has width/height')
        return
    viewbox = root.get('viewBox')
    if not viewbox:
        logging.warning(f'{path}: no viewBox')
        return
    parts = viewbox.split()
    if len(parts) != 4:
        logging.warning(f'{path}: invalid viewBox')
        return
    _, _, w, h = parts
    root.set('width', w)
    root.set('height', h)
    tree.write(path)
    logging.info(f'{path}: updated')


def main(target_dir='docs/images/'):
    for fname in os.listdir(target_dir):
        if not fname.endswith('.svg'):
            continue
        process(os.path.join(target_dir, fname))


if __name__ == '__main__':
    main()
