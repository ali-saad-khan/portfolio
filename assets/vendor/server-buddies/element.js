import { createBuddy } from "./core.js";

const OBSERVED = [
  "character", "hang", "position", "accessory", "color", "size", "length", "actions", "mood", "mount",
  "watch-input", "look-at", "hide-below", "offset-x", "offset-y"
];

function optionsFromAttributes(el) {
  const get = (name) => (el.hasAttribute(name) ? el.getAttribute(name) : undefined);
  const num = (v) => (v === undefined || v === "" ? undefined : Number(v));
  const actions = get("actions");
  const ox = num(get("offset-x"));
  const oy = num(get("offset-y"));
  return {
    character: get("character"),
    hang: get("hang"),
    position: get("position"),
    accessory: get("accessory"),
    color: get("color"),
    size: num(get("size")),
    length: num(get("length")),
    mood: get("mood"),
    mount: get("mount"),
    watchInput: get("watch-input"),
    lookAt: get("look-at"),
    hideBelow: num(get("hide-below")),
    offset: ox !== undefined || oy !== undefined ? { ...(ox !== undefined && { x: ox }), ...(oy !== undefined && { y: oy }) } : undefined,
    actions: actions === undefined ? undefined : actions.split(",").map((s) => s.trim()).filter(Boolean)
  };
}

const clean = (o) => Object.fromEntries(Object.entries(o).filter(([, v]) => v !== undefined));

/**
 * Registers `<server-buddy>`. Attributes mirror the options (kebab-case):
 * `<server-buddy character="robot" hang="chain" actions="eyes,swing,boop"></server-buddy>`
 */
export function defineServerBuddyElement(tag = "server-buddy") {
  if (typeof window === "undefined" || typeof customElements === "undefined" || customElements.get(tag)) return;
  customElements.define(
    tag,
    class extends HTMLElement {
      static get observedAttributes() {
        return OBSERVED;
      }
      connectedCallback() {
        this.style.display = "none";
        this.buddy = createBuddy(clean(optionsFromAttributes(this)));
      }
      disconnectedCallback() {
        this.buddy && this.buddy.destroy();
        this.buddy = null;
      }
      attributeChangedCallback() {
        if (this.buddy) this.buddy.update(clean(optionsFromAttributes(this)));
      }
    }
  );
}
