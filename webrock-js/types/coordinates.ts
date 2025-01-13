/**
 * Represents a point on the screen in pixels
 */
export interface Coords {
  x: number;
  y: number;
}

/**
 * Represents the coordinates that map up a box
 */
export interface BoxCoords {
  topLeft: Coords;
  topRight: Coords;
  bottomRight: Coords;
  bottomLeft: Coords;
  width: number;
  height: number;
}
