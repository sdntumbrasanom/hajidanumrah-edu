import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Onboarding Background to be full viewport and translucent/transparent
old_onboard_css = '''.onboarding-card-bg {
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.92) 0%, rgba(15, 23, 42, 0.97) 100%),
                  url('/assets/images/haji_umrah_cartoon.jpg') center/cover no-repeat;
      border: 1.5px solid var(--color-card-border);
      border-radius: var(--radius-card);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75), 0 0 45px rgba(245, 197, 66, 0.28);
      position: relative;
      overflow: hidden;
      animation: popModal 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }'''

new_onboard_css = '''/* Fullscreen and Translucent / Transparent Cartoon Background */
    #modal-onboarding {
      background: url('/assets/images/haji_umrah_cartoon.jpg') center/cover no-repeat fixed !important;
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
      z-index: 100;
    }
    #modal-onboarding.active {
      display: flex !important;
    }
    #modal-onboarding::before {
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at center, rgba(15, 23, 42, 0.55) 0%, rgba(15, 23, 42, 0.85) 100%);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 0;
      pointer-events: none;
    }
    .onboarding-card-bg {
      background: rgba(15, 23, 42, 0.78) !important;
      backdrop-filter: blur(18px) !important;
      -webkit-backdrop-filter: blur(18px) !important;
      border: 1.5px solid rgba(245, 197, 66, 0.55);
      border-radius: var(--radius-card);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.8), 0 0 45px rgba(245, 197, 66, 0.3);
      position: relative;
      z-index: 2;
      overflow: hidden;
      animation: popModal 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }'''

if old_onboard_css in html:
    html = html.replace(old_onboard_css, new_onboard_css, 1)
    print("Updated onboarding background to full and transparent!")

# 2. Add Jamarat dedicated throw controls in the HUD
old_jamarat_dock = '''        <div class="act-badge-title" id="live-act-title">TAWAF KA'BAH</div>'''
new_jamarat_dock = '''        <div class="act-badge-title" id="live-act-title">TAWAF KA'BAH</div>
        <!-- Jamarat Dedicated Pillar Throw Cluster (Ula, Wustha, Aqabah) -->
        <div id="jamarat-throw-cluster" style="display:none; margin:8px 0; width:100%;">
          <div style="font-size:0.75rem; color:#cbd5e1; margin-bottom:6px;">Pilih Pilar Jamarat & Lempar Kerikil:</div>
          <div style="display:flex; gap:6px; justify-content:center; flex-wrap:wrap;">
            <button type="button" class="btn-main clickable" id="btn-throw-ula" onclick="throwPebbleAtSpecificPillar('ULA')" style="width:auto; padding:8px 12px; font-size:0.8rem; background:linear-gradient(135deg, #10b981, #047857); color:#fff; border:1px solid #6ee7b7;">
              🪨 Lempar Jumrah Ula
            </button>
            <button type="button" class="btn-main clickable" id="btn-throw-wustha" onclick="throwPebbleAtSpecificPillar('WUSTHA')" style="width:auto; padding:8px 12px; font-size:0.8rem; background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; border:1px solid #7dd3fc;">
              🪨 Lempar Jumrah Wustha
            </button>
            <button type="button" class="btn-main clickable" id="btn-throw-aqabah" onclick="throwPebbleAtSpecificPillar('AQABAH')" style="width:auto; padding:8px 12px; font-size:0.8rem; background:linear-gradient(135deg, #f5c542, #d97706); color:#0f172a; border:1px solid #fff; font-weight:800;">
              🪨 Lempar Jumrah Aqabah
            </button>
          </div>
        </div>'''

if old_jamarat_dock in html:
    html = html.replace(old_jamarat_dock, new_jamarat_dock, 1)
    print("Added Jamarat dedicated throw cluster to live activity HUD!")

