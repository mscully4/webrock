export interface Tag {
  xpath: string;
  tagName: string;
  idNumber: number;
  innerText: string;
  ariaLabel?: string;
}

export interface DivTag extends Tag {
  role?: string;
  hasOnClickEvent?: boolean;
}

export interface AnchorTag extends Tag {
  role?: string;
}

export interface InputTag extends Tag {
  type?: string;
  value?: string;
  placeholder?: string;
}
