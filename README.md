# CaroAI - Minimax va Alpha-Beta

## 1. Gioi thieu
Day la chuong trinh game Caro 9x9 cho mon Tri tue nhan tao. Nguoi choi danh quan `X`, may tinh danh quan `O`. Ben nao co 4 quan lien tiep theo hang ngang, doc hoac cheo se thang. Chuong trinh khong xet luat chan hai dau.

AI duoc cai dat bang:
- Minimax co gioi han do sau
- Alpha-Beta pruning
- Ham danh gia trang thai
- Sap xep nuoc di va chi sinh nuoc di gan cac quan da danh
- Co che hoc kinh nghiem don gian sau moi van

## 2. Cau truc thu muc

```text
source_code/
├── main.py                  # Chay giao dien game
├── benchmark.py             # Chay thuc nghiem Minimax va Alpha-Beta
├── config.py                # Cau hinh chung
├── ai/
│   ├── agent.py             # Dieu phoi AI, chon thuat toan
│   ├── minimax.py           # Thuat toan Minimax
│   ├── alpha_beta.py        # Thuat toan Alpha-Beta pruning
│   ├── evaluator.py         # Ham danh gia trang thai
│   └── learning.py          # Bo nho hoc kinh nghiem sau tran
├── game/
│   ├── board.py             # Bieu dien ban co, luat choi, kiem tra thang/thua/hoa
│   ├── move_generator.py    # Sinh nuoc di hop le va sap xep nuoc di
│   └── test_states.py       # 5 trang thai kiem thu
├── ui/
│   ├── app.py               # Khoi tao ung dung Tkinter
│   ├── start_screen.py      # Man hinh bat dau
│   ├── game_screen.py       # Man hinh choi game
│   └── end_screen.py        # Thong bao ket thuc
└── utils/
    └── logger.py            # Ghi ket qua CSV
```

## 3. Cach chay game

Mo Command Prompt tai thu muc `source_code`, sau do chay:

```bash
python main.py
```

Neu Windows khong nhan lenh `python`, thu:

```bash
py main.py
```

Tren giao dien, nguoi choi co the:
- Nhap ten nguoi choi
- Bam truc tiep vao o tren ban co de danh
- Chon thuat toan `Minimax` hoac `Alpha-Beta`
- Chon do sau tim kiem tu 1 den 4
- Bat/tat bo nho hoc
- Di lai, choi lai, tam dung, xoa bo nho hoc

## 4. Cach chay thuc nghiem

Mo Command Prompt tai thu muc `source_code`, chay:

```bash
python benchmark.py
```

Chuong trinh se chay Minimax va Alpha-Beta tren 5 trang thai kiem thu, voi cac do sau 1, 2, 3, 4. Ket qua duoc ghi vao:

```text
results.csv
```

## 5. Ghi chu ve hoc kinh nghiem

File `ai/learning.py` cai dat co che hoc don gian. Sau moi tran, cac nuoc di cua AI duoc cong diem neu AI thang, tru diem neu AI thua va cong diem nhe neu hoa. Du lieu hoc duoc luu vao `learning_data.json` va duoc cong them vao diem danh gia o cac van sau.

Day khong phai neural network hay deep learning. Thuat toan chinh cua bai van la Minimax va Alpha-Beta pruning theo yeu cau de bai.

## 6. Thong tin nop bai

Ten repository nen dat theo mau:

```text
mssv1_mssv2_mssv3_CaroAI
```

Can co cac thanh phan:

```text
source_code/
requirements.txt
README.md
Bao_cao_CaroAI.docx
Bao_cao_CaroAI.pdf
```