# 3. Add Muzdalifah Pebble Pickup Modal
modal_muzdalifah_html = '''
  <!-- ======================================================= -->
  <!-- MODAL: MEMUNGUT KERIKIL DI MUZDALIFAH                   -->
  <!-- ======================================================= -->
  <div class="modal-backdrop" id="modal-muzdalifah-pebbles">
    <div class="card" style="max-width:540px; text-align:center;">
      <div class="modal-header-row">
        <h3 class="modal-title-gold"><span>🌙</span> <span>Memungut Kerikil di Muzdalifah</span></h3>
        <button class="btn-close-modal clickable" onclick="closeModal('modal-muzdalifah-pebbles')">✕</button>
      </div>
      <p style="font-size:0.86rem; color:#cbd5e1; line-height:1.5; margin-bottom:14px; text-align:left;">
        Malam tanggal 10 Dzulhijjah di Padang Muzdalifah. Jamaah disunnahkan memungut batu kerikil kecil seukuran biji kacang untuk melontar jumrah di Mina.
      </p>

      <div style="background:rgba(30, 41, 59, 0.7); border:1px solid var(--color-gold); border-radius:14px; padding:14px; margin-bottom:16px; text-align:left;">
        <div style="font-size:0.75rem; color:var(--color-cyan); font-weight:800; text-transform:uppercase; margin-bottom:4px;">
          SOAL FIQH MUZDALIFAH SEBELUM MEMUNGUT KERIKIL:
        </div>
        <p style="font-size:0.92rem; color:#ffffff; font-weight:600; line-height:1.5; margin-bottom:12px;" id="muzdalifah-question-txt">
          Berapa ukuran batu kerikil yang disunnahkan oleh Rasulullah SAW untuk melontar jumrah?
        </p>
        <div id="muzdalifah-choices-container"></div>
      </div>

      <div id="muzdalifah-success-box" style="display:none; background:rgba(6,78,59,0.7); border:1.5px solid #34d399; border-radius:12px; padding:12px; margin-bottom:14px;">
        <div style="color:#6ee7b7; font-weight:800; font-size:0.95rem;">✅ Kerikil Berhasil Dikumpulkan! (+30 Pahala)</div>
        <div style="font-size:0.8rem; color:#e2e8f0; margin-top:2px;">7 butir kerikil telah tersimpan di kantong untuk melempar Jumrah Aqabah.</div>
      </div>

      <div style="display:flex; gap:10px;">
        <button type="button" class="btn-main btn-gold clickable" id="btn-muzdalifah-next" onclick="closeModal('modal-muzdalifah-pebbles'); advanceToNextPos();" style="display:none; flex:1;">
          <span>🚀 Lanjut ke POS 8 (Jamarat Aqabah) ➔</span>
        </button>
        <button type="button" class="btn-main btn-secondary clickable" onclick="closeModal('modal-muzdalifah-pebbles')" style="width:auto; padding:10px 16px;">
          Tutup
        </button>
      </div>
    </div>
  </div>
'''

html = html.replace('</body>', modal_muzdalifah_html + '\n</body>', 1)
print("Added #modal-muzdalifah-pebbles HTML!")

