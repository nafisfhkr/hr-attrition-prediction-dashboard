# Belajar Penerapan Data Science: Human Resources Jaya Jaya Maju

## Business Understanding

### Business Problem

Jaya Jaya Maju menghadapi masalah employee attrition yang dapat meningkatkan biaya rekrutmen, onboarding, dan pelatihan karyawan baru. Tingginya attrition juga dapat mengganggu produktivitas dan kesinambungan pekerjaan di dalam perusahaan. Karena itu, departemen HR membutuhkan analisis berbasis data untuk mengetahui kelompok karyawan yang memiliki risiko attrition lebih tinggi dan menentukan prioritas program retention.

Dari 1.058 data karyawan yang memiliki label, 179 karyawan mengalami attrition sehingga attrition rate sebesar 16,92%. Angka tersebut menunjukkan bahwa attrition perlu dipantau secara sistematis melalui analisis dan dashboard.

### Cakupan Proyek

Proyek ini mencakup analisis data employee-level, EDA untuk menemukan faktor yang berkaitan dengan attrition, pembuatan model klasifikasi, penyimpanan pipeline model untuk prediksi data baru, serta pembuatan dataset dan dashboard Metabase untuk monitoring HR. Deployment ke lingkungan production tidak termasuk dalam scope.

### Persiapan

#### Sumber Data

Dataset yang digunakan adalah IBM HR Analytics Employee Attrition & Performance dari [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset). Salinan dataset yang digunakan berada di `data/employee_data.csv`.

#### Membuat dan Mengaktifkan Virtual Environment

Jalankan dari folder `submission`:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependency dan buka notebook:

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Data dibaca dari `data/employee_data.csv`. Target `Attrition` dipisahkan menjadi data berlabel dan data tanpa label. Sebanyak 412 baris tanpa label dipisahkan dan tidak digunakan untuk training. Data berlabel dibersihkan, target diubah menjadi integer, fitur kategorikal di-encode, dan data dibagi secara stratified menjadi data train dan test.

### Tujuan proyek

1. Mengidentifikasi kelompok karyawan dengan attrition rate tinggi.
2. Membandingkan Logistic Regression sebagai baseline dengan Random Forest Classifier.
3. Memilih model berdasarkan F1-score dan recall kelas attrition.
4. Menyediakan dataset dan rancangan dashboard untuk monitoring HR.

### Pertanyaan bisnis

- Apakah overtime berkaitan dengan attrition yang lebih tinggi?
- Job role, department, marital status, dan business travel mana yang perlu diprioritaskan?
- Bagaimana perbedaan age, monthly income, tenure, job satisfaction, environment satisfaction, dan work-life balance antara karyawan yang bertahan dan keluar?
- Bagaimana HR dapat menggunakan model dan dashboard sebagai alat monitoring retention?

## Data Understanding

Dataset utama berada di `data/employee_data.csv` dan berisi 1.470 baris serta 35 kolom. `Attrition` adalah target; 1 berarti karyawan mengalami attrition dan 0 berarti tidak. Sebanyak 412 baris tidak memiliki label, sedangkan data berlabel terdiri dari 879 kelas 0 dan 179 kelas 1.

Insight utama dari data berlabel:

- Karyawan dengan `OverTime = Yes` memiliki attrition rate 31,92%, dibandingkan 10,79% pada `No`.
- `Sales Representative` memiliki attrition rate tertinggi (43,10%), disusul `Laboratory Technician` (26,06%).
- Department `Sales` memiliki attrition rate 20,69%, lebih tinggi daripada Research & Development (15,26%) dan Human Resources (15,79%).
- Karyawan berstatus `Single` memiliki attrition rate 26,70%, lebih tinggi daripada Married (13,36%) dan Divorced (9,50%).
- `Travel_Frequently` memiliki attrition rate 24,88%, lebih tinggi daripada `Travel_Rarely` (15,68%) dan `Non-Travel` (10,28%).
- Median `MonthlyIncome` karyawan yang attrition adalah 3.388, sedangkan yang tidak attrition 5.210. Ini menunjukkan kompensasi perlu dievaluasi bersama faktor lain, bukan dianggap sebagai hubungan sebab-akibat langsung.
- Median `Age` karyawan yang attrition adalah 31 tahun, sedangkan yang tidak attrition 36 tahun.
- Median `YearsAtCompany` untuk karyawan attrition adalah 3 tahun, dibandingkan 6 tahun untuk karyawan yang bertahan.
- Rata-rata `JobSatisfaction`, `EnvironmentSatisfaction`, dan `WorkLifeBalance` pada kelompok attrition juga lebih rendah. Perbedaan paling terlihat pada `EnvironmentSatisfaction` (2,39 vs 2,78).

Notebook menyajikan tabel dan visualisasi EDA untuk memvalidasi insight tersebut.

## Data Preparation / Preprocessing

- Data dipisahkan menjadi data berlabel dan data tanpa label.
- Hanya data berlabel yang digunakan untuk modeling.
- `Attrition` diubah menjadi integer.
- `EmployeeId`, `EmployeeCount`, `Over18`, dan `StandardHours` dihapus dari fitur model karena tidak informatif atau konstan.
- Fitur kategorikal di-encode dengan `OneHotEncoder(handle_unknown="ignore")`.
- Preprocessing dan model dibungkus dalam sklearn `Pipeline`/`ColumnTransformer` agar konsisten saat prediksi.
- Data dibagi menggunakan stratified train-test split dengan `random_state=42`.

## Modeling

Notebook membandingkan dua model sederhana:

