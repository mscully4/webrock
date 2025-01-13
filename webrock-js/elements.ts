import { Logger, ILogObj } from 'tslog';
import { elementIsVisible } from './locator';

const log: Logger<ILogObj> = new Logger();

export function getAllElementsInAllFrames(): HTMLElement[] {
  // Main page
  const allElements: HTMLElement[] = Array.from(document.body.querySelectorAll('*'));

  // Add all elements in iframes
  // NOTE: This still doesn't work for all iframes
  const iframes = document.getElementsByTagName('iframe');
  for (let i = 0; i < iframes.length; i++) {
    try {
      const frame = iframes[i];
      const iframeDocument = frame.contentDocument || frame.contentWindow?.document;
      if (!iframeDocument) continue;

      const iframeElements = Array.from(iframeDocument.querySelectorAll('*')) as HTMLElement[];
      iframeElements.forEach((el) => el.setAttribute('iframe_index', i.toString()));
      allElements.push(...iframeElements);
    } catch (e) {
      console.error('Error accessing iframe content:', e);
    }
  }

  return allElements;
}

const EMPTY_TAG_WHITELIST = ['input', 'textarea', /*'select',*/ 'button'];

/**
 * A function that determines whether an element is empty
 * @param el
 * @returns
 */
function elementIsNotEmpty(el: HTMLElement): boolean {
  const tagName = el.tagName.toLowerCase();

  return EMPTY_TAG_WHITELIST.includes(tagName) || el.childElementCount > 0 || el.innerText.trim().length > 0
}

const INTERACTABLE_ELEMENTS = ['a', 'button', 'textarea', /* "select",*/ 'details', 'label'];

/**
 * A function that determines whether a user can interact with an element
 * @param el the element to check
 * @returns boolean
 */
function isInteractable(el: HTMLElement): boolean {
  // If it is a label but has an input child that it is a label for, say not interactable
  if (el.tagName.toLowerCase() === 'label' && el.querySelector('input')) {
    return false;
  }

  if (el.getAttribute('onClick') != null) {
    return true;
  }

  return (
    INTERACTABLE_ELEMENTS.includes(el.tagName.toLowerCase()) ||
    // @ts-expect-error IDK
    (el.tagName.toLowerCase() === 'input' && el.type !== 'hidden') ||
    el.role === 'button'
  );
}

function elementIsNotHidden(el: HTMLElement) {
  const rect = el.getBoundingClientRect();
  const computedStyle = window.getComputedStyle(el);

  const isHidden =
    computedStyle.visibility === 'hidden' ||
    computedStyle.display === 'none' ||
    el.hidden ||
    (el as HTMLButtonElement).disabled;

  const isTransparent = computedStyle.opacity === '0';
  const isZeroSize = rect.width === 0 || rect.height === 0;
  const isScriptOrStyle = el.tagName === 'SCRIPT' || el.tagName === 'STYLE';
  return !isHidden && !isTransparent && !isZeroSize && !isScriptOrStyle;
}

/**
 * A function to filter a list of elements down to just elements that should be tagged
 * @param allElements
 * @param tagLeafTexts
 * @returns
 */
export function getElementsToTag(allElements: HTMLElement[], tagLeafTexts: boolean): HTMLElement[] {
  return allElements
    .filter(el => isInteractable(el))
    .filter(el => elementIsNotEmpty(el))
    .filter(el => elementIsNotHidden(el))
    .filter(el => elementIsVisible(el))
}

export function removeNestedTags(elementsToTag: HTMLElement[]): HTMLElement[] {
  // An interactable element may have multiple tagged elements inside
  // Most commonly, the text will be tagged alongside the interactable element
  // In this case there is only one child, and we should remove this nested tag
  // In other cases, we will allow for the nested tagging

  const res = [...elementsToTag];
  elementsToTag.map((el) => {
    // Only interactable elements can have nested tags
    if (isInteractable(el)) {
      const elementsToRemove: HTMLElement[] = [];
      el.querySelectorAll('*').forEach((child) => {
        const index = res.indexOf(child as HTMLElement);
        if (index > -1) {
          elementsToRemove.push(child as HTMLElement);
        }
      });

      // Only remove nested tags if there is only a single element to remove
      if (elementsToRemove.length == 1) {
        for (const element of elementsToRemove) {
          res.splice(res.indexOf(element), 1);
        }
      }
    }
  });

  return res;
}

export function getElementXPath(element: HTMLElement | null) {
  const path_parts: string[] = [];

  let iframe_str = '';
  if (element && element.ownerDocument !== window.document) {
    // assert element.iframe_index !== undefined, "Element is not in the main document and does not have an iframe_index attribute";
    iframe_str = `iframe[${element.getAttribute('iframe_index')}]`;
  }

  while (element) {
    if (!element.tagName) {
      element = element.parentNode as HTMLElement | null;
      continue;
    }

    let prefix = element.tagName.toLowerCase();
    let sibling_index = 1;

    let sibling = element.previousElementSibling;
    while (sibling) {
      if (sibling.tagName === element.tagName) {
        sibling_index++;
      }
      sibling = sibling.previousElementSibling;
    }

    // Check next siblings to determine if index should be added
    let nextSibling = element.nextElementSibling;
    let shouldAddIndex = false;
    while (nextSibling) {
      if (nextSibling.tagName === element.tagName) {
        shouldAddIndex = true;
        break;
      }
      nextSibling = nextSibling.nextElementSibling;
    }

    if (sibling_index > 1 || shouldAddIndex) {
      prefix += `[${sibling_index}]`;
    }

    if (element.id) {
      prefix += `[@id="${element.id}"]`;

      // If the id is unique and we have enough path parts, we can stop
      if (path_parts.length > 3) {
        path_parts.unshift(prefix);
        return '//' + path_parts.join('/');
      }
    } else if (element.className) {
      prefix += `[@class="${element.className}"]`;
    }

    path_parts.unshift(prefix);
    element = element.parentNode as HTMLElement | null;
  }
  return iframe_str + '//' + path_parts.join('/');
}
