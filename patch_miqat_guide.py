import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS for Miqat Fiqh Guide modal and HUD widget
miqat_css = '''
    /* ===== MIQAT FIQH GUIDE & CHECKLIST STYLES ===== */
    .miqat-modal-card {
      background: var(--color-obsidian);
      border: 1.5px solid var(--color-gold);
      border-radius: var(--radius-card);
      padding: 24px 22px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75), 0 0 40px rgba(245, 197, 66, 0.28);
      width: 100%;
      max-width: 620px;
      max-height: 90vh;
      overflow-y: auto;
      animation: popModal 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .miqat-progress-box {
      background: rgba(30, 41, 59, 0.75);
      border: 1px solid rgba(245, 197, 66, 0.35);
      border-radius: 14px;
      padding: 12px 16px;
      margin-bottom: 16px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    .miqat-progress-track {
      width: 100%;
      height: 10px;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 999px;
      margin: 8px 0 10px 0;
      overflow: hidden;
      border: 1px solid rgba(245, 197, 66, 0.25);
    }
    .miqat-progress-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #f5c542, #10b981);
      transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 0 12px #10b981;
    }
    .miqat-step-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      justify-content: center;
    }
    .miqat-chip {
      font-size: 0.68rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      color: #94a3b8;
      border: 1px solid rgba(255, 255, 255, 0.15);
      transition: all 0.2s ease;
    }
    .miqat-chip.done {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border-color: #10b981;
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
    }
    .miqat-step-card {
      background: rgba(30, 41, 59, 0.65);
      border: 1.5px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 12px;
      transition: all 0.25s ease;
      text-align: left;
    }
    .miqat-step-card:hover {
      background: rgba(30, 41, 59, 0.85);
      border-color: var(--color-gold);
    }
    .miqat-step-card.step-completed {
      border-color: #10b981;
      background: linear-gradient(135deg, rgba(6, 78, 59, 0.35) 0%, rgba(30, 41, 59, 0.75) 100%);
      box-shadow: 0 0 16px rgba(16, 185, 129, 0.2);
    }
    .step-badge-status {
      font-size: 0.72rem;
      font-weight: 800;
      padding: 2px 10px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .status-pending {
      background: rgba(245, 197, 66, 0.15);
      color: var(--color-gold);
      border: 1px solid rgba(245, 197, 66, 0.4);
    }
    .status-done {
      background: rgba(16, 185, 129, 0.25);
      color: #34d399;
      border: 1px solid #10b981;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
    }
    .btn-step-action {
      background: linear-gradient(135deg, #f5c542 0%, #d97706 100%);
      color: #0f172a;
      font-weight: 800;
      font-size: 0.86rem;
      border: none;
      border-radius: 8px;
      padding: 9px 16px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      margin-top: 8px;
      transition: all 0.15s ease;
      box-shadow: 0 2px 10px rgba(245, 197, 66, 0.3);
    }
    .btn-step-action:hover {
      box-shadow: 0 0 18px rgba(245, 197, 66, 0.6);
      transform: translateY(-1px);
    }
    .btn-step-action.done-btn {
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid #10b981;
      color: #6ee7b7;
      cursor: default;
      box-shadow: none;
      transform: none;
    }
    /* Floating HUD Miqat Checklist Pill */
    .hud-miqat-pill {
      background: rgba(15, 23, 42, 0.88);
      border: 1.5px solid var(--color-gold);
      border-radius: var(--radius-chip);
      padding: 4px 12px;
      display: none;
      align-items: center;
      gap: 8px;
      font-size: 0.74rem;
      font-weight: 700;
      color: #fff;
      backdrop-filter: blur(8px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.4), 0 0 12px rgba(245,197,66,0.25);
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .hud-miqat-pill:hover {
      transform: translateY(-1px);
      border-color: #fff;
      box-shadow: 0 0 18px rgba(245,197,66,0.5);
    }
    .hud-miqat-pill.visible {
      display: inline-flex;
    }
    /* Easy Assist Controls for Live Activities */
    .easy-assist-row {
      display: flex;
      gap: 6px;
      margin-top: 6px;
      justify-content: center;
      flex-wrap: wrap;
    }
    .btn-easy-assist {
      background: rgba(245, 197, 66, 0.18);
      border: 1px solid var(--color-gold);
      color: #fef08a;
      font-size: 0.68rem;
      font-weight: 700;
      border-radius: 6px;
      padding: 3px 8px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-easy-assist:hover {
      background: rgba(245, 197, 66, 0.35);
      color: #fff;
      transform: scale(1.04);
    }
'''