# 4. Insert Pos-Specific Question Pool & Shuffle Logic in JS
pos_questions_js = '''
    /* ===== 🔀 RANDOMIZED QUESTION POOL PER POS & CHOICES SHUFFLER ===== */
    function shuffleArray(arr) {
      const result = [...arr];
      for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [result[i], result[j]] = [result[j], result[i]];
      }
      return result;
    }

    function shuffleChoices(choices) {
      const letters = ["A", "B", "C", "D"];
      const shuffled = shuffleArray(choices);
      return shuffled.map((ch, idx) => ({
        ...ch,
        key: letters[idx] || String(idx + 1)
      }));
    }

    const POS_SPECIFIC_QUESTIONS = {
      MIQAT: [
        {
          q: "Apa yang dimaksud dengan 'Miqat Makani' dalam ibadah haji dan umrah?",
          choices: [
            { text: "Batas tempat yang ditentukan syariat untuk memulai niat ihram", correct: true },
            { text: "Batas waktu berakhirnya ibadah tawaf", correct: false },
            { text: "Tempat membeli oleh-oleh kurma dan cinderamata", correct: false },
            { text: "Pintu gerbang masuk hotel di Makkah", correct: false }
          ],
          edu: "Miqat Makani adalah batas geografis resmi tempat jamaah wajib berniat ihram dan mengenakan kain ihram sebelum melangkah masuk ke Tanah Suci Makkah."
        },
        {
          q: "Apa hukum mengenakan pakaian berjahit bagi laki-laki yang sudah berniat ihram di Miqat?",
          choices: [
            { text: "Diharamkan, dan jika dilanggar wajib membayar dam/fidyah", correct: true },
            { text: "Boleh asal warnanya putih bersih", correct: false },
            { text: "Sunnah muakkadah", correct: false },
            { text: "Makruh saja tanpa denda", correct: false }
          ],
          edu: "Laki-laki yang sedang berihram diharamkan memakai pakaian berjahit, sepatu yang menutup mata kaki, dan penutup kepala yang menempel."
        },
        {
          q: "Bagi jamaah yang datang dari Madinah (atau gelombang 1), di manakah lokasi Miqat Makani mereka?",
          choices: [
            { text: "Dzulhulaifah (Bir Ali)", correct: true },
            { text: "Yalamlam", correct: false },
            { text: "Juhfah", correct: false },
            { text: "Qarnul Manazil", correct: false }
          ],
          edu: "Miqat bagi penduduk Madinah dan yang melewatinya adalah Dzulhulaifah yang kini dikenal sebagai Masjid Bir Ali."
        }
      ],
      KABAH: [
        {
          q: "Berapa putaran Tawaf yang wajib dilaksanakan saat mengelilingi Ka'bah dan dari mana memulainya?",
          choices: [
            { text: "7 putaran sempurna, dimulai dan diakhiri lurus dari garis Hajar Aswad", correct: true },
            { text: "3 putaran saja cukup, dimulai dari Maqam Ibrahim", correct: false },
            { text: "10 putaran, dimulai dari pintu Ka'bah", correct: false },
            { text: "7 putaran, dimulai dari bukit Shafa", correct: false }
          ],
          edu: "Tawaf wajib 7 putaran berlawanan jarum jam, posisi Ka'bah selalu di sisi kiri badan, mulai dan berakhir di sudut Hajar Aswad."
        },
        {
          q: "Di manakah posisi Ka'bah terhadap tubuh orang yang sedang melakukan Tawaf?",
          choices: [
            { text: "Ka'bah selalu berada di sisi kiri tubuh jamaah", correct: true },
            { text: "Ka'bah selalu berada di sisi kanan tubuh jamaah", correct: false },
            { text: "Ka'bah berada di belakang tubuh jamaah", correct: false },
            { text: "Bebas menghadap mana saja asalkan berputar", correct: false }
          ],
          edu: "Syarat sah tawaf adalah posisi Ka'bah selalu berada di sebelah kiri orang yang bertawaf."
        },
        {
          q: "Apakah sah putaran tawaf seorang jamaah jika ia berjalan memotong melalui dalam lengkungan Hijr Ismail?",
          choices: [
            { text: "Tidak sah, karena Hijr Ismail adalah bagian dari Ka'bah itu sendiri", correct: true },
            { text: "Sah dan mendapatkan pahala berlipat ganda", correct: false },
            { text: "Sah asalkan membaca takbir", correct: false },
            { text: "Sah khusus bagi jamaah lansia", correct: false }
          ],
          edu: "Hijr Ismail termasuk bagian dari dalam Ka'bah. Siapa yang tawaf di dalam Hijr Ismail berarti tidak mengitari Ka'bah seutuhnya."
        }
      ],
      HAJAR_ASWAD: [
        {
          q: "Apa yang disunnahkan saat berada lurus di hadapan Hajar Aswad pada setiap awal putaran Tawaf bila tidak memungkinkan menciumnya?",
          choices: [
            { text: "Melambaikan tangan kanan (istilam) sambil mengucap 'Bismillahi Allahu Akbar'", correct: true },
            { text: "Berdesak-desakan dan mendorong jamaah lain demi menciumnya", correct: false },
            { text: "Berbalik arah membelakangi Ka'bah", correct: false },
            { text: "Melemparkan uang koin ke arah Hajar Aswad", correct: false }
          ],
          edu: "Jika kondisi padat, cukup menghadapkan diri ke Hajar Aswad, melambaikan tangan kanan dan bertakbir tanpa menyakiti sesama muslim."
        }
      ],
      SHAFA: [
        {
          q: "Berapa kali perjalanan Sa'i yang harus ditempuh antara Bukit Shafa dan Bukit Marwah?",
          choices: [
            { text: "7 kali perjalanan (Shafa ke Marwah dihitung 1, berakhir di Marwah)", correct: true },
            { text: "7 kali bolak-balik (total 14 kali perjalanan)", correct: false },
            { text: "3 kali perjalanan saja", correct: false },
            { text: "Bebas sampai merasa lelah", correct: false }
          ],
          edu: "Sa'i ditempuh 7 kali perjalanan: Shafa ke Marwah (1), Marwah ke Shafa (2), hingga genap ke-7 berakhir di Marwah."
        },
        {
          q: "Di manakah ibadah Sa'i WAJIB dimulai dan diakhiri?",
          choices: [
            { text: "Dimulai dari Bukit Shafa dan diakhiri di Bukit Marwah", correct: true },
            { text: "Dimulai dari Bukit Marwah dan diakhiri di Bukit Shafa", correct: false },
            { text: "Dimulai dari Maqam Ibrahim dan diakhiri di Hijr Ismail", correct: false },
            { text: "Bebas dari bukit mana saja", correct: false }
          ],
          edu: "Rasulullah SAW bersabda: 'Mulailah dengan apa yang Allah mulai dengannya (Bukit Shafa).' (HR. Muslim)"
        },
        {
          q: "Apa yang disunnahkan saat melintasi zona antara dua pilar lampu hijau di Mas'a bagi jamaah laki-laki?",
          choices: [
            { text: "Berlari-lari kecil (ramal / jogging)", correct: true },
            { text: "Duduk bersila istirahat", correct: false },
            { text: "Melompat setinggi-tingginya", correct: false },
            { text: "Berjalan lambat sambil diam tanpa doa", correct: false }
          ],
          edu: "Laki-laki disunnahkan berlari kecil di antara dua pilar hijau meneladani Siti Hajar. Bagi perempuan tetap berjalan biasa."
        }
      ],
      MARWAH: [
        {
          q: "Apa amalan yang dilakukan di Bukit Marwah setelah menuntaskan putaran ke-7 Sa'i untuk mengakhiri ihram umrah?",
          choices: [
            { text: "Tahallul dengan mencukur atau memotong rambut minimal 3 helai", correct: true },
            { text: "Memotong kuku tangan dan kaki", correct: false },
            { text: "Langsung mandi dan ganti baju tanpa cukur rambut", correct: false },
            { text: "Membeli parfum baru di toko", correct: false }
          ],
          edu: "Tahallul adalah mencukur gundul (halq) atau memendekkan (taqshir) minimal 3 helai rambut, tanda sah dan selesainya umrah."
        }
      ],
      ARAFAH: [
        {
          q: "Rasulullah SAW bersabda: 'Al-Hajju 'Arafah' (Inti haji adalah Arafah). Kapan waktu wukuf di Padang Arafah?",
          choices: [
            { text: "Tanggal 9 Dzulhijjah, mulai tergelincir matahari (Dzuhur) hingga fajar 10 Dzulhijjah", correct: true },
            { text: "Tanggal 8 Dzulhijjah sepanjang hari", correct: false },
            { text: "Tanggal 10 Dzulhijjah setelah shalat Idul Adha", correct: false },
            { text: "Bebas hari apa saja di bulan Dzulhijjah", correct: false }
          ],
          edu: "Wukuf di Arafah pada 9 Dzulhijjah adalah rukun haji paling utama yang tidak boleh ditinggalkan sama sekali."
        },
        {
          q: "Apakah hukum ibadah haji seseorang yang tidak sempat hadir di padang Arafah pada waktu wukuf?",
          choices: [
            { text: "Hajinya tidak sah / gugur dan tidak bisa ditebus dengan dam", correct: true },
            { text: "Hajinya tetap sah asalkan membayar dam kambing", correct: false },
            { text: "Cukup diganti dengan puasa 10 hari", correct: false },
            { text: "Sah bila mewakilkannya kepada orang lain", correct: false }
          ],
          edu: "Wukuf adalah rukun haji mutlak. Siapa yang tertinggal wukuf, maka hajinya batal dan wajib mengulang di tahun depan."
        }
      ],
      MUZDALIFAH: [
        {
          q: "Apa dua amalan utama yang dilakukan jamaah haji saat tiba dan mabit di Padang Muzdalifah pada malam 10 Dzulhijjah?",
          choices: [
            { text: "Shalat jamak takhir Maghrib-Isya dan memungut batu kerikil", correct: true },
            { text: "Tawaf mengelilingi bukit dan menyembelih kurban", correct: false },
            { text: "Memotong rambut tahallul dan mandi besar", correct: false },
            { text: "Membeli tenda dan tidur sepanjang malam tanpa shalat", correct: false }
          ],
          edu: "Di Muzdalifah jamaah shalat jamak qashar Maghrib-Isya serta mengumpulkan kerikil kecil untuk melempar jumrah."
        },
        {
          q: "Berapa ukuran batu kerikil yang disunnahkan untuk melempar jumrah?",
          choices: [
            { text: "Seukuran biji kacang tanah (khasyaf)", correct: true },
            { text: "Sebesar buah kelapa", correct: false },
            { text: "Sebesar batu bata", correct: false },
            { text: "Batu pasir halus seperti debu", correct: false }
          ],
          edu: "Nabi SAW mencontohkan kerikil kecil seukuran biji kacang (khasyaf). Menggunakan batu besar dilarang karena berlebihan dan berbahaya."
        }
      ],
      JAMARAT: [
        {
          q: "Pada tanggal 10 Dzulhijjah (Hari Nahr), jumrah apakah yang HANYA boleh dilempar oleh jamaah haji?",
          choices: [
            { text: "Hanya Jumrah Aqabah saja sebanyak 7 kerikil", correct: true },
            { text: "Ketiga jumrah (Ula, Wustha, dan Aqabah) sekaligus", correct: false },
            { text: "Hanya Jumrah Ula saja", correct: false },
            { text: "Tidak ada lemparan jumrah di hari Nahr", correct: false }
          ],
          edu: "Pada 10 Dzulhijjah jamaah HANYA melontar Jumrah Aqabah dengan 7 kerikil. Ketiga jumrah baru dilempar pada hari tasyrik."
        },
        {
          q: "Pada hari-hari Tasyrik (11, 12, dan 13 Dzulhijjah), bagaimana urutan melempar tiga jumrah yang sah menurut syariat?",
          choices: [
            { text: "Berurutan: Jumrah Ula (Sughra) ➔ Jumrah Wustha ➔ Jumrah Aqabah (Kubra)", correct: true },
            { text: "Dimulai dari Aqabah ➔ Wustha ➔ Ula", correct: false },
            { text: "Bebas melempar mana saja terlebih dahulu", correct: false },
            { text: "Cukup melempar pilar tengah (Wustha) saja", correct: false }
          ],
          edu: "Urutan melontar pada hari tasyrik wajib tertib: Jumrah Ula (pertama), lalu Wustha (tengah), dan diakhiri Aqabah."
        },
        {
          q: "Bolehkah melempar pilar Jamarat dengan sandal, sepatu, atau botol minuman?",
          choices: [
            { text: "Dilarang keras, wajib melempar dengan batu kerikil sesuai sunnah Nabi SAW", correct: true },
            { text: "Boleh bila tidak menemukan batu kerikil", correct: false },
            { text: "Boleh asal sandal yang bersih", correct: false },
            { text: "Sunnah menggunakan sepatu kulit", correct: false }
          ],
          edu: "Melempar dengan sandal atau benda lain dilarang dan menyalahi sunnah Rasulullah SAW."
        }
      ],
      MINA: [
        {
          q: "Apa hukum mabit (menginap) di Mina pada malam-malam hari Tasyrik bagi jamaah haji?",
          choices: [
            { text: "Wajib Haji, jika ditinggalkan tanpa uzur wajib membayar Dam", correct: true },
            { text: "Rukun haji yang membatalkan haji jika tidak hadir", correct: false },
            { text: "Sunnah biasa tanpa konsekuensi apa-apa", correct: false },
            { text: "Haram hukumnya bermalam di tenda", correct: false }
          ],
          edu: "Mabit di Mina pada malam hari tasyrik adalah Wajib Haji. Ditinggalkan tanpa uzur syar'i dikenakan dam."
        }
      ],
      SELINGAN: [
        {
          q: "[Selingan Teori Fiqh] Manakah di bawah ini yang merupakan 5 Syarat Wajib Haji?",
          choices: [
            { text: "Islam, Baligh, Berakal, Merdeka, dan Istitha'ah (Mampu)", correct: true },
            { text: "Islam, Menikah, Kaya raya, dan Usia di atas 50 tahun", correct: false },
            { text: "Keturunan bangsawan dan hafal Al-Qur'an 30 juz", correct: false },
            { text: "Sudah umrah minimal 5 kali berturut-turut", correct: false }
          ],
          edu: "Syarat wajib haji ada 5: Islam, Baligh, Berakal, Merdeka, dan Istitha'ah (mampu fisik, bekal nafkah, dan aman perjalanan)."
        },
        {
          q: "[Selingan Teori Fiqh] Apa perbedaan mendasar antara 'Rukun Haji' dan 'Wajib Haji'?",
          choices: [
            { text: "Rukun jika ditinggalkan haji batal tidak sah; Wajib jika ditinggalkan haji tetap sah namun wajib bayar Dam", correct: true },
            { text: "Rukun dan wajib haji adalah sama persis tidak ada bedanya", correct: false },
            { text: "Wajib haji lebih tinggi kedudukannya daripada rukun haji", correct: false },
            { text: "Rukun haji boleh ditinggalkan asalkan berpuasa 3 hari", correct: false }
          ],
          edu: "Rukun haji tidak bisa ditebus dengan apapun (tidak sah hajinya). Wajib haji sah hajinya namun berdosa jika sengaja dan wajib bayar dam."
        },
        {
          q: "[Selingan Teori Fiqh] Haji Tamattu' yang umumnya dilakukan jamaah Indonesia adalah cara berhaji dengan:",
          choices: [
            { text: "Mendahulukan ibadah Umrah terlebih dahulu, bertahallul bebas, baru berihram haji pada 8 Dzulhijjah", correct: true },
            { text: "Hanya berniat haji saja tanpa melaksanakan umrah sama sekali", correct: false },
            { text: "Menggabungkan niat haji dan umrah dalam satu amalan tanpa jeda tahallul", correct: false },
            { text: "Berhaji tanpa perlu wukuf di padang Arafah", correct: false }
          ],
          edu: "Tamattu' berarti bersenang-senang menikmati jeda halal antara selesainya umrah kedatangan dan masuknya waktu haji pada 8 Dzulhijjah."
        }
      ]
    };

    function getQuestionsForCurrentPos(posData) {
      const lmKey = (posData && posData.landmarkKey) ? posData.landmarkKey : "MIQAT";
      const specificPool = POS_SPECIFIC_QUESTIONS[lmKey] || POS_SPECIFIC_QUESTIONS.MIQAT;
      const selinganPool = POS_SPECIFIC_QUESTIONS.SELINGAN;

      // Shuffle pools
      const shuffledSpecific = shuffleArray(specificPool);
      const shuffledSelingan = shuffleArray(selinganPool);

      // Pick up to 3 specific questions + 2 selingan
      const selected = [];
      shuffledSpecific.slice(0, 3).forEach(q => selected.push({ ...q, topic: `Materi Pos: ${posData.title}` }));
      shuffledSelingan.slice(0, 2).forEach(q => selected.push({ ...q, topic: `Selingan Fiqh: Syarat & Rukun` }));

      // Shuffle overall question order so students can't guess patterns
      const finalQuestions = shuffleArray(selected);

      // Shuffle choices for EACH question and reassign A, B, C, D
      return finalQuestions.map(q => ({
        ...q,
        choices: shuffleChoices(q.choices)
      }));
    }
'''

