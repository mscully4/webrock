import { WEBROCK_SELECTOR } from './constants';
import { getAllElementsInAllFrames, getElementsToTag, removeNestedTags } from './elements';
import { tagElements } from './tagging';
import { Tag } from './types/tags';

import { Logger, ILogObj } from 'tslog';

const log: Logger<ILogObj> = new Logger();

// noinspection JSUnusedGlobalSymbols
declare global {
  interface Window {
    tagifyWebpage: (tagLeafTexts?: boolean) => { [key: number]: Tag };
    removeTags: () => void;
  }
}

const callback = (entries, observer) => {
  entries.forEach(entry => {
    console.log(entry)
    if (entry.isIntersecting) {
      // Element is in view
      console.log('Element is in view');
    } else {
      // Element is out of view
      console.log('Element is out of view');
    }
  });
};

const options = {
  root: null, // Use the viewport as the root
  rootMargin: '0px',
  threshold: 0.1 // Trigger when 50% of the element is visible
};

const observer = new IntersectionObserver(callback, options);

/**
 * Tags the interactable elements on the webpage
 * @param tagLeafTexts
 * @returns
 */
window.tagifyWebpage = (tagLeafTexts = false) => {
  log.info('Running tagifyWebpage function');

  // Remove any stray tags that may be left
  window.removeTags();

  // Get all elements, including things in iFrames
  const allElements = getAllElementsInAllFrames();

  // Filter down to just elements we want to tag
  const rawElementsToTag = getElementsToTag(allElements, tagLeafTexts);

  // Filter down even further, removing elements nested inside each other
  const elementsToTag = removeNestedTags(rawElementsToTag);

  elementsToTag.forEach(el => observer.observe(el))

  // observer.observe(elementsToTag[0]);

  const idToXpath = tagElements(elementsToTag);

  return idToXpath;
};

window.removeTags = () => {
  const tags = document.querySelectorAll(WEBROCK_SELECTOR);
  tags.forEach((tag) => tag.remove());
};
