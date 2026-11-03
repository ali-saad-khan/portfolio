import { createBuddy, renderPreview, ensureStyles, ACTIONS, HANG_STYLES, POSITIONS, MOODS } from "./core.js";
import { CHARACTERS, CHARACTER_IDS, ACCESSORIES } from "./characters.js";
import { defineServerBuddyElement } from "./element.js";

export { createBuddy, renderPreview, ensureStyles, defineServerBuddyElement, ACTIONS, HANG_STYLES, POSITIONS, MOODS, ACCESSORIES };

/** Metadata for building pickers: `[{ id, name, blurb }]`. */
export const characters = CHARACTER_IDS.map((id) => ({ id, name: CHARACTERS[id].name, blurb: CHARACTERS[id].blurb }));