# 5. Update startFiveQuestionsPreAmalan to use getQuestionsForCurrentPos
old_start_quiz = '''function startFiveQuestionsPreAmalan(lmKey, actionIndex) {
      const qs = getFiveQuestionsList();'''

new_start_quiz = '''function startFiveQuestionsPreAmalan(lmKey, actionIndex) {
      const posData = getCurrentPosData() || { title: "Pos Ibadah", landmarkKey: lmKey };
      const qs = getQuestionsForCurrentPos(posData);'''

html = html.replace(old_start_quiz, pos_questions_js + '\n    ' + new_start_quiz, 1)
print("Added randomized pos-specific question pool and shuffler!")

# 6. Fix Tawaf vs Jamarat bug in openCurrentLocationActions & startInWorldActivity
old_open_actions = '''function openCurrentLocationActions(targetKey) {
      playBeep(440, 80);
      const lmKey = targetKey || state.currentInspectedLandmarkKey || "MIQAT";

      // If at Miqat (Pos 1), open the dedicated step-by-step Fiqh Guide & Checklist Modal
      if (lmKey === "MIQAT" || state.pos === 1) {
        openMiqatGuideModal();
        return;
      }
      const lm = LANDMARKS[lmKey] || LANDMARKS.MIQAT;'''

new_open_actions = '''function openCurrentLocationActions(targetKey) {
      playBeep(440, 80);
      const posData = getCurrentPosData();

      // If at Miqat (Pos 1), open the dedicated step-by-step Fiqh Guide & Checklist Modal
      if (state.pos === 1 || targetKey === "MIQAT") {
        openMiqatGuideModal();
        return;
      }

      // If at Muzdalifah (Pos 7 in Haji), open Muzdalifah pebble picking modal
      if (state.mode === "HAJI" && state.pos === 7) {
        openMuzdalifahPebbleModal();
        return;
      }

      // Strictly prioritize active quest landmark so Tawaf NEVER triggers Jamarat!
      let lmKey = targetKey;
      if (!lmKey) {
        if (posData && posData.landmarkKey) {
          lmKey = posData.landmarkKey;
        } else {
          lmKey = state.currentInspectedLandmarkKey || "KABAH";
        }
      }

      // Special guarantee: if quest is Tawaf (Pos 2 / 10 / 13), force KABAH / HAJAR_ASWAD
      if (posData && (posData.pos === 2 || posData.pos === 10 || posData.pos === 13)) {
        lmKey = "KABAH";
      }

      const lm = LANDMARKS[lmKey] || LANDMARKS.KABAH;'''

