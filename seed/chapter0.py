"""Chapter 0: Memory 101 — Variables, Types & Memory Model (all 8 modes)"""
import json

def seed(db, models):
    M = models
    ch = M.Chapter(slug="memory-101", title="Memory 101",
        subtitle="Variables, Types & Memory Model", topic="Variable & Memory",
        description="Fondasi sebelum mulai: variable, tipe data, stack vs heap, primitif vs reference.",
        order=0, is_published=True)
    db.session.add(ch); db.session.flush()

    # STORY
    story = [("orientation", "00_orientation.md", 0, False, None, [
        ("narrator", "// NexaPay HQ — Orientation day. Lantai 3.", None, None),
        ("riku", "Sebelum sentuh production, kalian harus paham: semua terjadi di MEMORY.", None, None),
        ("riku", "Variable itu KOTAK BERLABEL di memory.", None, None),
        ("narrator", "  int umur = 28;\n  1. JVM siapin 4 byte di stack\n  2. Label \"umur\"\n  3. Isi 28", "o", None),
        ("riku", "TIPE (ukuran), NAMA (label), NILAI (isi).", None, None),
        ("narrator", "  byte=1B short=2B int=4B long=8B\n  float=4B double=8B boolean=1B char=2B", "o", None),
        ("riku", "Ada DUA jenis: primitif dan reference.", None, None),
        ("narrator", "  int umur = 28;          langsung di stack\n  String nama = \"Taufik\"; stack=ALAMAT heap=data\n\n  Stack:              Heap:\n  [umur = 28]        [\"Taufik\"]\n  [nama = 0xA2] ---->", "o", None),
        ("sora", "Ini kenapa == untuk String nggak work. == cek ALAMAT bukan isi.", None, None),
        ("riku", "Bukan hafalan — kalian paham memory model.", None, None),
    ])]
    for slug, fn, order, ict, cg, lines in story:
        sc = M.Scene(chapter_id=ch.id, slug=slug, filename=fn, order=order, is_choice_target=ict, choice_group=cg)
        db.session.add(sc); db.session.flush()
        for i, (char, text, style, choice) in enumerate(lines):
            db.session.add(M.Line(scene_id=sc.id, char=char, text=text, style=style, order=i, choice_options=choice))

    # DEEP DIVE
    for i, (ti, co, cd, ky) in enumerate([
        ("L1 Variable", "Variable = kotak berlabel. TIPE, NAMA, NILAI.\nDeclare = bikin kotak. Assign = isi.",
         "int umur;      // declare\numur = 28;     // assign\nint umur = 28; // shortcut", "Variable = kotak berlabel."),
        ("L2 Tipe Data", "JVM perlu tahu byte. int=4B, double=8B paling sering.",
         "int i = 100;     // 4B\ndouble d = 3.14; // 8B\nboolean b = true; // 1B", "int(4B) double(8B) paling sering."),
        ("L3 Stack", "Variable lokal di STACK. Auto-bersih saat method selesai. LIFO.",
         "void f() {\n    int a = 10; // masuk stack\n} // hilang", "Stack = meja kerja auto-rapi."),
        ("L4 Heap", "Object, String, array di HEAP. Stack pegang ALAMAT.",
         "int x = 28;           // stack\nString s = \"hi\";      // stack:alamat heap:data", "Stack=alamat. Heap=data."),
        ("L5 Connect", "Paham memory = paham bug.\n== String cek alamat. NPE = alamat kosong.",
         "String a = \"hi\";\nString b = a; // copy ALAMAT bukan data", "Paham memory = paham bug."),
    ]):
        db.session.add(M.DeepDive(chapter_id=ch.id, order=i, title=ti, content=co, code=cd, keypoint=ky))

    # PRACTICE (MCQ only for simplicity, 8 questions)
    for i, (q, o, a, ex, cat) in enumerate([
        ("int x=42; berapa byte?", ["1","2","4","8"], "2", "int=4 bytes.", "t"),
        ("String data di mana?", ["Stack","Heap","Disk"], "1", "String=reference. Data di heap.", "m"),
        ("Kenapa Java butuh tipe?", ["Ribet","JVM perlu byte","Konvensi"], "1", "JVM harus tahu ukuran.", "t"),
        ("== pada new String cek?", ["Isi","Alamat","Tipe"], "1", "== reference=cek alamat.", "r"),
        ("Method selesai stack?", ["Tetap","Auto-bersih","Error"], "1", "Stack auto-clean.", "m"),
        ("boolean = ? byte", ["1","2","4"], "0", "boolean=1 byte.", "t"),
        ("null artinya?", ["Angka 0","Alamat kosong","String kosong"], "1", "null=alamat kosong.", "r"),
        ("Heap dibersihkan oleh?", ["Programmer","GC","OS"], "1", "Garbage Collection.", "m"),
    ]):
        db.session.add(M.Practice(chapter_id=ch.id, order=i, qtype="mcq", question=q,
            options_json=json.dumps(o), answer=a, explanation=ex, category=cat))

    # CHEATSHEET
    for i, (ti, co) in enumerate([
        ("Primitif", "byte=1B short=2B int=4B long=8B\nfloat=4B double=8B boolean=1B char=2B"),
        ("Variable", "TIPE NAMA = NILAI;\nint  umur = 28;"),
        ("Stack vs Heap", "STACK: lokal, auto-clean\nHEAP: objects, GC"),
        ("== vs equals", "Primitif: == cek NILAI\nRef: == cek ALAMAT\n.equals() cek ISI"),
    ]):
        db.session.add(M.Cheatsheet(chapter_id=ch.id, order=i, title=ti, content=co))

    # BUGS
    for i, (ti, ds, bg, fx, w) in enumerate([
        ("NPE", "null lalu akses method.", "String s = null;\ns.length(); // NPE!",
         "if (s != null) s.length();", "null=alamat kosong."),
        ("== vs equals", "== String cek alamat.", "new String(\"hi\") == new String(\"hi\") // false!",
         "a.equals(b) // true!", "Dua new=dua alamat."),
        ("Overflow", "int max lewat.", "int x = 2147483647;\nx = x + 1; // negatif!",
         "long x = 2147483647L;", "int 4B. Lewat max = flip."),
        ("Uninitialized", "Local tanpa assign.", "int x; println(x); // Error!",
         "int x = 0; println(x);", "Local nggak auto-init."),
    ]):
        db.session.add(M.BugExample(chapter_id=ch.id, order=i, title=ti, description=ds,
                                     buggy_code=bg, fixed_code=fx, why=w))

    # TRACES
    for i, (ti, cd, steps, q, an, ex) in enumerate([
        ("Primitif Copy", "int a=5; int b=a; a=10;", json.dumps([
            {"l":"a=5","sk":[["a","5"]],"hp":[],"ex":"Kotak a, isi 5."},
            {"l":"b=a","sk":[["a","5"],["b","5"]],"hp":[],"ex":"Copy NILAI."},
            {"l":"a=10","sk":[["a","10"],["b","5"]],"hp":[],"ex":"b nggak berubah."},
        ]), "b=?", "5", "Primitif copy nilai."),
        ("Reference", "String a=\"hello\"; String b=a; a=\"world\";", json.dumps([
            {"l":"a=hello","sk":[["a","->100"]],"hp":[["100","hello"]],"ex":"a pegang alamat."},
            {"l":"b=a","sk":[["a","->100"],["b","->100"]],"hp":[["100","hello"]],"ex":"Copy ALAMAT."},
            {"l":"a=world","sk":[["a","->200"],["b","->100"]],"hp":[["100","hello"],["200","world"]],"ex":"a nunjuk baru. b masih lama."},
        ]), "b=?", "hello", "String immutable. b masih lama."),
    ]):
        db.session.add(M.TraceExercise(chapter_id=ch.id, order=i, title=ti, code=cd,
                                        steps_json=steps, question=q, answer=an, explanation=ex))

    # INTERVIEW
    for i, (q, a, tip) in enumerate([
        ("Stack vs heap?", "Stack: lokal, kecil, auto-clean. Heap: objects, GC.", "Contoh: pass object=pass alamat."),
        ("== vs .equals()?", "==primitif:nilai. ==ref:alamat. .equals():isi.", "String interning."),
        ("NullPointerException?", "null=alamat kosong. Fix: null check.", "Tunjukkan paham root cause."),
    ]):
        db.session.add(M.InterviewQ(chapter_id=ch.id, order=i, question=q, answer=a, tip=tip))

    # FLASHCARDS
    for i, (f, b) in enumerate([
        ("int=?B", "4"), ("long=?B", "8"), ("boolean=?B", "1"),
        ("Primitif di?", "Stack"), ("Reference data di?", "Heap"),
        ("== ref cek?", "Alamat"), (".equals() cek?", "Isi"),
        ("null=?", "Alamat kosong"), ("Method done stack?", "Auto-bersih"),
        ("Heap oleh?", "GC"), ("int max?", "~2.1 milyar"),
    ]):
        db.session.add(M.Flashcard(chapter_id=ch.id, order=i, front=f, back=b))

    # DEEP QUIZ
    for i, (qt, diff, q, hint, accept, perfect, expl) in enumerate([
        ("write", "basic", "Tulis rumus untuk menghitung alamat elemen array di memory.",
         "Tiga komponen: titik awal, posisi, ukuran.", json.dumps(["base+index*size","base+(index*size)","base+(i*size)"]),
         "address = base + (index x size)", "Base=alamat pertama. Index=posisi. Size=ukuran per elemen."),
        ("predict", "basic", "int a = 5; int b = a; a = 99;\nSystem.out.println(b);",
         "int = primitif. Copy = copy apa?", json.dumps(["5"]),
         "5", "Primitif copy NILAI. b punya kotak sendiri."),
        ("predict", "medium", "int[] x = {10,20,30};\nint[] y = x;\ny[1] = 99;\nSystem.out.println(x[1]);",
         "Array = reference. y = x copy apa?", json.dumps(["99"]),
         "99", "Array=reference. Copy ALAMAT. Keduanya ke object SAMA."),
        ("write", "medium", "String a = null; a.length();\nApa nama error dan KENAPA?",
         "null nunjuk ke mana?", json.dumps(["nullpointerexception","npe","null pointer"]),
         "NullPointerException — a nunjuk alamat KOSONG.", "null=alamat kosong. .length() akses object yang nggak ada."),
        ("draw", "medium", "int x = 42; String s = \"hello\";\nGambar memory: STACK: [?] HEAP: [?]",
         "int langsung stack. String = alamat stack, data heap.", json.dumps(["stack:x=42","x=42,s=","x=42 s="]),
         "STACK: [x=42, s=alamat] HEAP: [\"hello\"]", "Primitif langsung stack. Reference: alamat stack, data heap."),
        ("predict", "hard", "String a = \"hello\"; String b = a;\na = null;\nSystem.out.println(b);",
         "a = null hapus apa?", json.dumps(["hello"]),
         "hello", "a=null hapus alamat a. Object \"hello\" masih ada karena b masih pegang reference."),
        ("write", "hard", "Kenapa == untuk String sering return false? Jelaskan dari sisi memory.",
         "== pada reference cek apa?", json.dumps(["alamat","address","cek alamat"]),
         "== cek ALAMAT di stack, bukan ISI di heap. Dua object beda = alamat beda = false.",
         "Dua new String = dua object = dua alamat. Pakai .equals() untuk cek isi."),
        ("explain", "master", "void process() punya int x dan String s. Method selesai.\nApa terjadi di STACK dan HEAP?",
         "Stack dan heap cleanup berbeda.", json.dumps(["stack hilang","stack bersih","heap gc","heap tetap"]),
         "STACK: x dan s hilang (auto-clean). HEAP: object String tetap sampai GC.",
         "Stack auto-clean saat return. Heap: GC handle, hanya kalau zero reference."),
        ("debug", "master", "String[] names = new String[3];\nnames[0] = \"A\";\nSystem.out.println(names[1].length());\nBug apa?",
         "Default String array = apa?", json.dumps(["null","npe","names[1] null"]),
         "NPE. names[1] default null. .length() pada null = crash.",
         "Reference array default = null per elemen. Gabungan: array defaults + null + reference."),
    ]):
        db.session.add(M.DeepQuiz(chapter_id=ch.id, order=i, qtype=qt, difficulty=diff, question=q,
                                   hint=hint, accept_json=accept, perfect=perfect, explanation=expl))

    # GLOSSARY
    for k, t, tp, s in [
        ("variable", "Variable", "concept", "Kotak berlabel. int umur=28."),
        ("tipe data", "Tipe Data", "concept", "Ukuran kotak. int=4B."),
        ("primitif", "Primitif", "category", "int,long,double,boolean. Di stack."),
        ("reference", "Reference", "category", "Isinya ALAMAT. Di heap."),
        ("stack", "Stack", "region", "Meja kerja. Auto-clean."),
        ("heap", "Heap", "region", "Gudang. GC clean."),
        ("null", "null", "value", "Alamat kosong. NPE."),
        ("byte", "Byte", "unit", "Satuan. int=4B."),
        ("garbage collection", "GC", "process", "Cleaning service."),
    ]:
        db.session.add(M.GlossaryTerm(key=k, term=t, type=tp, short=s, chapter_id=ch.id))

    db.session.commit()
    print(f"  Ch0: {ch.title} — story + 8 modes seeded")
    return ch