# Insert CSS before </style>
html = html.replace('</style>', miqat_css + '\n  </style>', 1)
print("Inserted Miqat CSS!")

# 2. Add HUD Miqat Checklist Pill next to Current Location banner
old_quest_banner = '''      <!-- Current Location & Quest Banner -->
      <div class="quest-location-banner clickable" onclick="openCurrentLocationActions()" title="Lihat Pilihan Amalan & Ibadah di Sini">
        <div class="quest-tag" id="banner-mode-txt">MISI AKTIF · UMRAH</div>
        <div class="quest-loc-title" id="banner-location-txt">📍 Stasiun Miqat (Dzulhulaifah)</div>
      </div>'''

new_quest_banner = '''      <!-- Current Location & Quest Banner -->
      <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
        <div class="quest-location-banner clickable" onclick="openCurrentLocationActions()" title="Lihat Pilihan Amalan & Ibadah di Sini">
          <div class="quest-tag" id="banner-mode-txt">MISI AKTIF · UMRAH</div>
          <div class="quest-loc-title" id="banner-location-txt">📍 Stasiun Miqat (Dzulhulaifah)</div>
        </div>
        <!-- Floating HUD Miqat Step-by-Step Checklist Widget -->
        <div class="hud-miqat-pill clickable" id="hud-miqat-pill" onclick="openMiqatGuideModal()" title="Buka Panduan & Checklist Rukun Miqat">
          <span style="color:var(--color-gold);">📋 Checklist Miqat:</span>
          <span id="hud-miqat-pill-txt" style="color:#10b981;">0/4 Selesai (0%)</span>
          <span style="font-size:0.65rem; background:rgba(245,197,66,0.2); padding:1px 6px; border-radius:4px; color:var(--color-gold);">Buka ➔</span>
        </div>
      </div>'''

if old_quest_banner in html:
    html = html.replace(old_quest_banner, new_quest_banner, 1)
    print("Added HUD Miqat Checklist widget!")

# 3. Add Easy-Assist buttons to Live Activity HUD (Tawaf, Sa'i, Wukuf, Jamarat)
old_live_activity_hud = '''      <div class="act-progress-track">
        <div class="act-progress-fill" id="live-act-progress"></div>
      </div>
    </div>'''

new_live_activity_hud = '''      <div class="act-progress-track">
        <div class="act-progress-fill" id="live-act-progress"></div>
      </div>
      <!-- Kemudahan Pengerjaan: Tombol Cepat / Bantu Hitung -->
      <div class="easy-assist-row clickable" id="live-act-assist-row">
        <button type="button" class="btn-easy-assist" id="btn-assist-step" onclick="assistAdvanceCurrentActivity()">
          ➕ Tambah 1 Hitungan
        </button>
        <button type="button" class="btn-easy-assist" style="border-color:#10b981; color:#a7f3d0; background:rgba(16,185,129,0.2);" onclick="instantCompleteCurrentActivity()">
          ⚡ Selesaikan Rukun Langsung
        </button>
      </div>
    </div>'''

if old_live_activity_hud in html:
    html = html.replace(old_live_activity_hud, new_live_activity_hud, 1)
    print("Added Easy-Assist buttons to Live Activity HUD!")

