import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from tkinter import *

# Veri setini yükle (dosya bulunamadığında hata mesajı göster)
try:
    data = pd.read_csv("tiroid_veriseti.csv")
except FileNotFoundError:
    print("Hata: 'tiroid_veriseti.csv' dosyası bulunamadı. Lütfen dosyanın script ile aynı dizinde olduğundan emin olun.")
    exit()

# Özellikler (features) ve hedef değişkeni (target) ayır
X = data.drop('condition', axis=1)
y = data['condition']

# Veriyi eğitim ve test setlerine bölelim (rastgele seçilim için `random_state=42`)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Özellikleri standartlaştırma (ölçeklendirme)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# KNN modelini oluşturalım (k=3 komşu)
k = 3
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# Önceden tanımlanmış kodlar buraya gelecek...


# Tahmin fonksiyonu
# Tahmin fonksiyonu
def predict_thyroid():
    global data  # data değişkenini global olarak tanımla
    try:
        # Kullanıcıdan sayısal veri iste ve hata yakala
        age = float(age_entry.get())
        tsh = float(tsh_entry.get())
        t3 = float(t3_entry.get())
        tt4 = float(tt4_entry.get())
        t4u = float(t4u_entry.get())
        fti = float(fti_entry.get())

        # Girdi verisini düzenle ve standartlaştır
        features = [[age, tsh, t3, tt4, t4u, fti]]
        features = scaler.transform(features)

        # Tahmini yap ve sonucu göster
        result = knn.predict(features)
        if result[0]:
            result_text = "Hasta"
        else:
            result_text = "Sağlıklı"

        # Tahmin değerini güncelle
        result_label.config(text=result_text)

        # Yeni veriyi tabloya ekleme ve tahmin değeriyle güncelleme
        new_data = pd.DataFrame({'age': [age], 'TSH': [tsh], 'T3': [t3], 'TT4': [tt4], 'T4U': [t4u], 'FTI': [fti], 'condition': [result[0]]})
        data = pd.concat([data, new_data], ignore_index=True)
        data.to_csv("tiroid_veriseti.csv", index=False)

    except ValueError:
        print("Hata: Lütfen her alan için geçerli sayısal değerler girin.")

    

# Arayüz oluşturma
root = Tk()
root.title("Tiroid Hastalığı Tahmini")
root.geometry("400x400")

# Etiketler ve giriş alanları
age_label = Label(root, text="Yaş:")
age_label.pack()
age_entry = Entry(root)
age_entry.pack()

tsh_label = Label(root, text="TSH:")
tsh_label.pack()
tsh_entry = Entry(root)
tsh_entry.pack()

t3_label = Label(root, text="T3:")
t3_label.pack()
t3_entry = Entry(root)
t3_entry.pack()

tt4_label = Label(root, text="TT4:")
tt4_label.pack()
tt4_entry = Entry(root)
tt4_entry.pack()

t4u_label = Label(root, text="T4U:")
t4u_label.pack()
t4u_entry = Entry(root)
t4u_entry.pack()

fti_label = Label(root, text="FTI:")
fti_label.pack()
fti_entry = Entry(root)
fti_entry.pack()
# ... (diğer etiket ve giriş alanları)

predict_button = Button(root, text="Tahmin Et ve Kaydet", command=predict_thyroid)
predict_button.pack()

result_label = Label(root, text="")
result_label.pack()

root.mainloop()
