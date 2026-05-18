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
| File | Chức năng |
|---|---|
| `ui.py` | Chạy giao diện đồ họa Tkinter, vẽ bàn cờ và xử lý click chuột |
| `main.py` | File chạy chương trình chính |
| `game_logic.py` | Xử lý luật chơi, bàn cờ, kiểm tra thắng/thua/hòa và sinh nước đi |
| `evaluation.py` | Hàm đánh giá trạng thái bàn cờ |
| `ai_algorithms.py` | Cài đặt Minimax, Alpha-Beta và bộ nhớ học kinh nghiệm |
| `benchmark.py` | Chạy thực nghiệm so sánh Minimax và Alpha-Beta |
| `recent_finished_games.json` | File tự sinh để lưu dữ liệu học kinh nghiệm của AI |
| `requirements.txt` | File yêu cầu thư viện |
| `README.md` | Hướng dẫn chạy chương trình |
## 3. Yêu cầu cài đặt

Chương trình được viết bằng ngôn ngữ Python và sử dụng thư viện giao diện đồ họa Tkinter. Đây là thư viện có sẵn khi cài Python trên Windows, nên thông thường không cần cài thêm thư viện ngoài.

## Phiên bản Python khuyến nghị

Nên sử dụng Python phiên bản 3.10 trở lên.

Các phiên bản có thể chạy tốt:

```test
Python 3.10
Python 3.11
Python 3.12
## 4. Cach chay game 

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

## 5. Cach chay thuc nghiem

Mo Command Prompt tai thu muc `source_code`, chay:

```bash
python benchmark.py
```

Chuong trinh se chay Minimax va Alpha-Beta tren 5 trang thai kiem thu, voi cac do sau 1, 2, 3, 4. Ket qua duoc ghi vao:

```text
results.csv
```

## 6. Ghi chu ve hoc kinh nghiem

File `ai/learning.py` cai dat co che hoc don gian. Sau moi tran, cac nuoc di cua AI duoc cong diem neu AI thang, tru diem neu AI thua va cong diem nhe neu hoa. Du lieu hoc duoc luu vao `learning_data.json` va duoc cong them vao diem danh gia o cac van sau.

Day khong phai neural network hay deep learning. Thuat toan chinh cua bai van la Minimax va Alpha-Beta pruning theo yeu cau de bai.

## 7. Thong tin nop bai

Ten repository nen dat theo mau:

```text
23021325_23021361_23021345_CaroAI
```

Can co cac thanh phan:

```text
source_code/
requirements.txt
README.md
Bao_cao_CaroAI.docx
Bao_cao_CaroAI.pdf
```