# 4. Insert dedicated #modal-miqat-guide HTML
modal_miqat_html = '''
  <!-- ======================================================= -->
  <!-- MODAL: PANDUAN FIQH & CHECKLIST AMALAN MIQAT (STEP-BY-STEP) -->
  <!-- ======================================================= -->
  <div class="modal-backdrop" id="modal-miqat-guide">
    <div class="miqat-modal-card">
      <div class="modal-header-row">
        <div class="modal-title-gold" style="font-size:1.35rem;">
          <span>📖</span> <span>Panduan Fiqh & Checklist Miqat</span>
        </div>
        <button class="btn-close-modal clickable" onclick="closeModal('modal-miqat-guide')">✕</button>
      </div>
      <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:12px; text-align:left;">
        Stasiun Miqat Dzulhulaifah (Bir Ali) — Selesaikan 4 urutan langkah fiqh resmi di bawah ini sebelum memasuki Tanah Suci Makkah:
      </p>

      <!-- Visual Checklist & Progress Bar Tracker -->
      <div class="miqat-progress-box">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem; font-weight:700;">
          <span style="color:var(--color-gold); display:flex; align-items:center; gap:6px;">
            <span>📋</span> <span>Progres Rukun Miqat:</span>
          </span>
          <span style="color:#34d399; font-size:0.9rem;" id="miqat-modal-stat-txt">0 / 4 Selesai (0%)</span>
        </div>
        <div class="miqat-progress-track">
          <div class="miqat-progress-fill" id="miqat-modal-bar" style="width:0%;"></div>
        </div>
        <div class="miqat-step-chips">
          <span class="miqat-chip" id="chip-step-bersuci">1. Bersuci</span>
          <span class="miqat-chip" id="chip-step-ihram">2. Busana Ihram</span>
          <span class="miqat-chip" id="chip-step-niat">3. Niat Ihram</span>
          <span class="miqat-chip" id="chip-step-talbiyah">4. Lantunan Talbiyah</span>
        </div>
      </div>

      <!-- Completion Announcement Banner (Hidden until 4/4 done) -->
      <div id="miqat-all-done-banner" style="display:none; background:linear-gradient(135deg, rgba(6,78,59,0.85), rgba(4,120,87,0.85)); border:1.5px solid #34d399; border-radius:14px; padding:16px; margin-bottom:16px; text-align:center; box-shadow:0 0 25px rgba(16,185,129,0.4);">
        <div style="font-size:2.2rem; margin-bottom:4px;">🎉</div>
        <h4 style="font-size:1.18rem; font-weight:800; color:#f0fdf4; margin-bottom:4px;">
          Alhamdulillah! Seluruh 4 Rukun Miqat Telah Tuntas Mabrur!
        </h4>
        <p style="font-size:0.82rem; color:#d1fae5; line-height:1.4; margin-bottom:12px;">
          Status Anda kini resmi Muhrim (berihram). Langkah berikutnya adalah menuju Baitullah Ka'bah untuk menunaikan Tawaf 7 Putaran.
        </p>
        <button type="button" class="btn-main btn-gold clickable" onclick="proceedFromMiqatToPos2()" style="font-size:1rem; padding:12px 20px;">
          <span>🚀 Lanjut ke POS 2 — Tawaf Ka'bah (Teleport Cepat) ➔</span>
        </button>
      </div>

      <!-- 4 Step-by-Step Procedure Cards -->
      <div id="miqat-steps-container">

        <!-- LANGKAH 1: BERSUCI (MANDI / WUDHU) -->
        <div class="miqat-step-card" id="card-step-bersuci">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.5rem;">💧</span>
              <div>
                <div style="font-weight:800; font-size:0.95rem; color:#ffffff;">
                  Langkah 1: Bersuci (Mandi Sunnah & Berwudhu)
                </div>
                <div style="font-size:0.7rem; color:var(--color-emerald); font-weight:700;">HUKUM: SUNNAH MU'AKKADAH</div>
              </div>
            </div>
            <span class="step-badge-status status-pending" id="badge-step-bersuci">⏳ Belum</span>
          </div>
          <p style="font-size:0.83rem; color:#cbd5e1; line-height:1.45; margin-top:8px;">
            Membersihkan badan secara menyeluruh sebelum ihram: memotong kuku, mencukur bulu ketiak/kemaluan, mandi sunnah ihram, dan mengambil wudhu suci dari hadas.
          </p>
          <div style="font-size:0.75rem; color:#94a3b8; font-style:italic; margin-top:4px;">
            "Rasulullah SAW mandi untuk memulai ihramnya." (HR. Tirmidzi)
          </div>
          <button type="button" class="btn-step-action clickable" id="btn-step-bersuci" onclick="executeMiqatStep('bersuci')">
            <span>💧 Laksanakan Bersuci & Mandi Ihram (+20 Pahala)</span>
          </button>
        </div>

        <!-- LANGKAH 2: MENGENAKAN PAKAIAN IHRAM -->
        <div class="miqat-step-card" id="card-step-ihram">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.5rem;">🥼</span>
              <div>
                <div style="font-weight:800; font-size:0.95rem; color:#ffffff;">
                  Langkah 2: Mengenakan Busana Ihram
                </div>
                <div style="font-size:0.7rem; color:var(--color-cyan); font-weight:700;">HUKUM: WAJIB HAJI / UMRAH</div>
              </div>
            </div>
            <span class="step-badge-status status-pending" id="badge-step-ihram">⏳ Belum</span>
          </div>
          <p style="font-size:0.83rem; color:#cbd5e1; line-height:1.45; margin-top:8px;">
            <b>Laki-laki:</b> 2 lembar kain putih tak berjahit (Izar sarung & Rida' selendang). Melepaskan pakaian berjahit, celana dalam, dan penutup kepala.<br>
            <b>Perempuan:</b> Pakaian muslimah syar'i menutup seluruh aurat kecuali wajah dan kedua telapak tangan serta mengenakan jilbab rapi.
          </p>
          <button type="button" class="btn-step-action clickable" id="btn-step-ihram" onclick="executeMiqatStep('ihram')">
            <span>🥼 Kenakan Busana Ihram Sempurna (+20 Pahala)</span>
          </button>
        </div>

        <!-- LANGKAH 3: MENGUCAPKAN NIAT IHRAM -->
        <div class="miqat-step-card" id="card-step-niat">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.5rem;">🤲</span>
              <div>
                <div style="font-weight:800; font-size:0.95rem; color:#ffffff;">
                  Langkah 3: Mengucapkan Niat Ihram
                </div>
                <div style="font-size:0.7rem; color:var(--color-gold); font-weight:700;">HUKUM: RUKUN (MUTLAK WAJIB)</div>
              </div>
            </div>
            <span class="step-badge-status status-pending" id="badge-step-niat">⏳ Belum</span>
          </div>
          <p style="font-size:0.83rem; color:#cbd5e1; line-height:1.4; margin-top:8px;">
            Menghadap ke arah kiblat, memantapkan niat di dalam hati semata-mata karena Allah Ta'ala dan melafalkan kalimat ihram:
          </p>
          <div class="amalan-doa-box" style="margin:8px 0 4px 0;" id="miqat-niat-doa-box">
            لَبَّيْكَ اللَّهُمَّ عُمْرَةً
          </div>
          <div class="amalan-arti" id="miqat-niat-arti-box">
            "Labbaikallaahumma 'umratan" — Aku penuhi panggilan-Mu ya Allah untuk berumrah.
          </div>
          <button type="button" class="btn-step-action clickable" id="btn-step-niat" onclick="executeMiqatStep('niat')">
            <span>🤲 Lafalkan Niat Ihram Menghadap Kiblat (+30 Pahala)</span>
          </button>
        </div>

        <!-- LANGKAH 4: MELAFALKAN KALIMAT TALBIYAH -->
        <div class="miqat-step-card" id="card-step-talbiyah">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.5rem;">📢</span>
              <div>
                <div style="font-weight:800; font-size:0.95rem; color:#ffffff;">
                  Langkah 4: Mengumandangkan Talbiyah
                </div>
                <div style="font-size:0.7rem; color:var(--color-emerald); font-weight:700;">HUKUM: SUNNAH SYI'AR UTAMA</div>
              </div>
            </div>
            <span class="step-badge-status status-pending" id="badge-step-talbiyah">⏳ Belum</span>
          </div>
          <p style="font-size:0.83rem; color:#cbd5e1; line-height:1.4; margin-top:8px;">
            Menyuarakan kalimat Talbiyah dengan lantang dan khusyuk sejak selesai berniat hingga tiba di depan Ka'bah:
          </p>
          <div class="amalan-doa-box" style="margin:8px 0 4px 0;">
            لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لاَ شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ لاَ شَرِيكَ لَكَ
          </div>
          <div class="amalan-arti">
            "Labbaikallaahumma labbaik, labbaika laa syariika laka labbaik. Innal hamda wan ni'mata laka wal mulk, laa syariika lak."
          </div>
          <button type="button" class="btn-step-action clickable" id="btn-step-talbiyah" onclick="executeMiqatStep('talbiyah')">
            <span>📢 Kumandangkan Suara Talbiyah (+30 Pahala)</span>
          </button>
        </div>
      </div>

      <!-- Quick Action: Complete All in 1 Click for Easy Progression -->
      <div style="margin-top:14px; display:flex; flex-direction:column; gap:8px;">
        <button type="button" class="btn-main clickable" onclick="executeAllMiqatStepsInstant()" style="background:linear-gradient(135deg, rgba(245,197,66,0.2), rgba(16,185,129,0.2)); border:1.5px solid var(--color-gold); color:var(--color-gold); font-size:0.88rem; padding:10px 16px;">
          <span>⚡ Laksanakan Semua Langkah Sekaligus (Instan Cepat)</span>
        </button>

        <div style="display:flex; gap:10px;">
          <button type="button" class="btn-main btn-secondary clickable" onclick="closeModal('modal-miqat-guide'); startCurrentPosQuiz();" style="flex:1; font-size:0.82rem; padding:10px;">
            <span>📝 Ujian Soal Bonus (+50 Poin)</span>
          </button>
          <button type="button" class="btn-main btn-secondary clickable" onclick="closeModal('modal-miqat-guide')" style="flex:1; font-size:0.82rem; padding:10px;">
            <span>Tutup</span>
          </button>
        </div>
      </div>
    </div>
  </div>
'''