1. Logistic Regression sebagai baseline yang mudah diinterpretasikan.
2. Random Forest Classifier sebagai model pembanding yang mampu menangkap hubungan non-linear.

Keduanya menggunakan `class_weight="balanced"` agar kelas attrition yang lebih sedikit tetap diperhatikan.

## Evaluation

Notebook menampilkan accuracy, precision, recall, F1-score, classification report, dan confusion matrix. Pemilihan model mengutamakan F1-score dan recall kelas attrition karena false negative dapat membuat HR melewatkan karyawan yang berisiko keluar.

Pada hasil Run All saat ini, Random Forest terpilih dengan accuracy 0,863, precision 0,630, recall 0,472, dan F1-score 0,540 untuk kelas attrition pada data test. Angka ini merupakan benchmark dari split `random_state=42`, bukan jaminan performa pada data baru.

Model terpilih disimpan sebagai pipeline lengkap di `model/attrition_model.pkl`.

## Business Dashboard

Dashboard telah dibuat secara manual menggunakan **Metabase**.

- Dashboard Tool: Metabase
- File data dashboard: `data/dashboard_employee_data.csv`
- Email: `root@mail.com`
- Password: `root123`
- Screenshot dashboard: `nafis_fakhru-dashboard.png`
- Database Metabase: `metabase.db.mv.db`

Visualisasi yang perlu dibuat:

- KPI total employee
- KPI attrition count
- KPI attrition rate
- Attrition rate by OverTime
- Attrition rate by JobRole
- Attrition rate by Department
- Attrition rate by MaritalStatus
- Attrition rate by BusinessTravel
- Distribusi MonthlyIncome berdasarkan Attrition
- Distribusi Age berdasarkan Attrition

`AttritionLabel` pada dataset dashboard berisi label yang mudah dibaca: `Tidak Attrition` atau `Attrition`. Dataset dashboard diimpor ke MySQL lokal dan digunakan sebagai sumber data Metabase. File `metabase.db.mv.db` menyimpan konfigurasi Metabase, pertanyaan, dan dashboard yang telah dibuat.

### Cara Menjalankan Dashboard Metabase

Gunakan Metabase versi `v0.46.4` dan jalankan perintah berikut dari folder submission:

```powershell
docker pull metabase/metabase:v0.46.4
docker create --name metabase -p 3000:3000 metabase/metabase:v0.46.4
docker cp .\metabase.db.mv.db metabase:/metabase.db.mv.db
docker start metabase
```

Setelah container selesai startup, akses dashboard melalui [http://localhost:3000](http://localhost:3000). Jika container `metabase` sudah pernah dibuat, gunakan `docker start metabase` tanpa menjalankan `docker create` lagi.

## Conclusion

Analisis menunjukkan bahwa employee attrition di Jaya Jaya Maju berkaitan dengan beberapa kelompok dan kondisi kerja tertentu. Attrition rate pada data berlabel adalah 16,92%, dengan kelompok `OverTime = Yes`, `Sales Representative`, `Laboratory Technician`, `Single`, dan `Travel_Frequently` menunjukkan rate yang relatif lebih tinggi.

Random Forest terpilih sebagai model terbaik pada eksperimen ini berdasarkan F1-score dan recall kelas attrition. Model dapat digunakan sebagai alat bantu untuk menentukan prioritas monitoring, bukan sebagai satu-satunya dasar pengambilan keputusan HR.

Dashboard Metabase melengkapi hasil modeling dengan menyediakan monitoring KPI, attrition rate berdasarkan kelompok karyawan, serta distribusi usia dan pendapatan.

## Rekomendasi Action Items

1. Evaluasi beban kerja, penjadwalan, dan kebijakan overtime, terutama pada kelompok `OverTime = Yes`.
2. Prioritaskan retention program untuk `Sales Representative` dan `Laboratory Technician`.
3. Lakukan monitoring khusus untuk karyawan yang sering melakukan business travel dan kelompok dengan masa kerja awal.
4. Evaluasi kompensasi, job satisfaction, environment satisfaction, dan work-life balance melalui pulse survey atau stay interview.
5. Gunakan dashboard untuk monitoring attrition rate secara berkala dan menilai efektivitas intervensi HR.
6. Gunakan probabilitas model sebagai sinyal prioritas, bukan keputusan otomatis terhadap karyawan.

## Cara Menjalankan

### Notebook

Install dependency, lalu buka dan jalankan `notebook.ipynb` dari cell pertama sampai terakhir:

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Notebook akan membuat atau memperbarui:

- `model/attrition_model.pkl`
- `data/dashboard_employee_data.csv`
- `data/sample_employee.csv`

### Prediction script

Gunakan file CSV dengan kolom employee seperti dataset asli, tanpa perlu menyertakan `Attrition`:

```bash
python prediction.py --input data/sample_employee.csv
```

Untuk menyimpan hasil prediksi ke CSV:

```bash
python prediction.py --input data/sample_employee.csv --output data/prediction_result.csv
```

Output berisi `Prediction` (`0` = Tidak Attrition, `1` = Attrition), `PredictionLabel`, dan `AttritionProbability` jika model mendukung probabilitas.

## Struktur Folder

```text
submission/
├── data/
│   ├── employee_data.csv
│   ├── dashboard_employee_data.csv
│   └── sample_employee.csv
├── model/
│   └── attrition_model.pkl
├── notebook.ipynb
├── prediction.py
├── README.md
├── requirements.txt
├── metabase.db.mv.db
└── nafis_fakhru-dashboard.png
```
