export const WEBROCK_ID = '__webrock__';
export const WEBROCK_SELECTOR = `#${WEBROCK_ID}`;

export enum TagNames {
  INPUT = 'INPUT',
  A = 'A',
  DIV = 'DIV',
  BUTTON = 'BUTTON'
}

export const tagAnnotationColors: Partial<Record<TagNames, string>> = {
  INPUT: '#00FF00',
  A: '#FF69B4',
  DIV: '#00FFFF'
};

export const everythingElseColor = '#FF0000';
