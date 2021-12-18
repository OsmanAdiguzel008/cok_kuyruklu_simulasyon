import numpy as np
import random
import datetime as dt


def rassal_sayi_uret(n=10, degisken=False, gelisler_arasi_sure=10):
    liste = []
    for i in range(n):
        sayi = random.random()
        if degisken == True:
            sayi = (-gelisler_arasi_sure) * np.log(sayi)
        liste.append(sayi)
    return liste

def aralik_hesapla(olasiliklar):        
    birikimli = np.cumsum(olasiliklar).tolist()
    birikimli.insert(0,0)
    
    aralik = []
    for i in range(len(olasiliklar)):
        aralik.append([birikimli[i],birikimli[i+1]])
    return aralik

def tercih_uret(rassal, olasiliklar, tercih_secenekleri):
    if (len(olasiliklar) != len(tercih_secenekleri)) | (sum(olasiliklar) != 1):
        raise Exception("Lutfen olasilik toplamlarini ve tercih seceneklerini kontrol ediniz")

    aralik = aralik_hesapla(olasiliklar)
    tercih_listesi = []
    for i in rassal:
        for j in aralik:
            if (i >= j[0]) and (i<j[1]):
                tercih_e = aralik.index(j)
                tercih = tercih_secenekleri[tercih_e]
                tercih_listesi.append(tercih)
    return tercih_listesi

def hizmet_suresi_uret(rassal, tercihler, hizmet, hizmet_suresi, hs_olasilik):
    aralik = aralik_hesapla(hs_olasilik)
        
    servis_sureleri = []
    for i in range(len(tercihler)):
        tercih = tercihler[i]
        hizmet_e = hizmet.index(tercih)
        hs = hizmet_suresi[hizmet_e]
        
        rs = rassal[i]    
        
        for j in aralik:
            if (rs >= j[0]) and (rs < j[1]):
                aralik_e = aralik.index(j)
                servis_suresi = hs[aralik_e]
                servis_sureleri.append(servis_suresi)
    return servis_sureleri
                
def dakika_ekle(saat, ekleme):
    return saat + dt.timedelta(minutes=ekleme)   

def hizmete_basla(musteri_gelisi, hizmet_bitis):
    if hizmet_bitis < musteri_gelisi:
        return musteri_gelisi
    else:
        return hizmet_bitis
    
def isletme_beklemeyi_uret(hizmet_bitis, musteri_gelisi):
    if hizmet_bitis >= musteri_gelisi:
        isletme_bekleme = dt.timedelta(0)
    else:
        isletme_bekleme = musteri_gelisi - hizmet_bitis
    return isletme_bekleme

if __name__ == "__main__":
    
    acilis = dt.datetime.strptime("9:00","%H:%M")
    musteri_sayisi = 20
    ort_m_g = 10            # musterilerin ortalama gelis suresi dakika
    
    hizmet = ["ic","dis","icdis"]
    tercih_olasiliklari = [0.2,0.2,0.6]
    hizmet_suresi_aralik = [[5,10],[7,15],[13,25]]
    hs_olasilik   = [0.3,0.7]
    
    beklenilen_sureler = []
    sistemde_gecen_sureler = []
    isletme_bos_suresi = []
    
    
    gelis_suresi = rassal_sayi_uret(n=musteri_sayisi, degisken=True, gelisler_arasi_sure = ort_m_g)
    print(gelis_suresi,"\n","_"*100,"\n")
    
    tercih_rs = rassal_sayi_uret(n=musteri_sayisi, degisken=False)
    tercihler = tercih_uret(rassal = tercih_rs, 
                            olasiliklar = tercih_olasiliklari, 
                            tercih_secenekleri = hizmet)
    print(tercihler,"\n","_"*100,"\n")
    
    servis_rs = rassal_sayi_uret(n=musteri_sayisi, degisken=False)
    
    hizmet_sureleri = hizmet_suresi_uret(rassal = servis_rs, 
                                         tercihler = tercihler, 
                                         hizmet = hizmet, 
                                         hizmet_suresi = hizmet_suresi_aralik, 
                                         hs_olasilik = hs_olasilik)
    print(hizmet_sureleri,"\n","_"*100,"\n")
    
    musteri = list(range(len(gelis_suresi)))
    
    musteri_gelisi = acilis
    bekleme_suresi = 0
    hizmet_bitis = acilis
    for i in musteri:
        print("-"*50,"\n")
        print(f"{i+1}. Musteri")
        
        musteri_gelisi = dakika_ekle(musteri_gelisi, ekleme=gelis_suresi[i])
        print(musteri_gelisi.time().isoformat(timespec='minutes'), "musteri geldi")
        
        isletme_bos_bekleme = isletme_beklemeyi_uret(hizmet_bitis, musteri_gelisi)
        
        hizmet_baslama = hizmete_basla(musteri_gelisi, hizmet_bitis)
        print(hizmet_baslama.time().isoformat(timespec='minutes'), "hizmete baslandi")
        
        hizmet_suresi = hizmet_sureleri[i]
        print("Hizmet suresi",hizmet_suresi,"dakika")
        
        hizmet_bitis = dakika_ekle(hizmet_baslama, ekleme=hizmet_suresi)
        print(hizmet_bitis.time().isoformat(timespec='minutes'), "hizmet bitti")
        
        musteri_bekleme = hizmet_baslama - musteri_gelisi
        print("Bekleme suresi", (dt.datetime.min + musteri_bekleme).time().isoformat(timespec='minutes'))
        
        sistemde_bekleme = hizmet_bitis - musteri_gelisi
        print("Sistemde gecen sure",(dt.datetime.min + sistemde_bekleme).time().isoformat(timespec='minutes'))
        
        beklenilen_sureler.append(musteri_bekleme)
        sistemde_gecen_sureler.append(sistemde_bekleme)
        isletme_bos_suresi.append(isletme_bos_bekleme)
        
    print("-"*50)
    print("_"*50,"\n")
    cum1 = dt.datetime.min
    for i in beklenilen_sureler:
      cum1 = cum1 + i      
    toplam = (cum1-dt.datetime.min).total_seconds()/len(beklenilen_sureler)
    saat,dakika = int(toplam / 3600), toplam % 3600
    dakika,saniye = int(dakika/60), int(dakika%60)
    print(f"Ortalama bekleme suresi '{saat}:{dakika}:{saniye}'")
    
    cum2 = dt.datetime.min
    for i in sistemde_gecen_sureler:
      cum2 = cum2 + i      
    toplam = (cum2-dt.datetime.min).total_seconds()/len(beklenilen_sureler)
    saat,dakika = int(toplam/3600), toplam%3600
    dakika,saniye = int(dakika/60), int(dakika%60)
    print(f"Ortalama sistemde gecen sure '{saat}:{dakika}:{saniye}'")
    
    
    cum3 = dt.datetime.min
    for i in isletme_bos_suresi:
      cum3 = cum3 + i      
    toplam = (cum3-dt.datetime.min).total_seconds()/len(beklenilen_sureler)
    saat,dakika = int(toplam/3600), toplam%3600
    dakika,saniye = int(dakika/60), int(dakika%60)
    print(f"Ortalama isletme bos bekleme suresi '{saat}:{dakika}:{saniye}'")
    
    print("_"*50)
    print("_"*50,"\n")
    print(acilis.time().isoformat(timespec='minutes'), "hizmet saati basladi")
    print(f"Gun icerisinde toplamda {musteri_sayisi} tane musteriye bakildi")
    print(hizmet_bitis.time().isoformat(timespec='minutes'), "butun musterilere hizmet verildi")
    
    print("_"*50)
    print("_"*50)
    