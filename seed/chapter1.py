"""Chapter 1: The Memory Incident — Array & Memory (all 8 modes)"""
import json

def seed(db, models):
    M = models
    ch = M.Chapter(slug="the-memory-incident", title="The Memory Incident",
        subtitle="Array & Memory Fundamentals", topic="Array & Memory",
        description="Production crash karena memory leak. Kamu harus paham array dari low-level sampai high-level.",
        order=1, is_published=True)
    db.session.add(ch); db.session.flush()

    # ══════════════ STORY (scenes + lines) ══════════════
    story = [
        ("intro", "00_intro.md", 0, False, None, [
            ("narrator", "// NexaPay HQ — Jakarta. 08:47 AM.", None, None),
            ("narrator", "// Hari pertamamu sebagai Backend Engineer.", None, None),
            ("narrator", "// Tiba-tiba semua layar berkedip merah.", None, None),
            ("narrator", "OUT OF MEMORY — payment-service-prod-07", "error", None),
            ("boss", "Semua ke war room. SEKARANG.", None, None),
        ]),
        ("warroom", "01_warroom.md", 1, False, None, [
            ("boss", "Payment service crash. 30K transaksi stuck. 1 jam sebelum SLA breach.", None, None),
            ("sora", "Masalahnya di batch processing — array yang grow tanpa batas di heap.", None, None),
            ("riku", "Heap usage naik 4GB dalam 10 menit.", None, None),
            ("boss", "Fix sekarang. Taufik, kamu ikut.", None, None),
            ("narrator", "// Pilih investigasi path:", None,
             json.dumps([{"label": "-> Ikut Riku — memory level", "next_scene_slug": "riku_memory"},
                         {"label": "-> Ikut Sora — algorithm", "next_scene_slug": "sora_algo"}])),
        ]),
        ("riku_memory", "02_riku_memory.md", 2, True, "investigation", [
            ("riku", "Waktu nulis int[] transactions = new int[5], JVM minta blok memory MENYAMBUNG.", None, None),
            ("narrator", "  Heap Memory:\n  [0x100][0x104][0x108][0x10C][0x110]\n   [0]    [1]    [2]    [3]    [4]\n  4 bytes each — CONTIGUOUS", "o", None),
            ("riku", "Mereka BERSEBELAHAN. Contiguous. Kayak loker kantor.", None, None),
            ("riku", "Karena contiguous, JVM bisa hitung posisi langsung:", None, None),
            ("narrator", "  address = base + (index x 4)\n  transactions[3] = 0x100 + 12 = 0x10C", "o", None),
            ("riku", "Itu namanya offset. Makanya access O(1) — langsung loncat.", None, None),
            ("riku", "Index mulai 0 karena elemen pertama nggak punya offset.", None, None),
            ("riku", "Masalah production: array baru di setiap loop tanpa release.", None, None),
            ("narrator", "  while (hasMoreBatches()) {\n      int[] buf = new int[100000]; // BARU TERUS\n      processBatch(buf);\n  }", "error", None),
            ("riku", "Setiap iterasi: 400KB baru. 10 menit = Out of Memory.", None, None),
        ]),
        ("sora_algo", "02_sora_algo.md", 2, True, "investigation", [
            ("sora", "Array punya trade-off yang jelas:", None, None),
            ("narrator", "  Access [i]    O(1)  — hitung offset\n  Search         O(n)  — cek satu-satu\n  Insert mid     O(n)  — geser semua\n  Resize         O(n)  — copy semua", "o", None),
            ("sora", "Array juara kalau SIZE sudah tahu dan butuh random access cepat.", None, None),
            ("sora", "Kayak meja makan: pesan untuk 5, datang 10 — harus pindah meja.", None, None),
            ("taufik", "Jadi setiap resize, semua di-copy?", None, None),
            ("sora", "Exactly. Fix: allocate SATU buffer di luar loop, reuse.", None, None),
            ("narrator", "  ArrayList strategy:\n  Capacity: 10 -> 20 -> 40 -> 80\n  Amortized add: O(1)", "o", None),
        ]),
        ("kai_bridge", "03_bridge.md", 3, False, None, [
            ("kai", "Gabungan Riku dan Sora:", None, None),
            ("narrator", "  1. Contiguous -> access O(1) -> offset calc\n  2. Fixed size -> resize O(n) -> copy semua\n  3. Memory terbatas -> allocate terus = crash", "o", None),
            ("kai", "Big O itu cuma cara ngukur apa yang terjadi di hardware.", None, None),
            ("kai", "O(1) bukan magic — karena memory contiguous.", None, None),
            ("taufik", "Big O = deskripsi hardware pakai matematika?", None, None),
            ("kai", "EXACTLY.", None, None),
        ]),
        ("challenge", "04_challenge.java", 4, False, None, [
            ("sora", "Bug di processBatches(). Array di-allocate tiap iterasi.", None, None),
            ("riku", "Kamu perlu SATU buffer, reuse berulang.", None, None),
            ("narrator", "// TODO: Fix the memory leak", "error", None),
        ]),
        ("resolution", "05_resolution.md", 5, False, None, [
            ("narrator", "BUILD PASSED — DEPLOYED TO PROD", "success", None),
            ("boss", "Memory stable. Good work.", None, None),
            ("kai", "Hari pertama deploy hotfix ke prod. Legend.", None, None),
            ("riku", "...Lumayan.", None, None),
        ]),
    ]
    for slug, fn, order, ict, cg, lines in story:
        sc = M.Scene(chapter_id=ch.id, slug=slug, filename=fn, order=order,
                     is_choice_target=ict, choice_group=cg)
        db.session.add(sc); db.session.flush()
        for i, (char, text, style, choice) in enumerate(lines):
            db.session.add(M.Line(scene_id=sc.id, char=char, text=text, style=style,
                                  order=i, choice_options=choice))

    # ══════════════ CHALLENGE ══════════════
    db.session.add(M.Challenge(chapter_id=ch.id,
        buggy_code="public void processBatches() {\n    while (hasMoreBatches()) {\n        int[] buffer = new int[100000];\n        loadBatch(buffer);\n        processPayments(buffer);\n    }\n}",
        fixed_code="public void processBatches() {\n    int[] buffer = new int[100000];\n    while (hasMoreBatches()) {\n        loadBatch(buffer);\n        processPayments(buffer);\n    }\n}",
        starter_code="public void processBatches() {\n    // TODO: allocate buffer di luar loop\n    \n    while (hasMoreBatches()) {\n        \n        loadBatch(buffer);\n        processPayments(buffer);\n    }\n}",
        validation_rules=json.dumps([
            {"type": "regex_match", "pattern": "int\\[\\]\\s*buffer\\s*=\\s*new\\s*int\\[\\d+\\]", "error": "Declare buffer di LUAR loop."},
            {"type": "regex_not_match_inside", "outer": "while[\\s\\S]*", "pattern": "new\\s+int\\[", "error": "Masih new di dalam loop!"},
        ]),
        hints=json.dumps(["Pindahkan int[] buffer = new int[100000]; ke SEBELUM while loop."]),
    ))

    # ══════════════ DEEP DIVE ══════════════
    for i, (ti, co, cd, ky) in enumerate([
        ("L1 — Apa itu Array?",
         "Array = deretan kotak BERSEBELAHAN di memory.\n\nKayak loker kantor: kamu booking 5 loker, dapat 100-104 — sebelahan, bukan random.\n\nDi Java: int[] arr = new int[5] → JVM allocate 5 x 4 byte = 20 byte contiguous di heap.",
         "int[] arr = new int[5];\n// JVM: \"Siapin 20 byte bersebelahan di heap\"\n// arr di stack = alamat ke blok di heap\n\n// Heap:\n// [0x100][0x104][0x108][0x10C][0x110]\n//   [0]    [1]    [2]    [3]    [4]",
         "Array = contiguous memory. JVM allocate blok bersebelahan di heap."),
        ("L2 — Offset: Kenapa Index Mulai 0",
         "Offset = jarak dari posisi awal (base address).\n\nKayak bioskop: kamu di kursi A1. Teman di A4 = 3 kursi dari kamu. Offset = 3.\n\nRumus: address = base + (index x size). Elemen pertama offset = 0 karena sudah di base.",
         "// base = 0x100, tiap int = 4 byte\narr[0] = 0x100 + (0 x 4) = 0x100  // no offset\narr[1] = 0x100 + (1 x 4) = 0x104\narr[3] = 0x100 + (3 x 4) = 0x10C  // langsung!",
         "Offset = jarak dari base. Index 0 karena elemen pertama sudah di base address."),
        ("L3 — O(1) Access: Kenapa Cepat",
         "Karena array contiguous, JVM bisa HITUNG posisi elemen manapun tanpa cari satu-satu.\n\nSatu operasi matematika: base + (index x size) → langsung ke alamat. Nggak peduli array size 5 atau 5 juta — sama cepatnya.\n\nItu O(1): constant time. Jumlah operasi nggak tergantung jumlah data.",
         "// Array size 5 — access arr[3]:\n// 0x100 + (3 x 4) = 0x10C → 1 calculation\n\n// Array size 5,000,000 — access arr[3000000]:\n// 0x100 + (3000000 x 4) = ... → still 1 calculation\n\n// SAMA cepatnya. Itu O(1).",
         "O(1) karena satu hitung langsung sampai. Nggak cari satu-satu."),
        ("L4 — O(n) Resize: Kenapa Mahal",
         "Array size FIXED setelah dibuat. Mau tambah? Harus:\n1. Bikin array baru yang lebih besar\n2. Copy SEMUA elemen dari lama ke baru\n3. Array lama jadi sampah (GC bersihin)\n\nKayak pindah meja di restoran: 5 orang datang lagi → copy semua piring ke meja baru.",
         "// resize dari 5 ke 10:\nint[] old = arr;                    // simpan referensi\narr = new int[10];                  // allocate baru\nSystem.arraycopy(old, 0, arr, 0, 5); // copy 5 elemen\n// old jadi sampah → GC\n\n// 5 elemen = 5 copy. 1 juta = 1 juta copy. = O(n)",
         "Resize = allocate baru + copy semua. Makin banyak elemen, makin lama. O(n)."),
        ("L5 — Array vs ArrayList",
         "Array: fixed size, kamu manage sendiri.\nArrayList: dynamic, Java handle resize otomatis.\n\nArrayList internally pakai array. Waktu penuh, dia double capacity → copy. Amortized O(1) add.\n\nKapan pakai apa?\n- Array: tahu size pasti, performance critical\n- ArrayList: size dinamis, convenience",
         "// Array — manual, fixed\nint[] arr = new int[100];\n\n// ArrayList — auto-resize\nArrayList<Integer> list = new ArrayList<>();\nlist.add(1); // internal: [1, _, _, _, _, _, _, _, _, _]\nlist.add(2); // internal: [1, 2, _, _, _, _, _, _, _, _]\n// capacity 10 -> 20 -> 40 saat penuh",
         "Array: fixed, manual. ArrayList: dynamic, auto-resize. Keduanya array di dalamnya."),
    ]):
        db.session.add(M.DeepDive(chapter_id=ch.id, order=i, title=ti, content=co, code=cd, keypoint=ky))

    # ══════════════ PRACTICE ══════════════
    for i, (qt, q, code, opts, ans, ex, cat) in enumerate([
        ("mcq", "int[] arr = new int[5]; berapa byte di heap?", None,
         json.dumps(["5", "10", "20", "40"]), "2", "int=4B x 5 = 20 bytes.", "size"),
        ("mcq", "Kenapa array access O(1)?", None,
         json.dumps(["Karena kecil", "Karena contiguous + offset calc", "Karena di stack"]), "1",
         "Contiguous memory = bisa hitung alamat langsung.", "complexity"),
        ("mcq", "Kenapa index mulai dari 0?", None,
         json.dumps(["Konvensi", "Elemen pertama offset-nya 0", "Bug lama"]), "1",
         "Elemen pertama sudah di base address. Offset = 0.", "offset"),
        ("mcq", "Resize array dari 100 ke 200 elemen. Berapa operasi copy?", None,
         json.dumps(["1", "100", "200", "300"]), "1",
         "Copy semua 100 elemen lama ke array baru. O(n) = O(100).", "complexity"),
        ("mcq", "Array di Java disimpan di mana?", None,
         json.dumps(["Stack", "Heap", "Register"]), "1",
         "Array = reference type. Data di heap, alamat di stack.", "memory"),
        ("mcq", "arr[3] — berapa kali JVM hitung alamat?", None,
         json.dumps(["1 kali", "3 kali", "4 kali"]), "0",
         "Satu perhitungan: base + (3 x size). O(1).", "offset"),
        ("mcq", "Insert elemen di tengah array size n. Big O?", None,
         json.dumps(["O(1)", "O(log n)", "O(n)"]), "2",
         "Harus geser semua elemen ke kanan. O(n).", "complexity"),
        ("mcq", "ArrayList capacity strategy?", None,
         json.dumps(["Tambah 1", "Double", "Triple"]), "1",
         "ArrayList double capacity saat penuh. Amortized O(1) add.", "complexity"),
        ("fill", "Rumus alamat elemen array:", "address = ______ + (index x size)", None,
         "base", "Base address = alamat elemen pertama.", "offset"),
        ("fill", "Array access time complexity:", "Array access = O(______)", None,
         "1", "O(1) constant time — satu hitung langsung sampai.", "complexity"),
    ]):
        db.session.add(M.Practice(chapter_id=ch.id, order=i, qtype=qt, question=q, code=code,
                                   options_json=opts, answer=ans, explanation=ex, category=cat))

    # ══════════════ CHEATSHEET ══════════════
    for i, (ti, co) in enumerate([
        ("Array Basics", "int[] arr = new int[5];\n- 5 elemen, index 0-4\n- Contiguous di heap\n- Fixed size setelah dibuat"),
        ("Offset Formula", "address = base + (index x size)\narr[0] = base + 0 = base\narr[3] = base + 12 (int=4B)"),
        ("Time Complexity", "Access [i]    O(1)  offset calc\nSearch         O(n)  linear scan\nInsert mid     O(n)  shift right\nDelete mid     O(n)  shift left\nResize         O(n)  copy all"),
        ("Array vs ArrayList", "Array: fixed, manual, int[]\nArrayList: dynamic, auto-resize\n\nArrayList internally = array\nDouble capacity saat penuh"),
        ("Memory Rules", "1. new int[n] = n x 4 byte di heap\n2. Variable di stack = alamat\n3. Contiguous = O(1) access\n4. Fixed = resize mahal O(n)\n5. Jangan new di loop!"),
    ]):
        db.session.add(M.Cheatsheet(chapter_id=ch.id, order=i, title=ti, content=co))

    # ══════════════ BUGS ══════════════
    for i, (ti, ds, bg, fx, w) in enumerate([
        ("Array di Loop", "Allocate array baru di setiap loop = memory leak.",
         "while (hasMore()) {\n    int[] buf = new int[100000]; // BARU TERUS!\n    process(buf);\n}",
         "int[] buf = new int[100000]; // SEKALI\nwhile (hasMore()) {\n    process(buf); // reuse\n}",
         "Setiap new = allocate di heap. Di loop = ribuan object. GC nggak sempat bersihin."),
        ("Off-by-One", "Loop sampai <= length instead of < length.",
         "int[] arr = new int[5];\nfor (int i = 0; i <= arr.length; i++) {\n    arr[i] = i; // BOOM di i=5!\n}",
         "for (int i = 0; i < arr.length; i++) {\n    arr[i] = i; // 0,1,2,3,4 OK\n}",
         "Array size 5 = index 0-4. arr[5] = ArrayIndexOutOfBoundsException. Pakai < bukan <=."),
        ("Null Array Access", "Array variable null lalu akses elemen.",
         "int[] arr = null;\narr[0] = 10; // NPE!\n// atau\nint[] arr = getArray(); // bisa return null\narr.length; // NPE!",
         "int[] arr = getArray();\nif (arr != null && arr.length > 0) {\n    arr[0] = 10; // safe\n}",
         "Array variable di stack bisa null. Akses elemen/length → NPE."),
        ("Shallow Copy Trap", "Copy array reference bukan data — ubah satu ubah dua.",
         "int[] a = {1, 2, 3};\nint[] b = a;      // copy ALAMAT!\nb[0] = 99;        // a[0] juga 99!",
         "int[] b = Arrays.copyOf(a, a.length);\n// atau\nint[] b = a.clone();\nb[0] = 99; // a[0] masih 1",
         "b = a copy alamat, bukan data. Keduanya nunjuk ke array SAMA di heap."),
    ]):
        db.session.add(M.BugExample(chapter_id=ch.id, order=i, title=ti, description=ds,
                                     buggy_code=bg, fixed_code=fx, why=w))

    # ══════════════ TRACES ══════════════
    for i, (ti, cd, steps, q, an, ex) in enumerate([
        ("Array Create", "int[] arr = new int[3];\narr[0] = 10;\narr[1] = 20;", json.dumps([
            {"l": "new int[3]", "sk": [["arr", "->100"]], "hp": [["100", "[0,0,0]"]], "ex": "Allocate 12 byte (3x4) di heap. arr pegang alamat."},
            {"l": "arr[0]=10", "sk": [["arr", "->100"]], "hp": [["100", "[10,0,0]"]], "ex": "base+0=100. Taruh 10 di situ."},
            {"l": "arr[1]=20", "sk": [["arr", "->100"]], "hp": [["100", "[10,20,0]"]], "ex": "base+4=104. Taruh 20."},
        ]), "arr[2]=?", "0", "Default value int array = 0. Belum di-assign."),
        ("Array Copy Trap", "int[] x = {1,2,3};\nint[] y = x;\ny[0] = 99;", json.dumps([
            {"l": "x={1,2,3}", "sk": [["x", "->200"]], "hp": [["200", "[1,2,3]"]], "ex": "x pegang alamat array."},
            {"l": "y=x", "sk": [["x", "->200"], ["y", "->200"]], "hp": [["200", "[1,2,3]"]], "ex": "y COPY ALAMAT. Keduanya ke array SAMA."},
            {"l": "y[0]=99", "sk": [["x", "->200"], ["y", "->200"]], "hp": [["200", "[99,2,3]"]], "ex": "Ubah via y = ubah object yang x juga nunjuk!"},
        ]), "x[0]=?", "99", "Array = reference. y dan x ke object SAMA. Ubah satu = ubah dua."),
        ("Array in Method", "void go(int[] a) {\n    a[0] = 99;\n}\nint[] x = {1,2};\ngo(x);", json.dumps([
            {"l": "x={1,2}", "sk": [["x", "->300"]], "hp": [["300", "[1,2]"]], "ex": "x pegang alamat."},
            {"l": "go(x)", "sk": [["x", "->300"], ["---", "go()"], ["a", "->300"]], "hp": [["300", "[1,2]"]], "ex": "Parameter a COPY ALAMAT x. Nunjuk ke SAMA."},
            {"l": "a[0]=99", "sk": [["x", "->300"], ["---", "go()"], ["a", "->300"]], "hp": [["300", "[99,2]"]], "ex": "a ubah array asli! Karena sama alamatnya."},
        ]), "x[0] setelah go()?", "99", "Pass array ke method = pass alamat. Method bisa ubah array asli."),
    ]):
        db.session.add(M.TraceExercise(chapter_id=ch.id, order=i, title=ti, code=cd,
                                        steps_json=steps, question=q, answer=an, explanation=ex))

    # ══════════════ INTERVIEW ══════════════
    for i, (q, a, tip) in enumerate([
        ("Jelaskan bagaimana array disimpan di memory.",
         "Array di-allocate sebagai blok CONTIGUOUS di heap. Setiap elemen bersebelahan.\n\nVariable array di stack menyimpan reference (alamat) ke blok di heap.\n\nAccess O(1) karena alamat elemen bisa dihitung langsung: base + (index x size).",
         "Gambar diagram stack-heap. Tunjukkan offset calculation. Ini bedakan kamu dari yang cuma hafal."),
        ("Kenapa array access O(1) tapi search O(n)?",
         "Access by index: JVM hitung alamat langsung pakai offset formula. Satu operasi = O(1).\n\nSearch by value: JVM nggak tahu DI MANA value itu. Harus cek satu-satu dari awal = O(n).\n\nKecuali sorted array → binary search O(log n).",
         "Hubungkan ke contiguous memory. O(1) access = konsekuensi dari memory layout, bukan keajaiban."),
        ("Kapan pakai array vs ArrayList?",
         "Array: size sudah pasti, primitif type, performance critical.\nArrayList: size dinamis, perlu convenience method (add, remove, contains).\n\nArrayList internally pakai array. Waktu penuh → double capacity → copy semua. Amortized O(1) add.",
         "Tunjukkan tahu INTERNALS ArrayList. Interviewer suka kandidat yang paham di balik layar."),
        ("Apa yang terjadi di memory saat array di-resize?",
         "1. Allocate blok baru yang lebih besar di heap\n2. Copy semua elemen dari blok lama ke baru — O(n)\n3. Update reference di stack ke blok baru\n4. Blok lama jadi garbage — GC bersihin\n\nIni kenapa resize mahal dan ArrayList pakai double strategy.",
         "Jelaskan step by step. Mention GC. Ini tunjukkan kamu paham full lifecycle."),
        ("Kenapa jangan allocate array di dalam loop?",
         "Setiap iterasi bikin object baru di heap. Loop 10000x = 10000 array di heap.\n\nGC harus bersihin semua object lama → GC pressure naik → latency spike.\n\nFix: allocate sekali di luar loop, reuse. Atau pakai object pool pattern.",
         "Ini pertanyaan real-world. Kaitkan ke production incident — memory leak, GC pause, OOM."),
    ]):
        db.session.add(M.InterviewQ(chapter_id=ch.id, order=i, question=q, answer=a, tip=tip))

    # ══════════════ FLASHCARDS ══════════════
    for i, (f, b) in enumerate([
        ("Array di memory = ?", "Contiguous (bersebelahan)"),
        ("Array access Big O?", "O(1)"),
        ("Array search Big O?", "O(n)"),
        ("Array resize Big O?", "O(n)"),
        ("Insert di tengah array?", "O(n) — geser semua ke kanan"),
        ("Kenapa index mulai 0?", "Elemen pertama offset = 0 dari base"),
        ("Offset formula?", "base + (index x size)"),
        ("int[] = berapa byte per elemen?", "4 bytes"),
        ("Array disimpan di?", "Heap (alamat di stack)"),
        ("ArrayList resize strategy?", "Double capacity"),
        ("new int[5] = berapa byte total?", "20 bytes (5 x 4)"),
        ("Default value int array?", "0"),
        ("Jangan allocate di loop karena?", "Memory leak — object baru tiap iterasi"),
        ("arr = arr2 copy apa?", "ALAMAT (bukan data)"),
        ("Deep copy array pakai?", "Arrays.copyOf() atau .clone()"),
    ]):
        db.session.add(M.Flashcard(chapter_id=ch.id, order=i, front=f, back=b))

    # ══════════════ DEEP QUIZ ══════════════
    for i, (qt, diff, q, hint, accept, perfect, expl) in enumerate([
        ("write", "basic", "int[] arr = new int[5]; — berapa TOTAL byte di heap?",
         "int = berapa byte? Kali berapa?", json.dumps(["20","20 byte"]),
         "20 bytes (5 x 4)", "int=4B. 5 elemen x 4 = 20 byte contiguous di heap."),
        ("predict", "basic", "int[] arr = new int[3];\nSystem.out.println(arr[2]);",
         "Default int = ?", json.dumps(["0"]),
         "0", "Default int array = 0. Valid index tapi belum di-assign."),
        ("predict", "medium", "int[] a = {1,2,3};\nint[] b = a;\nb = new int[]{7,8,9};\nSystem.out.println(a[0]);",
         "b = new bikin object BARU. a masih ke mana?", json.dumps(["1"]),
         "1", "b = new bikin object BARU. a masih nunjuk array lama {1,2,3}."),
        ("write", "hard", "Kenapa insert di TENGAH array O(n)?",
         "Elemen setelah posisi insert harus?", json.dumps(["geser","shift","copy","pindah"]),
         "Harus GESER semua elemen setelah posisi insert ke kanan.",
         "Array contiguous. Insert di posisi 3 array size 100 → geser 97 elemen."),
        ("debug", "master", "int[] arr = new int[5];\nfor (int i = 0; i <= 5; i++)\n    arr[i] = i * 10;\nBug?",
         "Size 5 = index berapa sampai berapa?", json.dumps(["<=","off by one","i<=5","arr[5]","outofbounds"]),
         "<= 5 harusnya < 5. arr[5] = ArrayIndexOutOfBoundsException.",
         "Off-by-one. Size 5 = index 0-4. arr[5] di luar batas."),
    ]):
        db.session.add(M.DeepQuiz(chapter_id=ch.id, order=i, qtype=qt, difficulty=diff, question=q,
                                   hint=hint, accept_json=accept, perfect=perfect, explanation=expl))

    # ══════════════ GLOSSARY ══════════════
    for k, t, tp, s, d in [
        ("array", "Array", "data_structure", "Deretan kotak bersebelahan di memory. Fixed size. Access O(1).", "Struktur data berurutan dan contiguous di heap."),
        ("contiguous", "Contiguous", "property", "Bersebelahan tanpa bolong. Kayak loker 100-104.", "Data tersimpan berurutan di memory tanpa jeda."),
        ("offset", "Offset", "calculation", "Jarak dari base address. arr[3] = loncat 3 kursi.", "Selisih: base + (index x size). Makanya O(1)."),
        ("base address", "Base Address", "pointer", "Alamat elemen pertama. Rumah. Semua offset dari sini.", "Alamat memory elemen pertama array."),
        ("o(1)", "O(1)", "complexity", "Satu langkah. Mau data 5 atau 5 juta = sama cepatnya.", "Waktu eksekusi konstan."),
        ("o(n)", "O(n)", "complexity", "Makin banyak data makin lama. 100 data = 100 langkah.", "Waktu eksekusi linear."),
        ("resize", "Resize", "operation", "Pindah meja. Array penuh → copy semua ke baru. O(n).", "Membuat array baru dan copy seluruh isi lama."),
        ("allocate", "Allocate", "action", "Pesan tempat. new int[5] = minta 20 byte di heap.", "Memesan ruang di memory."),
    ]:
        db.session.add(M.GlossaryTerm(key=k, term=t, type=tp, short=s, detail=d, chapter_id=ch.id))

    db.session.commit()
    print(f"  Ch1: {ch.title} - story + 8 modes seeded")
    return ch
