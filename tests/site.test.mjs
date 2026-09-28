import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(resolve(root, 'index.html'), 'utf8');
const css = readFileSync(resolve(root, 'styles.css'), 'utf8');

test('storefront has Spanish metadata and a clear demo label', () => {
  assert.match(html, /<html lang="es">/);
  assert.match(html, /<title>Lúmina Plata/);
  assert.match(html, /TIENDA DE DEMOSTRACIÓN/);
  assert.match(html, /no hay compras ni procesamiento de pagos/i);
});

test('storefront includes the collection, story, and contact sections', () => {
  for (const id of ['inicio', 'coleccion', 'nosotros', 'contacto']) {
    assert.match(html, new RegExp(`id="${id}"`), `missing #${id} section`);
  }
  for (const product of ['Aros Órbita', 'Anillo Alba', 'Collar Gota', 'Pulsera Trama']) {
    assert.ok(html.includes(product), `missing product: ${product}`);
  }
});

test('all in-page links and local resources resolve', () => {
  const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]));
  for (const [, href] of html.matchAll(/\bhref="#([^"]+)"/g)) {
    assert.ok(ids.has(href), `broken in-page link: #${href}`);
  }
  for (const [, path] of html.matchAll(/\b(?:href|src)="(assets\/[^"#?]+|styles\.css)"/g)) {
    assert.ok(existsSync(resolve(root, path)), `missing local resource: ${path}`);
  }
});

test('styles provide responsive layouts, keyboard focus, and reduced-motion support', () => {
  assert.match(css, /@media\s*\(max-width:\s*850px\)/);
  assert.match(css, /@media\s*\(max-width:\s*600px\)/);
  assert.match(css, /:focus-visible/);
  assert.match(css, /prefers-reduced-motion/);
});
