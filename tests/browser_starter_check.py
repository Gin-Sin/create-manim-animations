"""Check the served starter with Playwright and Pillow.

Usage: python tests/browser_starter_check.py http://localhost:8000
Requires playwright, pillow, and a Playwright Chromium installation.
CHROMIUM_PATH can select an existing full Chromium executable.
"""
import base64
import io
import os
import sys

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright, expect

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"


def pixels(data):
    return Image.open(io.BytesIO(base64.b64decode(data.split(",", 1)[1]))).convert("RGB")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH"))
    page = browser.new_page(viewport={"width": 1000, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.goto(url, wait_until="networkidle")
    expect(page.locator("#scene")).to_have_attribute("data-state", "ready")
    expect(page.locator("canvas")).to_have_count(1)
    frames = page.evaluate("""async () => {
      const canvas = document.querySelector('canvas');
      const slider = document.querySelector('#position');
      slider.value = '4';
      slider.dispatchEvent(new Event('input'));
      document.querySelector('#controls').requestSubmit();
      const first = await new Promise(resolve => requestAnimationFrame(() => resolve(canvas.toDataURL())));
      const locked = document.querySelector('#actions').disabled;
      await new Promise(resolve => setTimeout(resolve, 220));
      const middle = await new Promise(resolve => requestAnimationFrame(() => resolve(canvas.toDataURL())));
      return { first, middle, locked };
    }""")
    assert frames["locked"], "Controls were not locked during animation"
    assert ImageChops.difference(pixels(frames["first"]), pixels(frames["middle"])).getbbox(), "No animated canvas change"
    expect(page.locator("#scene")).to_have_attribute("data-state", "ready")
    expect(page.locator("#status")).to_have_text("Current position: 4.")
    expect(page.locator("#actions")).to_be_enabled()
    page.emulate_media(reduced_motion="reduce")
    page.get_by_role("button", name="Reset", exact=True).click()
    expect(page.locator("#status")).to_have_text("Current position: 0.")
    page.locator("#position").focus()
    page.keyboard.press("ArrowRight")
    expect(page.locator("#target")).to_have_text("1")
    page.get_by_role("button", name="Move point", exact=True).click()
    expect(page.locator("#status")).to_have_text("Current position: 1.")
    for width in (360, 768, 1000):
        page.set_viewport_size({"width": width, "height": 900})
        page.wait_for_timeout(100)
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Overflow at {width}px"
    assert not errors, errors
    fallback = browser.new_page()
    fallback.add_init_script("""const original = HTMLCanvasElement.prototype.getContext;
      HTMLCanvasElement.prototype.getContext = function(kind, ...args) {
        return String(kind).includes('webgl') ? null : original.call(this, kind, ...args);
      };""")
    fallback.goto(url, wait_until="networkidle")
    expect(fallback.locator("#status")).to_contain_text("Text view is active")
    fallback.locator("#position").focus()
    fallback.keyboard.press("ArrowRight")
    fallback.get_by_role("button", name="Move point", exact=True).click()
    expect(fallback.locator("#status")).to_contain_text("Current position: 1.")
    browser.close()
print("PASS: live Manim canvas motion, input locking, reset, reduced motion, keyboard controls, resizing, and graphics fallback.")