# Insert modal before </body
html = html.replace('</body>', modal_miqat_html + '\n</body>', 1)
print("Inserted #modal-miqat-guide HTML!")

# 5. Add JavaScript state for miqatSteps and logic
old_state_def = 'hasReachedCurrentPosCheckpoint: false,'
new_state_def = '''hasReachedCurrentPosCheckpoint: false,
      miqatSteps: {
        bersuci: false,
        ihram: false,
        niat: false,
        talbiyah: false
      },'''

if old_state_def in html:
    html = html.replace(old_state_def, new_state_def, 1)
    print("Added miqatSteps to state!")

# 6. Add JS functions for Miqat Checklist and Easy-Assist
miqat_js = '''
    /* ===== 📋 MIQAT FIQH GUIDE & CHECKLIST LOGIC ===== */
    function openMiqatGuideModal() {
      playBeep(480, 70);
      updateMiqatModalUI();
      openModal("modal-miqat-guide");
    }

    function getMiqatCompletedCount() {
      if (!state.miqatSteps) state.miqatSteps = {};
      let c = 0;
      if (state.miqatSteps.bersuci) c++;
      if (state.miqatSteps.ihram) c++;
      if (state.miqatSteps.niat) c++;
      if (state.miqatSteps.talbiyah) c++;
      return c;
    }

    function updateMiqatModalUI() {
      const steps = state.miqatSteps || {};
      const count = getMiqatCompletedCount();
      const pct = Math.round((count / 4) * 100);

      // Update progress bar & chips
      const statTxt = document.getElementById("miqat-modal-stat-txt");
      const barEl = document.getElementById("miqat-modal-bar");
      if (statTxt) statTxt.textContent = `${count} / 4 Selesai (${pct}%)`;
      if (barEl) barEl.style.width = `${pct}%`;

      // Update chips
      const chips = ["bersuci", "ihram", "niat", "talbiyah"];
      chips.forEach(s => {
        const chip = document.getElementById(`chip-step-${s}`);
        const card = document.getElementById(`card-step-${s}`);
        const badge = document.getElementById(`badge-step-${s}`);
        const btn = document.getElementById(`btn-step-${s}`);
        const isDone = !!steps[s];

        if (chip) chip.className = `miqat-chip ${isDone ? "done" : ""}`;
        if (card) {
          if (isDone) card.classList.add("step-completed");
          else card.classList.remove("step-completed");
        }
        if (badge) {
          badge.className = `step-badge-status ${isDone ? "status-done" : "status-pending"}`;
          badge.textContent = isDone ? "✅ Selesai" : "⏳ Belum";
        }
        if (btn) {
          if (isDone) {
            btn.className = "btn-step-action done-btn";
            btn.innerHTML = "<span>✔️ Telah Dilaksanakan</span>";
            btn.disabled = true;
          } else {
            btn.className = "btn-step-action clickable";
            btn.disabled = false;
          }
        }
      });

      // Update Niat text according to Umrah vs Haji
      const niatBox = document.getElementById("miqat-niat-doa-box");
      const niatArti = document.getElementById("miqat-niat-arti-box");
      if (niatBox && niatArti) {
        if (state.mode === "HAJI") {
          niatBox.textContent = "لَبَّيْكَ اللَّهُمَّ حَجّاً (atau نَوَيْتُ الْحَجَّ وَأَحْرَمْتُ بِهِ لِلَّهِ تَعَالَى)";
          niatArti.textContent = '"Labbaikallaahumma hajjan" — Aku penuhi panggilan-Mu ya Allah untuk berhaji.';
        } else {
          niatBox.textContent = "لَبَّيْكَ اللَّهُمَّ عُمْرَةً (atau نَوَيْتُ الْعُمْرَةَ وَأَحْرَمْتُ بِهَا لِلَّهِ تَعَالَى)";
          niatArti.textContent = '"Labbaikallaahumma \'umratan" — Aku penuhi panggilan-Mu ya Allah untuk berumrah.';
        }
      }

      // Check if all 4 steps are complete
      const allDoneBanner = document.getElementById("miqat-all-done-banner");
      if (allDoneBanner) {
        allDoneBanner.style.display = (count >= 4) ? "block" : "none";
      }

      // Update HUD widget
      updateMiqatHUDWidget();
    }

    function updateMiqatHUDWidget() {
      const pill = document.getElementById("hud-miqat-pill");
      const txt = document.getElementById("hud-miqat-pill-txt");
      if (!pill || !txt) return;

      if (state.pos === 1) {
        pill.classList.add("visible");
        const count = getMiqatCompletedCount();
        const pct = Math.round((count / 4) * 100);
        if (count >= 4) {
          txt.style.color = "#34d399";
          txt.textContent = "✅ 4/4 Selesai (Lanjut ke Ka'bah)";
        } else {
          txt.style.color = "var(--color-gold)";
          txt.textContent = `${count}/4 Selesai (${pct}%)`;
        }
      } else {
        pill.classList.remove("visible");
      }
    }

    function executeMiqatStep(stepName) {
      if (!state.miqatSteps) state.miqatSteps = {};
      const isAlreadyDone = !!state.miqatSteps[stepName];

      const stepPahala = (stepName === "niat" || stepName === "talbiyah") ? 30 : 20;

      if (!isAlreadyDone) {
        state.miqatSteps[stepName] = true;
        state.pahala += stepPahala;
        showFloatingScore(`+${stepPahala} PAHALA`);
        saveLocalProgress();
        updateHUD();
      }

      if (stepName === "bersuci") {
        soundCorrect();
        toast("💧 Alhamdulillah, Mandi Sunnah Ihram & Berwudhu telah dilaksanakan!");
      } else if (stepName === "ihram") {
        soundCorrect();
        toast(state.gender === "L"
          ? "🥼 Dua lembar kain ihram putih tak berjahit telah dikenakan dengan rapi!"
          : "🧕 Busana muslimah putih tertutup syar'i & jilbab telah dikenakan sempurna!");
      } else if (stepName === "niat") {
        soundCorrect();
        toast(`🤲 Niat ihram untuk ${state.mode} telah diikrarkan menghadap kiblat!`);
      } else if (stepName === "talbiyah") {
        initTalbiyahAudioEngine();
        soundFinish();
        toast("📢 Labbaikallahumma Labbaik... Lantunan Talbiyah berkumandang indah!");
      }

      updateMiqatModalUI();

      // If all 4 are completed now
      if (getMiqatCompletedCount() >= 4) {
        soundFinish();
        soundTingChime();
        toast("🎉 Mabrur! Seluruh 4 rukun Miqat selesai. Siap berangkat ke Ka'bah!");
      }
    }

    function executeAllMiqatStepsInstant() {
      playBeep(523, 100);
      state.miqatSteps = { bersuci: true, ihram: true, niat: true, talbiyah: true };
      state.pahala += 100;
      showFloatingScore("+100 PAHALA MIQAT LENGKAP");
      initTalbiyahAudioEngine();
      soundFinish();
      soundTingChime();
      saveLocalProgress();
      updateHUD();
      updateMiqatModalUI();
      toast("⚡ Seluruh 4 amalan Miqat telah selesai sekaligus! Silakan lanjut ke Pos 2.");
    }

    function proceedFromMiqatToPos2() {
      closeModal("modal-miqat-guide");
      advanceToNextPos();
      setTimeout(() => {
        teleportTo("HAJAR_ASWAD");
        toast("🕋 Tiba di pelataran Ka'bah! Mulailah Tawaf sebanyak 7 putaran.");
      }, 500);
    }

    /* ===== KEMUDAHAN PENGERJAAN: EASY-ASSIST CONTROLS ===== */
    function assistAdvanceCurrentActivity() {
      playBeep(520, 80);
      const act = state.liveActivity;
      if (!act.active) {
        toast("💡 Tidak ada aktivitas berhitung yang sedang aktif.");
        return;
      }
      if (act.type === "tawaf") {
        act.count = Math.min(7, act.count + 1);
        soundTawafLap();
        showFloatingScore(`Putaran ${act.count}/7 Selesai!`);
        toast(`🔄 Bantu Hitung: Putaran Tawaf ke-${act.count}/7 tercatat!`);
        updateActivityHUD();
        if (act.count >= 7) completeLiveActivity();
      } else if (act.type === "sai") {
        act.count = Math.min(7, act.count + 1);
        soundTawafLap();
        showFloatingScore(`Lintasan ${act.count}/7 Selesai!`);
        toast(`🚶 Bantu Hitung: Perjalanan Sa'i ke-${act.count}/7 tercatat!`);
        updateActivityHUD();
        if (act.count >= 7) completeLiveActivity();
      } else if (act.type === "jamarat") {
        throwPebbleAtJamarat();
      }
    }

    function instantCompleteCurrentActivity() {
      playBeep(659, 120);
      const act = state.liveActivity;
      if (!act.active) {
        toast("💡 Tidak ada aktivitas yang sedang aktif.");
        return;
      }
      if (act.type === "tawaf") {
        act.count = 7;
        updateActivityHUD();
        completeLiveActivity();
      } else if (act.type === "sai") {
        act.count = 7;
        updateActivityHUD();
        completeLiveActivity();
      } else if (act.type === "wukuf") {
        act.wukufSeconds = 10;
        updateActivityHUD();
        completeLiveActivity();
      } else if (act.type === "jamarat") {
        act.stonesThrown = 7;
        updateActivityHUD();
        completeLiveActivity();
      }
      toast("⚡ Alhamdulillah! Rukun berhasil diselesaikan secara instan.");
    }
'''

