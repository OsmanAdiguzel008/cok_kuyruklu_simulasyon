import numpy as np
import random
import datetime as dt
import matplotlib.pyplot as plt


def rassal_sayi_uret(n=10, degisken=False, gelisler_arasi_sure=10):
    liste = []
    for i in range(n):
        sayi = random.random()
        if degisken == True:
            #buradaki formulden kaynakli n buyudukce cok buyuk sayilar cikabiliyor.
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

def kuyruk(kacinci_musteri, musteri_gelisi, gelis_suresi, hizmet_bitis, kuyruk_d):
    print("-"*50,"\n")
    print(f"{i+1}. Musteri")
    
    res = [k for k, v in kuyruk_d.items() if v==min(kuyruk_d.values())]
    n_kuyruk = min(res)
    
    musteri_gelisi = dakika_ekle(musteri_gelisi, ekleme=gelis_suresi[i])
    print(musteri_gelisi.time().isoformat(timespec='minutes'), "musteri geldi")
    
    isletme_bos_bekleme = isletme_beklemeyi_uret(kuyruk_d[n_kuyruk], musteri_gelisi)
    
    print(f"Musteri {n_kuyruk}. kuyruga girmistir")
    hizmet_baslama = hizmete_basla(musteri_gelisi, kuyruk_d[n_kuyruk])
    print(hizmet_baslama.time().isoformat(timespec='minutes'), "hizmete baslandi")
    
    hizmet_suresi = hizmet_sureleri[i]
    print("Hizmet suresi",hizmet_suresi,"dakika")
    
    hizmet_bitis = dakika_ekle(hizmet_baslama, ekleme=hizmet_suresi)
    kuyruk_d[n_kuyruk] = hizmet_bitis
    print(hizmet_bitis.time().isoformat(timespec='minutes'), "hizmet bitti")
    
    musteri_bekleme = hizmet_baslama - musteri_gelisi
    print("Bekleme suresi", (dt.datetime.min + musteri_bekleme).time().isoformat(timespec='minutes'))
    
    sistemde_bekleme = hizmet_bitis - musteri_gelisi
    print("Sistemde gecen sure",(dt.datetime.min + sistemde_bekleme).time().isoformat(timespec='minutes'))
    print("Isletmenin bos beklemesi",(dt.datetime.min + isletme_bos_bekleme).time().isoformat(timespec='minutes'))
    return musteri_bekleme,sistemde_bekleme,isletme_bos_bekleme, musteri_gelisi, hizmet_bitis

def ortalama_sure(liste, yazi):
    cum = dt.datetime.min
    for i in liste:
        cum = cum + i      
    toplam = (cum-dt.datetime.min).total_seconds()/len(liste)
    saat,dakika = int(toplam/3600), toplam%3600
    dakika,saniye = int(dakika/60), int(dakika%60)
    print(f"{yazi} '{saat}:{dakika}:{saniye}'")
    return toplam/60
    
if __name__ == "__main__":
    '''
    
    Ortalama bekleme suresi '0:10:14'
    Ortalama sistemde gecen sure '0:28:20'
    Ortalama isletme bos bekleme suresi '0:2:25'
    -------------------------------------------------- 
     __________________________________________________ 
    
    09:00 hizmet saati basladi
    Gun icerisinde toplamda 20 tane musteriye bakildi
    12:34 butun musterilere hizmet verildi
    __________________________________________________ 
     __________________________________________________
     '''
    similasyon_calisma_sayisi = 15
    acilis = dt.datetime.strptime("9:00","%H:%M")
    musteri_sayisi = 20
    kuyruk_sayisi = 3       # servis sayisini belirtir
    ort_m_g = 10            # musterilerin ortalama gelis suresi
    
    hizmet = ["ic","dis","icdis"]
    tercih_olasiliklari = [0.2,0.2,0.6]
    hizmet_suresi_aralik = [[5,10],[7,15],[13,25]]
    hs_olasilik   = [0.3,0.7]
    
    ort_bs_liste = []    # ortalama musterinin bekleme sureleri
    ort_ss_liste = []    # ortalama sistemde bekleme suresleri
    ort_is_liste = []    # ortalama isletme bos bekleme sureleri
    
    for i in range(similasyon_calisma_sayisi):
        beklenilen_sureler = []
        sistemde_gecen_sureler = []
        isletme_bos_suresi = []
        
        gelis_suresi = rassal_sayi_uret(musteri_sayisi, degisken=True, 
                                        gelisler_arasi_sure=10)
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
        hizmet_bitis = acilis
        
        kuyruk_d = {} 
        for i in range(kuyruk_sayisi):
            kuyruk_d[i+1] = hizmet_bitis
            
        for i in musteri:
            
            mb,sb,ib,mg, hb = kuyruk(kacinci_musteri = i, 
                              musteri_gelisi = musteri_gelisi, 
                              gelis_suresi = gelis_suresi, 
                              hizmet_bitis = hizmet_bitis,
                              kuyruk_d = kuyruk_d)
            
            musteri_gelisi, hizmet_bitis = mg, hb
            beklenilen_sureler.append(mb)
            sistemde_gecen_sureler.append(sb)
            isletme_bos_suresi.append(ib)
            
            
        
        print("-"*50,"\n","_"*50,"\n")
        ort_bs = ortalama_sure(liste=beklenilen_sureler, yazi="Ortalama bekleme suresi")
        ort_ss = ortalama_sure(liste=sistemde_gecen_sureler, yazi="Ortalama sistemde gecen sure")
        ort_is = ortalama_sure(liste=isletme_bos_suresi, yazi="Ortalama isletme bos bekleme suresi")
        
        
        print("-"*50,"\n","_"*50,"\n")
        print(acilis.time().isoformat(timespec='minutes'), "hizmet saati basladi")
        print(f"Gun icerisinde toplamda {musteri_sayisi} tane musteriye bakildi")
        print(hizmet_bitis.time().isoformat(timespec='minutes'), "butun musterilere hizmet verildi")
        print("_"*50,"\n","_"*50)
    
        ort_bs_liste.append(ort_bs)
        ort_ss_liste.append(ort_ss)
        ort_is_liste.append(ort_is)
        
        
    
    
    plt.plot(list(range(1,len(ort_bs_liste)+1)), ort_bs_liste)
    plt.ylabel("ortalama musteri bekleme (dk)")
    plt.xlabel("similasyon sayisi")
    plt.show()
    
    plt.plot(list(range(1,len(ort_ss_liste)+1)), ort_ss_liste)
    plt.ylabel("ortalama sistemde bekleme (dk)")
    plt.xlabel("similasyon sayisi")
    plt.show()
    
    plt.plot(list(range(1,len(ort_is_liste)+1)), ort_is_liste)
    plt.ylabel("ortalama isletme bos bekleme (dk)")
    plt.xlabel("similasyon sayisi")
    plt.show()