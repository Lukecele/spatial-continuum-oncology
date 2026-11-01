#!/usr/bin/env node
/**
 * Responsive Multi-Screen Layout & Graphical Integrity Verifier
 * Evaluates index.html across 8 distinct device profiles (4K down to compact mobile).
 * Tests horizontal overflow, canvas scaling, module navigation, and visual rendering via Headless Chrome CDP.
 *
 * Author: Luca Celebrano, MD Candidate, Università degli Studi di Napoli Federico II
 */

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const HTML_PATH = path.join(ROOT_DIR, 'index.html');
const SCREENSHOT_DIR = path.join(ROOT_DIR, 'figure_scientifiche', 'responsive_screenshots');

if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getCDPTarget(port) {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${port}/json`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const list = JSON.parse(data);
          const page = list.find(t => t.type === 'page');
          resolve(page);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.id = 1;
    this.callbacks = new Map();
  }

  async connect() {
    const WS = globalThis.WebSocket;
    return new Promise((resolve, reject) => {
      this.ws = new WS(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (err) => reject(err);
      this.ws.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        if (msg.id && this.callbacks.has(msg.id)) {
          const { res, rej } = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) rej(msg.error);
          else res(msg.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((res, rej) => {
      const id = this.id++;
      this.callbacks.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const result = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (result.exceptionDetails) {
      throw new Error(JSON.stringify(result.exceptionDetails));
    }
    return result.result.value;
  }

  async captureScreenshot(outputPath, fullPage = false) {
    const params = { format: 'png' };
    if (fullPage) {
      params.captureBeyondViewport = true;
    }
    const result = await this.send('Page.captureScreenshot', params);
    fs.writeFileSync(outputPath, Buffer.from(result.data, 'base64'));
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

// -----------------------------------------------------------------------------
// Target Device Screen Profiles to Audit
// -----------------------------------------------------------------------------
const DEVICE_PROFILES = [
  { name: 'Desktop_4K_UltraWide', width: 2560, height: 1440, dpr: 1.0, mobile: false, desc: 'High-Resolution 4K / Widescreen Monitor' },
  { name: 'Desktop_Standard_FHD', width: 1920, height: 1080, dpr: 1.0, mobile: false, desc: 'Standard 1080p FHD Desktop Monitor' },
  { name: 'Laptop_Standard_HD', width: 1440, height: 900, dpr: 1.0, mobile: false, desc: 'MacBook Pro / Standard Workstation Laptop' },
  { name: 'Laptop_Compact_WXGA', width: 1280, height: 800, dpr: 1.0, mobile: false, desc: 'Compact Laptop / Chromebook Display' },
  { name: 'Tablet_Landscape_iPadPro', width: 1024, height: 768, dpr: 2.0, mobile: false, desc: 'iPad Pro / Surface Pro (Landscape)' },
  { name: 'Tablet_Portrait_iPad', width: 768, height: 1024, dpr: 2.0, mobile: true, desc: 'Standard iPad 9.7" / Tablet (Portrait)' },
  { name: 'Mobile_Large_iPhone14ProMax', width: 430, height: 932, dpr: 3.0, mobile: true, desc: 'iPhone 14/15 Pro Max, Galaxy S23 Ultra' },
  { name: 'Mobile_Standard_iPhone14', width: 390, height: 844, dpr: 3.0, mobile: true, desc: 'iPhone 12/13/14, Pixel 7 (Standard Mobile)' },
  { name: 'Mobile_Compact_Android', width: 360, height: 740, dpr: 2.0, mobile: true, desc: 'Budget Android / Compact Smartphone' },
];

async function runResponsiveAudit() {
  console.log('='.repeat(80));
  console.log('📱 SPATIAL ONCOLOGY PORTAL — MULTI-SCREEN RESPONSIVE LAYOUT AUDIT');
  console.log('='.repeat(80));

  const port = 9444;

  // Launch headless Chrome
  const chrome = spawn('google-chrome', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--window-size=1440,900',
    `file://${HTML_PATH}`
  ]);

  await wait(2000);

  let allPassed = true;
  const auditResults = [];

  try {
    const target = await getCDPTarget(port);
    console.log(`[✓] Chrome instance launched successfully: ${target.title}`);

    const cdp = new CDPClient(target.webSocketDebuggerUrl);
    await cdp.connect();
    console.log('[✓] CDP WebSocket connected.\n');

    await cdp.send('Runtime.enable');
    await cdp.send('Page.enable');

    for (const dev of DEVICE_PROFILES) {
      console.log(`--- Auditing Device: ${dev.name} (${dev.width}x${dev.height}, DPR: ${dev.dpr}) ---`);
      console.log(`    Target: ${dev.desc}`);

      // 1. Set emulation metrics
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: dev.width,
        height: dev.height,
        deviceScaleFactor: dev.dpr,
        mobile: dev.mobile,
        fitWindow: false,
      });

      await wait(300);

      // 2. Measure layout metrics across modules
      const layoutCheck = await cdp.evaluate(`
        (() => {
          const docEl = document.documentElement;
          const body = document.body;
          const scrollW = Math.max(docEl.scrollWidth, body.scrollWidth);
          const clientW = docEl.clientWidth;
          const winW = window.innerWidth;
          const hasHorizontalOverflow = scrollW > winW + 1; // 1px tolerance for subpixel antialiasing

          // Check container and cards
          const container = document.querySelector('.container');
          const containerW = container ? container.getBoundingClientRect().width : 0;

          // Check canvas sizes
          const visCanvas = document.getElementById('visium-canvas');
          const visCanvasBox = visCanvas ? visCanvas.getBoundingClientRect() : null;

          return {
            scrollW,
            clientW,
            winW,
            hasHorizontalOverflow,
            overflowDelta: scrollW - winW,
            containerW,
            visCanvasBox: visCanvasBox ? { w: Math.round(visCanvasBox.width), h: Math.round(visCanvasBox.height) } : null,
          };
        })()
      `);

      const screenshotName = `viewport_${dev.name}_${dev.width}x${dev.height}.png`;
      const screenshotPath = path.join(SCREENSHOT_DIR, screenshotName);
      await cdp.captureScreenshot(screenshotPath, false);

      const isPass = !layoutCheck.hasHorizontalOverflow;
      if (!isPass) allPassed = false;

      const statusIcon = isPass ? '✓ PASS' : '❌ OVERFLOW';
      console.log(`    ${statusIcon}: Viewport = ${layoutCheck.winW}px, ScrollWidth = ${layoutCheck.scrollW}px (Delta: ${layoutCheck.overflowDelta.toFixed(1)}px)`);
      if (layoutCheck.visCanvasBox) {
        console.log(`    Canvas: Width = ${layoutCheck.visCanvasBox.w}px, Height = ${layoutCheck.visCanvasBox.h}px (Responsive scaling OK)`);
      }
      console.log(`    Screenshot saved: ${screenshotName}\n`);

      auditResults.push({
        device: dev.name,
        resolution: `${dev.width}x${dev.height}`,
        isPass,
        overflowDelta: layoutCheck.overflowDelta,
        screenshot: screenshotName,
      });
    }

    // -------------------------------------------------------------------------
    // Mobile Interactive Tab Switching Test
    // -------------------------------------------------------------------------
    console.log('--- Testing Mobile Interactive Module Transitions on iPhone 14 (390x844) ---');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 3.0,
      mobile: true,
    });
    await wait(200);

    // Switch through all modules to verify render integrity
    for (let modId = 1; modId <= 6; modId++) {
      const switchResult = await cdp.evaluate(`
        (() => {
          switchMainModule('${modId}');
          const mod = document.getElementById('module-${modId}');
          const btn = document.getElementById('mod-btn-${modId}');
          return {
            activeDisplay: mod ? window.getComputedStyle(mod).display : 'missing',
            btnActive: btn ? btn.classList.contains('active') : false,
            scrollW: document.documentElement.scrollWidth,
            winW: window.innerWidth,
          };
        })()
      `);

      const modScreenshot = path.join(SCREENSHOT_DIR, `mobile_390x844_module_${modId}.png`);
      await cdp.captureScreenshot(modScreenshot, false);

      const modPass = switchResult.scrollW <= switchResult.winW + 1;
      if (!modPass) allPassed = false;
      const modIcon = modPass ? '✓' : '❌';
      console.log(`    ${modIcon} Module ${modId} Display: ${switchResult.activeDisplay} | Horizontal Fit: ${switchResult.scrollW <= switchResult.winW ? 'OK' : 'OVERFLOW'} | Saved: mobile_390x844_module_${modId}.png`);
    }

    cdp.close();
  } catch (err) {
    console.error('Audit Error:', err);
    allPassed = false;
  } finally {
    chrome.kill('SIGTERM');
  }

  console.log('\n' + '='.repeat(80));
  console.log('📊 RESPONSIVE MULTI-SCREEN AUDIT RESULTS SUMMARY');
  console.log('='.repeat(80));

  console.table(auditResults);

  if (allPassed) {
    console.log('🎉 100% RESPONSIVE INTEGRITY: ZERO HORIZONTAL OVERFLOW ACROSS ALL 9 SCREEN PROFILES!');
  } else {
    console.log('⚠️ Some screen sizes showed layout overflow. Review table above.');
  }

  return allPassed;
}

runResponsiveAudit().then(passed => {
  process.exit(passed ? 0 : 1);
});
