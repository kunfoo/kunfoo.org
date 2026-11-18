/* Colour scheme override.
 *
 * The <meta name="color-scheme"> element in the document head is the source of
 * truth: "light dark" means follow the system preference, "light" or "dark" pin
 * a scheme. main.css maps that content back onto the color-scheme property, so
 * this file only has to keep the meta and localStorage in sync.
 *
 * Without this file the page still works: the meta stays "light dark", the page
 * follows the system preference, and the button stays hidden.
 */
(function () {
  var KEY = "color-scheme";
  var meta = document.querySelector('meta[name="color-scheme"]');
  var button = document.getElementById("scheme-toggle");
  if (!meta || !button) return;

  var systemScheme = function () {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  };

  var storedScheme = function () {
    try {
      var value = localStorage.getItem(KEY);
      return value === "light" || value === "dark" ? value : null;
    } catch (error) {
      return null;
    }
  };

  /* Read the meta rather than localStorage: the meta is what CSS keys off, so
     it stays correct even when storage is unavailable and the override could
     not be persisted. */
  var renderedScheme = function () {
    var content = meta.content.trim();
    return content === "light" || content === "dark" ? content : systemScheme();
  };

  /* The button names the action it performs, not the state it is in. */
  var relabel = function () {
    button.textContent = renderedScheme() === "dark" ? "light theme" : "dark theme";
  };

  var apply = function () {
    meta.content = storedScheme() || "light dark";
    relabel();
  };

  button.addEventListener("click", function () {
    /* Intent is "give me the opposite of what I see", so the target is the
     * inverse of the rendered scheme rather than of the system preference. */
    var target = renderedScheme() === "dark" ? "light" : "dark";
    try {
      if (target === systemScheme()) {
        /* Toggling back to the system preference is the user undoing their
         * override, so drop the stored value instead of pinning it. */
        localStorage.removeItem(KEY);
      } else {
        localStorage.setItem(KEY, target);
      }
    } catch (error) {
      /* Site data may be blocked. Apply the scheme anyway, just without
       * persisting it across page loads. */
      meta.content = target;
      relabel();
      return;
    }
    apply();

  });

  /* The override may have been changed in another tab. */
  window.addEventListener("storage", function (event) {
    if (event.key === KEY) apply();
  });

  /* When no override is stored the scheme follows the system preference through
   * CSS, so a system change only needs the label corrected. A stored value is
   * deliberately kept even once the system comes to match it, otherwise an OS
   * that switches on a schedule would make pinning a scheme impossible. */
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", relabel);

  relabel();
  button.hidden = false;
})();