html = html.replace(old_open_actions, new_open_actions, 1)
print("Fixed Tawaf vs Jamarat priority bug in openCurrentLocationActions!")

# 7. Add Visible Throwing Animation & Specific Pillar target in throwPebbleAtJamarat
jamarat_functions = '''
    /* ===== 🪨 VISIBLE JAMARAT PEBBLE THROW ANIMATION & MULTI-PILLAR TARGETING ===== */
    const JAMARAT_PILLARS = {
      ULA: { x: -60, y: 4, z: -5, name: "Jumrah Ula" },
      WUSTHA: { x: -60, y: 4, z: -15, name: "Jumrah Wustha" },
      AQABAH: { x: -60, y: 4, z: -25, name: "Jumrah Aqabah" }
    };

    let activeTargetPillarKey = "AQABAH";

    function throwPebbleAtSpecificPillar(pillarKey) {
      activeTargetPillarKey = pillarKey || "AQABAH";
      throwPebbleAtJamarat();
    }

    function throwPebbleAtJamarat() {
      if (!state.liveActivity.active || state.liveActivity.type !== "jamarat") {
        // If not in live activity yet, start it
        startInWorldActivity("jamarat");
      }
      if (state.liveActivity.stonesThrown >= 7) return;
      state.liveActivity.stonesThrown++;

      soundPebbleClack();
      hapticFeedback([35, 20, 50]);

      // 1. VISIBLE CHARACTER THROW ANIMATION (Roblox right arm swing forward)
      if (playerLimbs && playerLimbs.armR) {
        playerLimbs.armR.rotation.x = 1.2; // pull back
        if (playerLimbs.torso) playerLimbs.torso.rotation.x = -0.15;
        setTimeout(() => {
          if (playerLimbs && playerLimbs.armR) {
            playerLimbs.armR.rotation.x = -1.8; // swing forward release!
            if (playerLimbs.torso) playerLimbs.torso.rotation.x = 0.22;
          }
          setTimeout(() => {
            if (playerLimbs && playerLimbs.armR) playerLimbs.armR.rotation.x = 0;
            if (playerLimbs.torso) playerLimbs.torso.rotation.x = 0;
          }, 240);
        }, 75);
      }

      // 2. 3D FLYING PEBBLE WITH ARC TRAJECTORY
      const pillarCfg = JAMARAT_PILLARS[activeTargetPillarKey] || JAMARAT_PILLARS.AQABAH;
      const pebble = new THREE.Mesh(
        new THREE.DodecahedronGeometry(0.32),
        new THREE.MeshStandardMaterial({ color: 0x5a544d, roughness: 0.9 })
      );
      pebble.position.set(playerPhysics.x, playerPhysics.y + 1.8, playerPhysics.z);

      const targetPillar = new THREE.Vector3(pillarCfg.x, pillarCfg.y, pillarCfg.z);
      const dir = targetPillar.clone().sub(pebble.position).normalize();
      pebble.userData = {
        velocity: dir.multiplyScalar(24).add(new THREE.Vector3(0, 6.5, 0)),
        life: 1.3
      };
      scene.add(pebble);
      flyingPebbles.push(pebble);

      toast(`🪨 Bismillahi Allahu Akbar! Kerikil ke-${state.liveActivity.stonesThrown}/7 dilempar ke ${pillarCfg.name}.`);
      showFloatingScore(`Kerikil ${state.liveActivity.stonesThrown}/7`);
      updateActivityHUD();

      if (state.liveActivity.stonesThrown >= 7) {
        setTimeout(() => completeLiveActivity(), 1000);
      }
    }

    /* ===== 🌙 MUZDALIFAH PEBBLE PICKING QUIZ ===== */
    function openMuzdalifahPebbleModal() {
      playBeep(480, 80);
      const qData = POS_SPECIFIC_QUESTIONS.MUZDALIFAH[1] || POS_SPECIFIC_QUESTIONS.MUZDALIFAH[0];
      const qTxt = document.getElementById("muzdalifah-question-txt");
      const cBox = document.getElementById("muzdalifah-choices-container");
      const successBox = document.getElementById("muzdalifah-success-box");
      const nextBtn = document.getElementById("btn-muzdalifah-next");

      if (successBox) successBox.style.display = "none";
      if (nextBtn) nextBtn.style.display = "none";

      if (qTxt) qTxt.textContent = qData.q;
      if (cBox) {
        cBox.innerHTML = "";
        const shuffled = shuffleChoices(qData.choices);
        shuffled.forEach(ch => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "choice-option-btn clickable";
          btn.innerHTML = `<span class="choice-badge-key">${ch.key}</span> <span>${ch.text}</span>`;
          btn.onclick = () => submitMuzdalifahAnswer(ch.correct, qData.edu);
          cBox.appendChild(btn);
        });
      }
      openModal("modal-muzdalifah-pebbles");
    }

    function submitMuzdalifahAnswer(isCorrect, edu) {
      if (isCorrect) {
        soundCorrect();
        soundPebbleClack();
        // Visible character bend animation to pick up stones
        if (playerLimbs && playerLimbs.torso) {
          playerLimbs.torso.rotation.x = 0.65;
          setTimeout(() => { if (playerLimbs && playerLimbs.torso) playerLimbs.torso.rotation.x = 0; }, 400);
        }
        state.pahala += 30;
        showFloatingScore("+30 PAHALA KERIKIL MUZDALIFAH");
        saveLocalProgress();
        updateHUD();

        const successBox = document.getElementById("muzdalifah-success-box");
        const nextBtn = document.getElementById("btn-muzdalifah-next");
        if (successBox) successBox.style.display = "block";
        if (nextBtn) nextBtn.style.display = "inline-flex";
        toast("✅ Jawaban Benar! 7 butir kerikil Muzdalifah berhasil dikumpulkan.");
      } else {
        soundWrong();
        toast("❌ Belum tepat. Pelajari dalil dan coba pilih kembali!");
      }
    }
'''

