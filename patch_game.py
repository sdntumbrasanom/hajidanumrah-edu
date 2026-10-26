import re

with open('/tmp/patched_step1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Three.js loading with local fallback
three_cdn = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
three_enhanced = '''<!-- Three.js CDN with bundled NPM fallback for guaranteed offline/headless execution -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script type="module">
    import * as THREE from 'three';
    if (!window.THREE) {
      window.THREE = THREE;
    }
  </script>'''

if three_cdn in html:
    html = html.replace(three_cdn, three_enhanced, 1)
    print("Enhanced Three.js loader with local fallback!")

# 2. Add Onboarding CSS styles for cartoon background and 2-step navigation
onboard_css_target = "/* Onboarding Card */"
onboard_css_replacement = '''/* Onboarding Card with Cartoon Background & 2-Step Navigation */
    .onboarding-card-bg {
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.92) 0%, rgba(15, 23, 42, 0.97) 100%),
                  url('/assets/images/haji_umrah_cartoon.jpg') center/cover no-repeat;
      border: 1.5px solid var(--color-card-border);
      border-radius: var(--radius-card);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75), 0 0 45px rgba(245, 197, 66, 0.28);
      position: relative;
      overflow: hidden;
      animation: popModal 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .onboarding-hero-banner {
      width: 100%;
      height: 175px;
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 14px;
      position: relative;
      border: 1.5px solid rgba(245, 197, 66, 0.5);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }
    .onboarding-hero-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 25%;
      display: block;
    }
    .onboarding-step-indicator {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
    }
    .step-pill {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.1);
      color: #94a3b8;
      border: 1px solid rgba(255, 255, 255, 0.15);
      transition: all 0.2s ease;
    }
    .step-pill.active {
      background: rgba(245, 197, 66, 0.2);
      color: var(--color-gold);
      border-color: var(--color-gold);
      box-shadow: 0 0 10px rgba(245, 197, 66, 0.3);
    }
    /* Onboarding Card */'''

if onboard_css_target in html:
    html = html.replace(onboard_css_target, onboard_css_replacement, 1)
    print("Added Onboarding CSS with Cartoon theme!")

# 3. Replace #modal-onboarding HTML with 2-step wizard
modal_onboarding_regex = r'<div class="modal-backdrop" id="modal-onboarding">.*?</div>\s*</div>\s*<!-- ======================================================= -->'
new_modal_onboarding = '''<div class="modal-backdrop" id="modal-onboarding">
    <div class="card onboarding-card-bg" style="max-width:580px; text-align:center;">
      <!-- Step Indicator -->
      <div class="onboarding-step-indicator">
        <span class="step-pill active" id="step-pill-1">1. Pilih Ibadah</span>
        <span style="color:#64748b; font-size:0.75rem;">➔</span>
        <span class="step-pill" id="step-pill-2">2. Identitas & Karakter</span>
      </div>

      <!-- ================= HALAMAN 1: PILIH UMRAH ATAU HAJI ================= -->
      <div id="onboard-step-1">
        <!-- Hero Cartoon Banner -->
        <div class="onboarding-hero-banner">
          <img src="/assets/images/haji_umrah_cartoon.jpg" alt="Petualangan Haji dan Umrah Kartun" class="onboarding-hero-img">
          <div style="position:absolute; inset:0; background:linear-gradient(to top, rgba(15,23,42,0.92) 0%, rgba(15,23,42,0.3) 60%, transparent 100%); display:flex; flex-direction:column; justify-content:flex-end; padding:12px 16px; text-align:left;">
            <div style="font-size:0.75rem; color:var(--color-gold); font-weight:800; letter-spacing:1px; text-transform:uppercase;">
              🕌 SIMULASI MANASIK TANAH SUCI 3D
            </div>
            <h2 style="font-size:1.45rem; font-weight:800; color:#ffffff; line-height:1.2; text-shadow:0 2px 8px rgba(0,0,0,0.8);">
              IBADAH QUEST
            </h2>
          </div>
        </div>

        <div style="margin-bottom:14px;">
          <h3 style="font-size:1.22rem; color:var(--color-gold); font-weight:800; margin-bottom:4px;">
            Pilih Petualangan Ibadah
          </h3>
          <p style="font-size:0.84rem; color:#cbd5e1; line-height:1.45;">
            Tentukan jenis ibadah yang ingin kamu laksanakan terlebih dahulu. Amalan dan rute pos akan disesuaikan secara otomatis:
          </p>
        </div>

        <!-- Pilihan Ibadah: Umrah atau Haji -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:20px; text-align:left;">
          <div id="onboard-mode-umrah" class="onboarding-mode-btn selected" onclick="setOnboardingMode('UMRAH')">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
              <span style="font-size:2.4rem;">🕋</span>
              <span style="font-size:0.68rem; background:rgba(245,197,66,0.2); color:var(--color-gold); padding:2px 8px; border-radius:999px; font-weight:700;">4 Pos Rukun</span>
            </div>
            <span style="font-size:1.1rem; font-weight:800; color:#fff; margin-top:4px;">Ibadah Umrah</span>
            <span style="font-size:0.72rem; color:#cbd5e1; line-height:1.35;">
              Miqat ➔ Tawaf ➔ Sa'i Shafa-Marwah ➔ Tahallul
            </span>
            <div style="font-size:0.66rem; color:#10b981; font-weight:700; margin-top:4px;">
              ⏱️ Estimasi: ~10-15 Menit
            </div>
          </div>

          <div id="onboard-mode-haji" class="onboarding-mode-btn" onclick="setOnboardingMode('HAJI')">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
              <span style="font-size:2.4rem;">🏔️</span>
              <span style="font-size:0.68rem; background:rgba(56,189,248,0.2); color:var(--color-cyan); padding:2px 8px; border-radius:999px; font-weight:700;">13 Pos Lengkap</span>
            </div>
            <span style="font-size:1.1rem; font-weight:800; color:#fff; margin-top:4px;">Haji Tamattu'</span>
            <span style="font-size:0.72rem; color:#cbd5e1; line-height:1.35;">
              Miqat ➔ Tawaf ➔ Mina ➔ Wukuf Arafah ➔ Muzdalifah ➔ Lempar Jamarat
            </span>
            <div style="font-size:0.66rem; color:#38bdf8; font-weight:700; margin-top:4px;">
              ⏱️ Estimasi: ~25-35 Menit
            </div>
          </div>
        </div>

        <button type="button" class="btn-main btn-gold clickable" onclick="goToOnboardingStep(2)" style="padding:14px 20px; font-size:1.05rem;">
          <span>Lanjut ke Pengisian Data Santri ➔</span>
        </button>
      </div>

      <!-- ================= HALAMAN 2: ISI NAMA & PILIH KARAKTER ================= -->
      <div id="onboard-step-2" style="display:none;">
        <!-- Selected Mode Indicator -->
        <div style="background:rgba(245,197,66,0.12); border:1.5px solid rgba(245,197,66,0.4); border-radius:12px; padding:10px 16px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
          <div style="text-align:left;">
            <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700; letter-spacing:0.5px;">Ibadah yang Dipilih:</div>
            <div style="font-size:1rem; font-weight:800; color:var(--color-gold);" id="onboard-selected-mode-text">
              🕋 Ibadah Umrah (4 Pos Rukun)
            </div>
          </div>
          <button type="button" class="btn-main btn-secondary clickable" onclick="goToOnboardingStep(1)" style="width:auto; padding:6px 14px; font-size:0.76rem; border-color:var(--color-gold); color:var(--color-gold);">
            Ganti Ibadah
          </button>
        </div>

        <div style="margin-bottom:14px; text-align:left;">
          <h3 style="font-size:1.25rem; color:#ffffff; font-weight:800; margin-bottom:4px;">
            Identitas & Karakter Santri
          </h3>
          <p style="font-size:0.84rem; color:#cbd5e1; line-height:1.4;">
            Masukkan nama santri dan pilih busana karakter Roblox yang ingin kamu gunakan:
          </p>
        </div>

        <!-- Input Nama Santri -->
        <div style="text-align:left; margin-bottom:16px;">
          <label style="font-size:0.82rem; color:var(--color-gold); font-weight:700;">
            👤 Nama Santri / Siswa:
          </label>
          <input type="text" id="onboard-name-input" placeholder="Ketik nama lengkap Anda (contoh: Muhammad Al-Fatih)" style="width:100%; padding:12px 16px; background:rgba(30,41,59,0.9); border:1.5px solid var(--color-card-border); border-radius:12px; color:#fff; font-family:inherit; font-size:0.95rem; margin-top:6px; outline:none;" onkeydown="if(event.key==='Enter') submitOnboarding()">
        </div>

        <!-- Pilihan Karakter & Busana -->
        <div style="text-align:left; margin-bottom:22px;">
          <label style="font-size:0.82rem; color:#cbd5e1; font-weight:700;">Pilih Karakter & Busana:</label>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:6px;">
            <button type="button" id="onboard-gender-L" class="gender-pill-btn selected" onclick="setOnboardingGender('L')" style="flex-direction:column; padding:12px 10px; gap:4px;">
              <span style="font-size:2rem;">👦</span>
              <span style="font-weight:700; font-size:0.88rem;">Santri Putra</span>
              <span style="font-size:0.68rem; color:#94a3b8;">Kain Ihram Putih & Peci</span>
            </button>
            <button type="button" id="onboard-gender-P" class="gender-pill-btn" onclick="setOnboardingGender('P')" style="flex-direction:column; padding:12px 10px; gap:4px;">
              <span style="font-size:2rem;">🧕</span>
              <span style="font-weight:700; font-size:0.88rem;">Santri Putri</span>
              <span style="font-size:0.68rem; color:#94a3b8;">Muslimah Berjilbab Rapi</span>
            </button>
          </div>
        </div>

        <!-- Buttons Row -->
        <div style="display:flex; gap:12px;">
          <button type="button" class="btn-main btn-secondary clickable" onclick="goToOnboardingStep(1)" style="flex:1;">
            <span>⬅️ Kembali</span>
          </button>
          <button type="button" class="btn-main btn-gold clickable" onclick="submitOnboarding()" style="flex:2; font-size:1.02rem;">
            <span>🚀 Bismillah, Mulai Ibadah</span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- ======================================================= -->'''

html = re.sub(modal_onboarding_regex, new_modal_onboarding, html, flags=re.DOTALL)
print("Replaced #modal-onboarding with 2-step onboarding!")

# 4. Update Profile Modal gender button labels to match Jilbab
profile_gender_old = '''          <button type="button" class="btn-main btn-secondary clickable" id="gender-btn-L" onclick="changeGender('L')">
            <span>👦</span> <span>Santri Putra (Ihram)</span>
          </button>
          <button type="button" class="btn-main btn-secondary clickable" id="gender-btn-P" onclick="changeGender('P')">
            <span>👧</span> <span>Santri Putri (Jilbab)</span>
          </button>'''

profile_gender_new = '''          <button type="button" class="btn-main btn-secondary clickable" id="gender-btn-L" onclick="changeGender('L')">
            <span>👦</span> <span>Santri Putra (Ihram)</span>
          </button>
          <button type="button" class="btn-main btn-secondary clickable" id="gender-btn-P" onclick="changeGender('P')">
            <span>🧕</span> <span>Santri Putri (Muslimah Berjilbab)</span>
          </button>'''

if profile_gender_old in html:
    html = html.replace(profile_gender_old, profile_gender_new, 1)
    print("Updated profile modal gender labels!")

# 5. Replace buildRobloxCharacter with high quality Jilbab & Gamis for female character
char_regex = r'function buildRobloxCharacter\(\)\s*\{.*?playerGroup\.position\.set\(playerPhysics\.x, playerPhysics\.y, playerPhysics\.z\);\s*scene\.add\(playerGroup\);\s*\}'

new_build_roblox_character = '''function buildRobloxCharacter() {
      if (playerGroup) scene.remove(playerGroup);
      playerGroup = new THREE.Group();
      const isMale = state.gender === "L";
      const brownSkinColor = 0x9c6538;
      const blushPinkColor = 0xc27a64;
      const skinMat = new THREE.MeshStandardMaterial({ color: brownSkinColor, roughness: 0.65, metalness: 0.05 });
      const blushMat = new THREE.MeshBasicMaterial({ color: blushPinkColor });
      const ihramMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.85, metalness: 0.0 });
      const beltGreenMat = new THREE.MeshStandardMaterial({ color: 0x1b5e20, roughness: 0.6 });

      // Torso
      const torsoMesh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.35, 0.65), ihramMat);
      torsoMesh.position.y = 1.6;
      torsoMesh.castShadow = true;
      playerGroup.add(torsoMesh);

      if (isMale) {
        // Green belt for male ihram
        const belt = new THREE.Mesh(new THREE.BoxGeometry(1.24, 0.18, 0.68), beltGreenMat);
        belt.position.y = 1.15;
        playerGroup.add(belt);
      }

      // Head
      const head = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.75, 0.75), skinMat);
      head.position.y = 2.65;
      head.castShadow = true;
      playerGroup.add(head);

      // Eyes
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x140c06 });
      const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.11, 0.05), eyeMat);
      eyeL.position.set(0.18, 2.68, 0.38);
      playerGroup.add(eyeL);
      const eyeR = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.11, 0.05), eyeMat);
      eyeR.position.set(-0.18, 2.68, 0.38);
      playerGroup.add(eyeR);

      // Cute blush for female santri
      if (!isMale) {
        const blushL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.06, 0.04), blushMat);
        blushL.position.set(0.22, 2.56, 0.38);
        playerGroup.add(blushL);
        const blushR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.06, 0.04), blushMat);
        blushR.position.set(-0.22, 2.56, 0.38);
        playerGroup.add(blushR);
      }

      // Headwear & Jilbab
      if (isMale) {
        // Peci hitam santri putra
        const peciMat = new THREE.MeshStandardMaterial({ color: 0x141414, roughness: 0.8 });
        const peci = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.28, 0.78), peciMat);
        peci.position.y = 3.05;
        playerGroup.add(peci);
      } else {
        // Jilbab / Hijab Muslimah Cantik & Rapi (Multi-Part 3D Jilbab)
        const hijabClothMat = new THREE.MeshStandardMaterial({ color: 0xfafafa, roughness: 0.85, metalness: 0.02 });
        const ciputMat = new THREE.MeshStandardMaterial({ color: 0xf1ebe1, roughness: 0.8 });

        // 1. Ciput / Inner headband under hijab
        const ciput = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.12, 0.77), ciputMat);
        ciput.position.set(0, 2.94, 0.03);
        playerGroup.add(ciput);

        // 2. Jilbab Crown / Top Dome covering hair
        const hijabTop = new THREE.Mesh(new THREE.BoxGeometry(0.88, 0.38, 0.88), hijabClothMat);
        hijabTop.position.set(0, 3.06, -0.01);
        playerGroup.add(hijabTop);

        // 3. Jilbab Back Drape covering neck and back of head
        const hijabBack = new THREE.Mesh(new THREE.BoxGeometry(0.88, 0.95, 0.22), hijabClothMat);
        hijabBack.position.set(0, 2.5, -0.4);
        playerGroup.add(hijabBack);

        // 4. Jilbab Left & Right Side Cheek Drapes framing the face
        const hijabL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.78, 0.68), hijabClothMat);
        hijabL.position.set(0.42, 2.55, 0.04);
        playerGroup.add(hijabL);

        const hijabR = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.78, 0.68), hijabClothMat);
        hijabR.position.set(-0.42, 2.55, 0.04);
        playerGroup.add(hijabR);

        // 5. Jilbab Bergo / Khimar Shoulder Drape (covering chest and neck)
        const hijabChest = new THREE.Mesh(new THREE.BoxGeometry(1.28, 0.52, 0.74), hijabClothMat);
        hijabChest.position.set(0, 2.05, 0.04);
        playerGroup.add(hijabChest);

        // 6. Gold Brooch / Pin on Jilbab
        const broochMat = new THREE.MeshStandardMaterial({ color: 0xf5c542, metalness: 0.88, roughness: 0.18 });
        const brooch = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.04, 10), broochMat);
        brooch.rotation.x = Math.PI / 2;
        brooch.position.set(0, 2.15, 0.44);
        playerGroup.add(brooch);
      }

      // Arms
      const armGeo = new THREE.BoxGeometry(0.48, 1.25, 0.48);
      armGeo.translate(0, -0.5, 0);
      const armMat = isMale ? skinMat : ihramMat; // Female has white long sleeves
      const armL = new THREE.Mesh(armGeo, armMat);
      armL.position.set(0.85, 2.2, 0);
      armL.castShadow = true;
      playerGroup.add(armL);
      const armR = new THREE.Mesh(armGeo, armMat);
      armR.position.set(-0.85, 2.2, 0);
      armR.castShadow = true;
      playerGroup.add(armR);

      // Hands exposed in skin tone for female (sesuai syariat aurat wanita: wajah dan telapak tangan)
      if (!isMale) {
        const handGeo = new THREE.BoxGeometry(0.38, 0.22, 0.38);
        const handL = new THREE.Mesh(handGeo, skinMat);
        handL.position.set(0.85, 0.96, 0);
        playerGroup.add(handL);
        const handR = new THREE.Mesh(handGeo, skinMat);
        handR.position.set(-0.85, 0.96, 0);
        playerGroup.add(handR);
      }

      // Legs / Lower Body
      const legL = new THREE.Group(); legL.position.set(0.32, 1.2, 0);
      const legR = new THREE.Group(); legR.position.set(-0.32, 1.2, 0);

      if (isMale) {
        // Santri Putra: 2-piece ihram with exposed lower legs
        const upperLegGeo = new THREE.BoxGeometry(0.55, 0.85, 0.55);
        upperLegGeo.translate(0, -0.42, 0);
        const upperLegL = new THREE.Mesh(upperLegGeo, ihramMat);
        upperLegL.castShadow = true; legL.add(upperLegL);
        const upperLegR = new THREE.Mesh(upperLegGeo, ihramMat);
        upperLegR.castShadow = true; legR.add(upperLegR);

        const lowerLegGeo = new THREE.BoxGeometry(0.48, 0.45, 0.48);
        lowerLegGeo.translate(0, -0.95, 0);
        const lowerLegL = new THREE.Mesh(lowerLegGeo, skinMat); legL.add(lowerLegL);
        const lowerLegR = new THREE.Mesh(lowerLegGeo, skinMat); legR.add(lowerLegR);
      } else {
        // Santri Putri: Long modest Gamis / Abaya white dress covering full legs
        const dressGeo = new THREE.BoxGeometry(1.24, 1.35, 0.72);
        const dress = new THREE.Mesh(dressGeo, ihramMat);
        dress.position.y = 0.75;
        dress.castShadow = true;
        playerGroup.add(dress);

        // Modest feet / slippers
        const shoeGeo = new THREE.BoxGeometry(0.44, 0.16, 0.55);
        const shoeMat = new THREE.MeshStandardMaterial({ color: 0x5a3d28, roughness: 0.8 });
        const shoeL = new THREE.Mesh(shoeGeo, shoeMat);
        shoeL.position.set(0.32, 0.08, 0.05);
        legL.add(shoeL);
        const shoeR = new THREE.Mesh(shoeGeo, shoeMat);
        shoeR.position.set(-0.32, 0.08, 0.05);
        legR.add(shoeR);
      }

      playerGroup.add(legL);
      playerGroup.add(legR);

      // Shadow Disc
      const shadowDisc = new THREE.Mesh(
        new THREE.PlaneGeometry(1.4, 1.4),
        new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.35, depthWrite: false })
      );
      shadowDisc.rotation.x = -Math.PI / 2;
      shadowDisc.position.y = 0.03;
      playerGroup.add(shadowDisc);

      // Overhead Golden Beacon Pin (prominent in top-down view)
      const pinGeo = new THREE.ConeGeometry(0.32, 0.75, 8);
      const pinMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
      const pinMesh = new THREE.Mesh(pinGeo, pinMat);
      pinMesh.rotation.x = Math.PI; // point downward towards head
      pinMesh.position.y = 4.1;
      playerGroup.add(pinMesh);

      playerLimbs = { armL, armR, legL, legR, torso: torsoMesh, head, pin: pinMesh };
      playerGroup.position.set(playerPhysics.x, playerPhysics.y, playerPhysics.z);
      scene.add(playerGroup);
    }'''

html = re.sub(char_regex, new_build_roblox_character, html, flags=re.DOTALL)
print("Updated buildRobloxCharacter with Muslimah Jilbab!")

# 6. Add "Ting!" chime sound function & Checkpoint 3D marker
ting_audio_code = '''    /* ===== 🔔 CHECKPOINT "TING!" CHIME & AUDIO ===== */
    function soundTingChime() {
      if (state.isMuted) return;
      hapticFeedback([40, 25, 65]);
      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;
      // High harmonic crystal bell chime ("TING! ✨")
      const freqs = [1046.5, 1567.98, 2093.0, 3135.96]; // C6, G6, C7, G7
      freqs.forEach((f, idx) => {
        try {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(f, now);
          const initialVol = 0.18 / (idx + 1);
          gain.gain.setValueAtTime(initialVol, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.25 - idx * 0.18);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 1.3);
        } catch (e) {}
      });
    }

    /* ===== 🎯 3D POS CHECKPOINT MARKER SYSTEM ===== */
    let currentPosCheckpointGroup = null;
    let checkpointDiamondMesh = null;
    let checkpointBeamMesh = null;
    let checkpointFloorRings = [];
    let checkpointBurstFlash = 0;

    function buildPosCheckpointMarker() {
      if (currentPosCheckpointGroup) scene.remove(currentPosCheckpointGroup);
      currentPosCheckpointGroup = new THREE.Group();

      // 1. Glowing celestial light pillar
      const beamGeo = new THREE.CylinderGeometry(2.4, 2.4, 14, 24, 1, true);
      const beamMat = new THREE.MeshBasicMaterial({
        color: 0xf5c542,
        transparent: true,
        opacity: 0.35,
        side: THREE.DoubleSide,
        depthWrite: false
      });
      checkpointBeamMesh = new THREE.Mesh(beamGeo, beamMat);
      checkpointBeamMesh.position.y = 7;
      currentPosCheckpointGroup.add(checkpointBeamMesh);

      // 2. Floating spinning Golden-Emerald Diamond Gem
      const diamondGeo = new THREE.OctahedronGeometry(1.2, 0);
      const diamondMat = new THREE.MeshStandardMaterial({
        color: 0xf5c542,
        emissive: 0x10b981,
        emissiveIntensity: 0.85,
        metalness: 0.85,
        roughness: 0.15
      });
      checkpointDiamondMesh = new THREE.Mesh(diamondGeo, diamondMat);
      checkpointDiamondMesh.position.y = 3.6;
      checkpointDiamondMesh.castShadow = true;
      currentPosCheckpointGroup.add(checkpointDiamondMesh);

      // 3. Floating Target Pin above Diamond
      const targetPin = new THREE.Mesh(
        new THREE.ConeGeometry(0.38, 0.85, 8),
        new THREE.MeshBasicMaterial({ color: 0xffea85 })
      );
      targetPin.rotation.x = Math.PI;
      targetPin.position.y = 5.2;
      currentPosCheckpointGroup.add(targetPin);

      // 4. Concentric expanding ground radar rings
      checkpointFloorRings = [];
      const ringColors = [0xf5c542, 0x10b981];
      for (let i = 0; i < 2; i++) {
        const ringGeo = new THREE.RingGeometry(1.4 + i * 1.5, 1.8 + i * 1.5, 32);
        const ringMat = new THREE.MeshBasicMaterial({
          color: ringColors[i],
          transparent: true,
          opacity: 0.8,
          side: THREE.DoubleSide,
          depthWrite: false
        });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.rotation.x = -Math.PI / 2;
        ringMesh.position.y = 0.32 + i * 0.02;
        currentPosCheckpointGroup.add(ringMesh);
        checkpointFloorRings.push({ mesh: ringMesh, baseRadius: 1.4 + i * 1.5 });
      }

      scene.add(currentPosCheckpointGroup);
      updatePosCheckpointPosition();
    }

    function updatePosCheckpointPosition() {
      if (!currentPosCheckpointGroup) return;
      const posData = getCurrentPosData();
      if (!posData) {
        currentPosCheckpointGroup.visible = false;
        return;
      }
      const lm = LANDMARKS[posData.landmarkKey] || LANDMARKS.KABAH;
      currentPosCheckpointGroup.position.set(lm.x, lm.y, lm.z);
      currentPosCheckpointGroup.visible = true;
    }

    function updatePosCheckpointAnimation(dt, now) {
      if (!currentPosCheckpointGroup || !currentPosCheckpointGroup.visible) return;
      if (checkpointDiamondMesh) {
        checkpointDiamondMesh.rotation.y += dt * 2.2;
        checkpointDiamondMesh.rotation.z = Math.sin(now * 0.002) * 0.2;
        checkpointDiamondMesh.position.y = 3.4 + Math.sin(now * 0.0035) * 0.35;
        if (checkpointBurstFlash > 0) {
          checkpointBurstFlash -= dt * 2.5;
          checkpointDiamondMesh.material.emissiveIntensity = Math.max(0.85, 0.85 + checkpointBurstFlash * 3.5);
        }
      }
      if (checkpointBeamMesh) {
        checkpointBeamMesh.rotation.y -= dt * 0.5;
        checkpointBeamMesh.material.opacity = 0.26 + Math.sin(now * 0.003) * 0.14;
      }
      checkpointFloorRings.forEach((r, idx) => {
        const scale = 1 + (Math.sin(now * 0.004 + idx * 1.5) * 0.22);
        r.mesh.scale.set(scale, scale, 1);
      });
    }
'''

# Insert ting_audio_code before init3DWorld
init_3d_target = "function init3DWorld() {"
html = html.replace(init_3d_target, ting_audio_code + "\n    " + init_3d_target, 1)
print("Added Ting chime & Checkpoint 3D marker code!")

# 7. Call buildPosCheckpointMarker() in init3DWorld()
build_mutawwif_target = "buildMutawwifNPCs();"
html = html.replace(build_mutawwif_target, build_mutawwif_target + "\n      buildPosCheckpointMarker();", 1)

# 8. Call updatePosCheckpointAnimation in tick(now)
update_mutawwif_target = "updateMutawwifNPCs(dt, now);"
html = html.replace(update_mutawwif_target, update_mutawwif_target + "\n        updatePosCheckpointAnimation(dt, now);", 1)

# 9. Add Checkpoint collision detection inside updateRealtimeActivities
activity_hud_check = 'const currentPosData = getCurrentPosData();\n      if (!currentPosData) return;'
checkpoint_collision_code = '''const currentPosData = getCurrentPosData();
      if (!currentPosData) return;

      // 🎯 Checkpoint Collision & Ting! Chime Detection
      if (currentPosCheckpointGroup) {
        const targetLm = LANDMARKS[currentPosData.landmarkKey] || LANDMARKS.KABAH;
        const distToCheckpoint = Math.hypot(playerPhysics.x - targetLm.x, playerPhysics.z - targetLm.z);

        if (distToCheckpoint <= 4.2) {
          if (!state.hasReachedCurrentPosCheckpoint) {
            state.hasReachedCurrentPosCheckpoint = true;
            checkpointBurstFlash = 1.0;
            soundTingChime();
            showFloatingScore("✨ TING! POS TERCAPAI!");
            toast(`🎯 TING! Kamu telah sampai di ${currentPosData.title} (${targetLm.title})!`);
            // Sparkle feedback
            for (let s = 0; s < 10; s++) {
              spawnDustParticle(targetLm.x, targetLm.y + 0.5, targetLm.z);
            }
          }
        }
      }'''

html = html.replace(activity_hud_check, checkpoint_collision_code, 1)
print("Added Checkpoint collision detection to updateRealtimeActivities!")

# 10. Reset checkpoint trigger state in advanceToNextPos, switchMode, teleportTo
advance_target = "state.completedPos[oldPosNum] = true;"
advance_replacement = '''state.completedPos[oldPosNum] = true;
      state.hasReachedCurrentPosCheckpoint = false;
      updatePosCheckpointPosition();'''
html = html.replace(advance_target, advance_replacement, 1)

switch_target = "state.liveActivity.active = false;"
switch_replacement = '''state.liveActivity.active = false;
      state.hasReachedCurrentPosCheckpoint = false;
      updatePosCheckpointPosition();'''
html = html.replace(switch_target, switch_replacement, 1)

# 11. Update Onboarding JS functions: goToOnboardingStep, setOnboardingMode, setOnboardingGender, submitOnboarding
old_onboard_js = '''    /* ===== ONBOARDING LOGIN & PILIHAN UMRAH / HAJI ===== */
    let tempOnboardingGender = "L";
    let tempOnboardingMode = "UMRAH";'''

new_onboard_js = '''    /* ===== ONBOARDING LOGIN & 2-STEP WIZARD (UMRAH/HAJI -> NAMA & KARAKTER) ===== */
    let tempOnboardingGender = "L";
    let tempOnboardingMode = "UMRAH";
    let currentOnboardingStep = 1;

    function goToOnboardingStep(step) {
      playBeep(480, 60);
      currentOnboardingStep = step;
      const step1El = document.getElementById("onboard-step-1");
      const step2El = document.getElementById("onboard-step-2");
      const pill1 = document.getElementById("step-pill-1");
      const pill2 = document.getElementById("step-pill-2");

      if (step === 1) {
        if (step1El) step1El.style.display = "block";
        if (step2El) step2El.style.display = "none";
        if (pill1) pill1.classList.add("active");
        if (pill2) pill2.classList.remove("active");
      } else {
        if (step1El) step1El.style.display = "none";
        if (step2El) step2El.style.display = "block";
        if (pill1) pill1.classList.remove("active");
        if (pill2) pill2.classList.add("active");
        // Update selected mode text badge
        const modeBadge = document.getElementById("onboard-selected-mode-text");
        if (modeBadge) {
          if (tempOnboardingMode === "UMRAH") {
            modeBadge.innerHTML = "🕋 <b>Ibadah Umrah</b> (4 Pos Rukun)";
          } else {
            modeBadge.innerHTML = "🏔️ <b>Haji Tamattu'</b> (13 Pos Lengkap)";
          }
        }
        // Focus name input
        setTimeout(() => {
          const inp = document.getElementById("onboard-name-input");
          if (inp) inp.focus();
        }, 150);
      }
    }'''

html = html.replace(old_onboard_js, new_onboard_js, 1)

# 12. Update setOnboardingGender and setOnboardingMode
old_set_onboard = '''    function setOnboardingGender(g) {
      tempOnboardingGender = g;
      const btnL = document.getElementById("onboard-gender-L");
      const btnP = document.getElementById("onboard-gender-P");
      if (btnL) btnL.className = `gender-pill-btn ${g === "L" ? "selected" : ""}`;
      if (btnP) btnP.className = `gender-pill-btn ${g === "P" ? "selected" : ""}`;
    }
    function setOnboardingMode(m) {
      tempOnboardingMode = m;
      const bUmrah = document.getElementById("onboard-mode-umrah");
      const bHaji = document.getElementById("onboard-mode-haji");
      if (bUmrah) bUmrah.className = `onboarding-mode-btn ${m === "UMRAH" ? "selected" : ""}`;
      if (bHaji) bHaji.className = `onboarding-mode-btn ${m === "HAJI" ? "selected" : ""}`;
    }'''

new_set_onboard = '''    function setOnboardingGender(g) {
      playBeep(440, 50);
      tempOnboardingGender = g;
      const btnL = document.getElementById("onboard-gender-L");
      const btnP = document.getElementById("onboard-gender-P");
      if (btnL) btnL.className = `gender-pill-btn ${g === "L" ? "selected" : ""}`;
      if (btnP) btnP.className = `gender-pill-btn ${g === "P" ? "selected" : ""}`;
    }
    function setOnboardingMode(m) {
      playBeep(480, 60);
      tempOnboardingMode = m;
      const bUmrah = document.getElementById("onboard-mode-umrah");
      const bHaji = document.getElementById("onboard-mode-haji");
      if (bUmrah) bUmrah.className = `onboarding-mode-btn ${m === "UMRAH" ? "selected" : ""}`;
      if (bHaji) bHaji.className = `onboarding-mode-btn ${m === "HAJI" ? "selected" : ""}`;
    }'''

html = html.replace(old_set_onboard, new_set_onboard, 1)

# 13. Update openOnboardingModal to reset to step 1
old_open_onboard = '''    function openOnboardingModal() {
      const nameInput = document.getElementById("onboard-name-input");
      if (nameInput) {
        nameInput.value = (state.nama && state.nama !== "Santri Petualang") ? state.nama : "";
      }
      setOnboardingGender(state.gender || "L");
      setOnboardingMode(state.mode || "UMRAH");
      openModal("modal-onboarding");
    }'''

new_open_onboard = '''    function openOnboardingModal() {
      const nameInput = document.getElementById("onboard-name-input");
      if (nameInput) {
        nameInput.value = (state.nama && state.nama !== "Santri Petualang") ? state.nama : "";
      }
      setOnboardingGender(state.gender || "L");
      setOnboardingMode(state.mode || "UMRAH");
      goToOnboardingStep(1);
      openModal("modal-onboarding");
    }'''

html = html.replace(old_open_onboard, new_open_onboard, 1)

# 14. Update submitOnboarding to position checkpoint marker and sound
old_submit_onboard = '''      buildRobloxCharacter();
      updateHUD();
      closeModal("modal-onboarding");
      initTalbiyahAudioEngine();
      updateTalbiyahProximity();
      teleportTo("MIQAT");
      soundFinish();'''

new_submit_onboard = '''      buildRobloxCharacter();
      updateHUD();
      closeModal("modal-onboarding");
      initTalbiyahAudioEngine();
      updateTalbiyahProximity();
      state.hasReachedCurrentPosCheckpoint = false;
      updatePosCheckpointPosition();
      teleportTo("MIQAT");
      soundTingChime();
      soundFinish();'''

html = html.replace(old_submit_onboard, new_submit_onboard, 1)

# 15. Update HUD avatar for female to jilbab emoji
old_hud_avatar = 'document.getElementById("hud-avatar").textContent = state.gender === "L" ? "👦" : "👧"'
new_hud_avatar = 'document.getElementById("hud-avatar").textContent = state.gender === "L" ? "👦" : "🧕"'
html = html.replace(old_hud_avatar, new_hud_avatar, 1)

# 16. Add hasReachedCurrentPosCheckpoint to initial state
old_state = 'nearbyMutawwifId: null,'
new_state = '''nearbyMutawwifId: null,
      hasReachedCurrentPosCheckpoint: false,'''
html = html.replace(old_state, new_state, 1)

with open('/tmp/final_index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch complete! Generated /tmp/final_index.html")
