import { BoxCoords, Coords } from './types/coordinates';

// See: https://stackoverflow.com/a/442474
export function getCoordinatesOfElement(el: HTMLElement): BoxCoords {
  let x = 0;
  let y = 0;
  const rect = el.getBoundingClientRect();
  while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
    x += el.offsetLeft - el.scrollLeft;
    y += el.offsetTop - el.scrollTop;
    el = el.offsetParent as HTMLElement;
  }
  return {
    topLeft: { x: x, y: y },
    topRight: { x: x + rect.width, y: y },
    bottomRight: { x: x + rect.width, y: y + rect.height },
    bottomLeft: { x: x, y: y + rect.height },
    width: rect.width,
    height: rect.height,
  };
}

export function elementIsVisibleAtCoords(el: HTMLElement, coords: Coords): boolean {
  const highest = document.elementFromPoint(coords.x, coords.y);
  if (highest?.contains(el)) {
    return true;
  }
  if (el.contains(highest)) {
    return true;
  }
  return false;
}

export function elementIsVisible(el: HTMLElement): boolean {
  const boxCoords = getCoordinatesOfElement(el);
  // If any of the box corners are visible, return true
  const coordsList = [boxCoords.topLeft, boxCoords.topRight, boxCoords.bottomRight, boxCoords.bottomLeft];

  const midpoint: Coords = {
    x: (boxCoords.bottomRight.x + boxCoords.topLeft.x) / 2,
    y: (boxCoords.bottomRight.y + boxCoords.topLeft.y) / 2
  }
  coordsList.push(midpoint)

  for (const coords of coordsList) {
    if (elementIsVisibleAtCoords(el, coords)) return true;
  }

  // Otherwise return false
  return false;
}