# Replace old throwPebbleAtJamarat with enhanced version
throw_regex = r'function throwPebbleAtJamarat\(\)\s*\{.*?updateActivityHUD\(\);\s*if \(state\.liveActivity\.stonesThrown >= 7\) \{\s*setTimeout\(\(\) => completeLiveActivity\(\), 1000\);\s*\}\s*\}'
html = re.sub(throw_regex, jamarat_functions, html, flags=re.DOTALL)
print("Replaced throwPebbleAtJamarat with multi-pillar throw and Muzdalifah modal!")

# 8. Show Jamarat throwing cluster when Jamarat is active, hide when Tawaf
old_update_act_hud = 'countEl.textContent = `Putaran ${act.count}/7`;'
new_update_act_hud = '''countEl.textContent = `Putaran ${act.count}/7`;
        const jCluster = document.getElementById("jamarat-throw-cluster");
        if (jCluster) jCluster.style.display = "none";'''
html = html.replace(old_update_act_hud, new_update_act_hud, 1)

old_jamarat_act_hud = 'countEl.textContent = `Kerikil ${act.stonesThrown}/7`;'
new_jamarat_act_hud = '''countEl.textContent = `Kerikil ${act.stonesThrown}/7`;
        const jCluster = document.getElementById("jamarat-throw-cluster");
        if (jCluster) jCluster.style.display = "block";'''
html = html.replace(old_jamarat_act_hud, new_jamarat_act_hud, 1)
print("Updated HUD to toggle Jamarat cluster!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("All patches applied successfully to index.html!")
