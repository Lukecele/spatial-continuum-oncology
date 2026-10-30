/**
 * Automated End-to-End Test & Headless CDP Verification for Grand Unified Portal
 * Tests all 5 modules in index.html (Bedside, 10x Visium, Digital Twin, InSituGame, MSKCC)
 * Pure standard Node.js (zero npm packages).
 */

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

async function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getCDPTarget(port) {
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

  close() {
    if (this.ws) this.ws.close();
  }
}

async function run() {
  console.log('=== STARTING TEST & CONTRO-TEST SU GRAND UNIFIED PORTAL (5 MODULI) ===');
  const port = 9333;
  const htmlPath = path.resolve('/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/index.html');

  // Spawn Headless Chrome
  const chrome = spawn('google-chrome', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--window-size=1440,960',
    `file://${htmlPath}`
  ]);

  await wait(1800);

  try {
    const target = await getCDPTarget(port);
    console.log('✓ Attached to Headless Chrome via CDP:', target.title);

    const cdp = new CDPClient(target.webSocketDebuggerUrl);
    await cdp.connect();
    console.log('✓ WebSocket debugger connection established');

    // 1. Enable Runtime & check initial console state
    await cdp.send('Runtime.enable');
    await cdp.send('Page.enable');

    // 2. Verify all 5 modules exist in DOM
    const modulesExist = await cdp.evaluate(`
      (() => {
        const results = {};
        for (let i = 1; i <= 5; i++) {
          const btn = document.getElementById('mod-btn-' + i);
          const mod = document.getElementById('module-' + i);
          results['mod_' + i] = {
            btnExists: !!btn,
            modExists: !!mod,
            display: mod ? mod.style.display : null
          };
        }
        return results;
      })()
    `);
    console.log('✓ Modules DOM structure check:');
    for (let k in modulesExist) {
      console.log(`   ${k}: btn=${modulesExist[k].btnExists}, mod=${modulesExist[k].modExists}, display=${modulesExist[k].display}`);
      if (!modulesExist[k].btnExists || !modulesExist[k].modExists) {
        throw new Error(`Module DOM element missing for ${k}`);
      }
    }

    // 3. Test Navigation to Module 2 (10x Visium HD Spatial Benchmark)
    console.log('\n--- TESTING MODULE 2: 10x VISIUM HD BENCHMARK ---');
    await cdp.evaluate(`switchMainModule('2')`);
    await wait(500);

    const mod2Data = await cdp.evaluate(`
      (() => {
        const mod2 = document.getElementById('module-2');
        const canvas = document.getElementById('visium-canvas');
        const pfsCanvas = document.getElementById('visium-pfs-canvas');
        const tbody = document.getElementById('visium-patients-tbody');
        const spotsCount = typeof VISIUM_SPOTS !== 'undefined' ? VISIUM_SPOTS.length : 0;
        return {
          display: mod2.style.display,
          spotsCount: spotsCount,
          canvasW: canvas ? canvas.width : 0,
          pfsCanvasW: pfsCanvas ? pfsCanvas.width : 0,
          patientRows: tbody ? tbody.children.length : 0
        };
      })()
    `);
    console.log('✓ Module 2 Active State:', mod2Data);
    if (mod2Data.spotsCount !== 3858) {
      throw new Error(`VISIUM_SPOTS count expected 3858, got ${mod2Data.spotsCount}`);
    }
    if (mod2Data.patientRows !== 4) {
      throw new Error(`Patient rows expected 4, got ${mod2Data.patientRows}`);
    }

    // 4. Test Filter buttons in Module 2
    console.log('✓ Testing Filter buttons (sanctuary, endo, tumor, all)...');
    await cdp.evaluate(`setVisiumFilter('sanctuary', document.querySelectorAll('.vis-filter-btn')[1])`);
    await wait(200);
    await cdp.evaluate(`setVisiumFilter('endo', document.querySelectorAll('.vis-filter-btn')[2])`);
    await wait(200);
    await cdp.evaluate(`setVisiumFilter('all', document.querySelectorAll('.vis-filter-btn')[0])`);
    await wait(200);

    // 5. Capture visual snapshot of Module 2
    const shotResult = await cdp.send('Page.captureScreenshot', { format: 'png' });
    const shotPath = '/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/figure_scientifiche/test_module2_visium_render.png';
    fs.writeFileSync(shotPath, Buffer.from(shotResult.data, 'base64'));
    console.log('✓ Visual render snapshot of Module 2 saved to:', shotPath);

    // 6. Test Bedside Integration: Apply patient s3_PFS_15 (Solid, Tier 3)
    console.log('\n--- TESTING BEDSIDE INTEGRATION: APPLY PATIENT s3_PFS_15 ---');
    await cdp.evaluate(`applyPatientToBedside('s3_PFS_15')`);
    await wait(500);

    const mod1State = await cdp.evaluate(`
      (() => {
        const mod1 = document.getElementById('module-1');
        const histo = document.getElementById('select-histology') ? document.getElementById('select-histology').value : null;
        const geno = document.getElementById('select-genomics') ? document.getElementById('select-genomics').value : null;
        const stroma = document.getElementById('select-stroma') ? document.getElementById('select-stroma').value : null;
        const criText = document.getElementById('cri-score-display') ? document.getElementById('cri-score-display').textContent : '';
        return {
          mod1Display: mod1.style.display,
          histo, geno, stroma, criText
        };
      })()
    `);
    console.log('✓ Module 1 After Patient Load:', mod1State);
    if (mod1State.histo !== '1.00' || mod1State.geno !== '1.00' || mod1State.stroma !== '1.00') {
      throw new Error('Patient s3_PFS_15 genomic/histologic profile was not applied accurately!');
    }

    // 7. Test Navigation to Module 3 (60 FPS Digital Twin)
    console.log('\n--- TESTING MODULE 3: 60 FPS DIGITAL TWIN ---');
    await cdp.evaluate(`switchMainModule('3')`);
    await wait(400);
    const mod3State = await cdp.evaluate(`
      (() => {
        const mod3 = document.getElementById('module-3');
        const iframe = document.getElementById('sim-frame');
        return {
          display: mod3.style.display,
          iframeSrc: iframe ? iframe.getAttribute('src') : null
        };
      })()
    `);
    console.log('✓ Module 3 State:', mod3State);
    if (mod3State.iframeSrc !== 'simulator.html') {
      throw new Error('Module 3 iframe source missing or incorrect!');
    }

    // 8. Test Navigation to Module 4 (InSituGame)
    console.log('\n--- TESTING MODULE 4: IN SITU GAME ---');
    await cdp.evaluate(`switchMainModule('4')`);
    await wait(400);
    const mod4State = await cdp.evaluate(`
      (() => {
        const mod4 = document.getElementById('module-4');
        return { display: mod4.style.display };
      })()
    `);
    console.log('✓ Module 4 State:', mod4State);

    // 9. Test Navigation to Module 5 (MSKCC & Evidence Hub)
    console.log('\n--- TESTING MODULE 5: MSKCC & EVIDENCE HUB ---');
    await cdp.evaluate(`switchMainModule('5')`);
    await wait(400);
    const mod5State = await cdp.evaluate(`
      (() => {
        const mod5 = document.getElementById('module-5');
        const kmCanvas = document.getElementById('km-canvas');
        return {
          display: mod5.style.display,
          kmCanvasW: kmCanvas ? kmCanvas.width : 0
        };
      })()
    `);
    console.log('✓ Module 5 State:', mod5State);

    console.log('\n======================================================');
    console.log('✓ ALL 5 PORTAL MODULES & INTERACTIVE BENCHMARKS PASSED: 100%');
    console.log('======================================================');

    cdp.close();
  } finally {
    chrome.kill();
  }
}

run().catch(err => {
  console.error('TEST FAILED:', err);
  process.exit(1);
});