# Insert miqat_js before openCurrentLocationActions
target_actions = "function openCurrentLocationActions(targetKey) {"
html = html.replace(target_actions, miqat_js + "\n    " + target_actions, 1)

# 7. When player opens actions at MIQAT, redirect to openMiqatGuideModal
actions_deck_miqat_hook = '''function openCurrentLocationActions(targetKey) {
      playBeep(440, 80);
      const lmKey = targetKey || state.currentInspectedLandmarkKey || "MIQAT";

      // If at Miqat (Pos 1), open the dedicated step-by-step Fiqh Guide & Checklist Modal
      if (lmKey === "MIQAT" || state.pos === 1) {
        openMiqatGuideModal();
        return;
      }'''

html = html.replace(target_actions, actions_deck_miqat_hook, 1)
print("Updated openCurrentLocationActions to open Miqat Guide at Miqat!")

# 8. When colliding with checkpoint at Pos 1, open Miqat Guide modal directly!
old_checkpoint_collision = '''          if (!state.hasReachedCurrentPosCheckpoint) {
            state.hasReachedCurrentPosCheckpoint = true;
            checkpointBurstFlash = 1.0;
            soundTingChime();
            showFloatingScore("✨ TING! POS TERCAPAI!");
            toast(`🎯 TING! Kamu telah sampai di ${currentPosData.title} (${targetLm.title})!`);
            // Sparkle feedback
            for (let s = 0; s < 10; s++) {
              spawnDustParticle(targetLm.x, targetLm.y + 0.5, targetLm.z);
            }
          }'''

