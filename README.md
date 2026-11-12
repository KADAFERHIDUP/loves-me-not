# Loves me, loves me not

Game pixel art kecil yang dibuat dengan Python dan pygame. Cabut kelopak bunga satu per satu sambil bergantian "loves me" dan "loves me not". Kelopak terakhir yang menentukan hasilnya.

**Main langsung di browser (HP atau laptop):** https://kadaferhidup.github.io/loves-me-not/

![Demo](demo/demo.gif)

## Fitur

- Grafis pixel art 180×240 yang diperbesar tajam (pixel-perfect) sesuai ukuran jendela
- Langit malam dengan gradasi dither, bintang berkelip, bulan, bukit, dan rumput yang bergoyang
- Kelopak yang dicabut jatuh berputar dengan gravitasi dan hambatan udara
- Jumlah kelopak diacak tiap putaran (9–15), jadi hasil akhirnya juga acak
- Versi web punya lagu latar chiptune original, efek suara tiap kelopak dicabut, dan jingle penutup (ikon speaker di pojok kiri atas atau tombol M untuk mematikan suara)

## Cara menjalankan (versi Python)

```bash
pip install -r requirements.txt
python loves_me_not.py
```

## Kontrol

| Tombol | Fungsi |
| --- | --- |
| Klik kiri / Spasi | Cabut satu kelopak |
| R | Ulang dengan bunga baru |
| Esc | Keluar |

Di versi web: ketuk layar untuk mencabut kelopak, ketuk lagi setelah selesai untuk mengulang, dan ketuk ikon speaker untuk mematikan atau menyalakan suara. Musik mulai setelah sentuhan pertama.

## Tampilan

| Awal | Akhir |
| --- | --- |
| ![Awal](demo/awal.png) | ![Akhir](demo/akhir.png) |

Video lengkap dengan suara: [demo/demo.mp4](demo/demo.mp4)

---

Dibuat oleh Ahmad Umraithi
