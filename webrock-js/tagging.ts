import { TagNames, WEBROCK_ID, WEBROCK_SELECTOR, everythingElseColor, tagAnnotationColors } from './constants';
import { getElementXPath } from './elements';
import { AnchorTag, InputTag, Tag } from './types/tags';

type StyleDeclaration = Partial<CSSStyleDeclaration>;

function createSpanStyle(color: string): StyleDeclaration {
  return {
    position: 'absolute',
    top: '0',
    right: '0',
    color: 'white',
    padding: '0 2px',
    backgroundColor: color,
  };
}

function createDivStyle(color: string, rect: DOMRect): StyleDeclaration {
  return {
    position: 'absolute',
    width: `${rect.width}px`,
    height: `${rect.height}px`,
    fontSize: '100%',
    left: `${rect.left}px`,
    top: `${rect.top}px`,
    zIndex: '-1',
    boxSizing: 'border-box',
    border: `2px solid ${color}`,
  };
}

function getColorForElement(el: HTMLElement) {
  if (el.tagName in tagAnnotationColors) {
    return tagAnnotationColors[el.tagName];
  }

  return everythingElseColor;
}

function createTagFromElement(el: HTMLElement, idNum: number): Tag {
  const tag: Tag = {
    xpath: getElementXPath(el),
    tagName: el.tagName,
    idNumber: idNum,
    innerText: el.innerText,
  };

  if (el.tagName === TagNames.INPUT) {
    const inputElement = el as HTMLInputElement;
    const inputTag: InputTag = {
      ...tag,
      value: inputElement.value,
      type: inputElement.type,
      placeholder: inputElement.placeholder,
      ariaLabel: inputElement.ariaLabel ? inputElement.ariaLabel : undefined,
    };
    return inputTag;
  } else if (el.tagName === TagNames.A) {
    const anchorElement = el as HTMLAnchorElement;
    const anchorTag: AnchorTag = {
      ...tag,
      role: anchorElement.role ? anchorElement.role : undefined
    }
    return anchorTag
  } else {
    return tag;
  }
}

export function tagElements(elementsToTag: HTMLElement[]): Record<number, Tag> {
  const idToTag = {};

  elementsToTag.forEach((el, i) => {
    const tag = createTagFromElement(el, i);
    idToTag[i] = tag;
    createAnnotation(el, i);

  })

  // Make all annotations previously created visible
  const tags: NodeListOf<HTMLElement> = document.querySelectorAll(WEBROCK_SELECTOR);

  tags.forEach((el: HTMLElement) => {
    el.style.zIndex = '999999999';
  });

  return idToTag;
}

export function createAnnotation(el: HTMLElement, idNumber: number) {
  // Get the appropriate color for the element
  const color = getColorForElement(el);

  const rect = el.getBoundingClientRect();

  // Create a new div and assign it our id
  const div = document.createElement('div');
  div.id = WEBROCK_ID;
  Object.assign(div.style, createDivStyle(color, rect));

  // Create a span with the idNumber and put it in the top right corner of the div
  const span = document.createElement('span');
  Object.assign(span.style, createSpanStyle(color));
  span.innerText = idNumber.toLocaleString();

  div.appendChild(span);
  document.body.appendChild(div);
  return div;
}