new_checkpoint_collision = '''          if (!state.hasReachedCurrentPosCheckpoint) {
            state.hasReachedCurrentPosCheckpoint = true;
            checkpointBurstFlash = 1.0;
            soundTingChime();
            showFloatingScore("✨ TING! POS TERCAPAI!");
            toast(`🎯 TING! Kamu telah sampai di ${currentPosData.title} (${targetLm.title})!`);
            // Sparkle feedback
            for (let s = 0; s < 10; s++) {
              spawnDustParticle(targetLm.x, targetLm.y + 0.5, targetLm.z);
            }
            // Auto open Miqat Guide modal on first arrival at Pos 1 so player immediately knows what to do
            if (state.pos === 1) {
              setTimeout(() => {
                openMiqatGuideModal();
              }, 600);
            }
          }'''

html = html.replace(old_checkpoint_collision, new_checkpoint_collision, 1)
print("Added auto-open Miqat Guide on arrival at Pos 1!")

# 9. Update saveLocalProgress and loadLocalProgress to preserve miqatSteps
old_save = '''          totalQuizScore: state.totalQuizScore || 0,
          badges: state.badges,'''

new_save = '''          totalQuizScore: state.totalQuizScore || 0,
          miqatSteps: state.miqatSteps || {},
          badges: state.badges,'''

html = html.replace(old_save, new_save, 1)

old_load = '''          state.totalQuizScore = d.totalQuizScore || 0;
          state.badges = d.badges || {};'''

new_load = '''          state.totalQuizScore = d.totalQuizScore || 0;
          state.miqatSteps = d.miqatSteps || { bersuci: false, ihram: false, niat: false, talbiyah: false };
          state.badges = d.badges || {};'''

html = html.replace(old_load, new_load, 1)

# 10. Call updateMiqatHUDWidget() inside updateHUD()
old_update_hud = 'document.getElementById("hud-avatar").textContent = state.gender === "L" ? "👦" : "🧕";'
new_update_hud = '''document.getElementById("hud-avatar").textContent = state.gender === "L" ? "👦" : "🧕";
      updateMiqatHUDWidget();'''

html = html.replace(old_update_hud, new_update_hud, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch complete! Updated index.html successfully.")
