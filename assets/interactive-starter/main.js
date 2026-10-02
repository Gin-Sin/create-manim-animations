const container = document.querySelector("#scene");
const controls = document.querySelector("#controls");
const actions = document.querySelector("#actions");
const slider = document.querySelector("#position");
const target = document.querySelector("#target");
const status = document.querySelector("#status");
const reduced = matchMedia("(prefers-reduced-motion: reduce)");
let scene, dot, Shift, position = 0, busy = false, disposed = false, resizePending = false;
const location = value => [-4 + 2 * value, 0, 0];

function describe() {
  status.textContent = `Current position: ${position}.` + (scene ? "" : " Text view is active; the animation is unavailable.");
  container.dataset.position = String(position);
}

function resize() {
  if (!scene || disposed) return;
  if (busy) { resizePending = true; return; }
  const width = Math.max(1, container.clientWidth);
  scene.resize(width, Math.max(220, Math.round(width * 0.5)));
  scene.render();
  resizePending = false;
}

async function move(next) {
  if (busy || disposed || !Number.isInteger(next) || next < 0 || next > 4) return;
  const before = position;
  position = next; // Commit one valid model update; rendering cannot corrupt it.
  slider.value = String(next);
  target.value = String(next);
  busy = true;
  actions.disabled = true;
  container.dataset.state = "animating";
  status.textContent = `Moving from ${before} to ${next}.`;
  try {
    if (scene) {
      if (reduced.matches || before === next) dot.moveTo(location(next));
      else await scene.play(new Shift(dot, { direction: [2 * (next - before), 0, 0], duration: 0.8 }));
      if (disposed) return;
      dot.moveTo(location(next));
      scene.render();
    }
  } catch (error) {
    console.warn("Animation unavailable; preserving the textual model.", error);
    try { scene?.dispose(); } catch { /* The graphics context may already be lost. */ }
    scene = null;
    container.replaceChildren();
  } finally {
    busy = false;
    actions.disabled = false;
    container.dataset.state = "ready";
    if (!disposed) {
      if (resizePending) resize();
      describe();
    }
  }
}

slider.addEventListener("input", () => { target.value = slider.value; });
controls.addEventListener("submit", event => { event.preventDefault(); void move(Number(slider.value)); });
document.querySelector("#reset").addEventListener("click", () => { void move(0); });
actions.disabled = true;
try {
  await document.fonts.ready;
  const api = await import("manim-web");
  if (!disposed) {
    Shift = api.Shift;
    scene = new api.Scene(container, {
      width: Math.max(1, container.clientWidth), height: 400,
      frameWidth: 10, frameHeight: 5, backgroundColor: "#000000",
      autoRender: false, autoResize: false,
    });
    scene.add(new api.Line({ start: [-4.3, 0, 0], end: [4.3, 0, 0], color: "#aaa7a0", strokeWidth: 2 }));
    for (let value = 0; value <= 4; value++) {
      const [x] = location(value);
      scene.add(new api.Line({ start: [x, -0.12, 0], end: [x, 0.12, 0], color: "#aaa7a0" }));
      scene.add(new api.Text({ text: String(value), fontFamily: "monospace", fontSize: 25, color: "#f5f3ef" }).moveTo([x, -0.55, 0]));
    }
    scene.add(new api.Text({ text: "A position on the line", fontFamily: "serif", fontSize: 30, color: "#f5f3ef" }).moveTo([0, 1.5, 0]));
    dot = new api.Dot({ radius: 0.15, color: "#58c4dd" }).moveTo(location(position));
    scene.add(dot);
    resize();
  }
} catch (error) {
  console.warn("Graphics initialization failed; controls remain available.", error);
  try { scene?.dispose(); } catch { /* Preserve the fallback even on failed cleanup. */ }
  scene = null;
  container.replaceChildren();
} finally {
  actions.disabled = false;
  container.dataset.state = "ready";
  describe();
}
const observer = new ResizeObserver(resize);
observer.observe(container);
addEventListener("pagehide", event => {
  if (event.persisted) return; // Preserve a page retained in the browser's back/forward cache.
  disposed = true;
  observer.disconnect();
  scene?.dispose();
}, { once: true });
