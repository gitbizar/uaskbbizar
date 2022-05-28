#Nama   : Abizar Fadhil
#NIM    : 191011401800
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : Rumah Makan

#Banyaknya Porsi : min 500 prs dan max 1200 prs.
#Banyaknya Makanan  : sedikit 40 dan banyak 80.
#Tingkat Piring Kotor  : rendah 40, sedang 50, dan 60 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Makanan():
    minimum = 40
    maximum = 80

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Piring_Kotor():
    minimum = 40
    medium = 50
    maximum = 60

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Porsi():
    minimum = 500
    maximum = 1200
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_makanan, jumlah_piring_kotor):
        mak = Makanan()
        pktr = Piring_Kotor()
        result = []
        
        # [R1] Jika Makanan SEDIKIT, dan Piring Kotor RENDAH, 
        #     MAKA Porsi = 500
        α1 = min(mak.sedikit(jumlah_makanan), pktr.rendah(jumlah_piring_kotor))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Makanan SEDIKIT, dan Piring Kotor SEDANG, 
        #     MAKA Porsi = 10 * jumlah_piring_kotor + 100
        α2 = min(mak.sedikit(jumlah_makanan), pktr.sedang(jumlah_piring_kotor))
        z2 = 10 * jumlah_piring_kotor + 100
        result.append((α2, z2))

        # [R3] Jika Makanan SEDIKIT, dan Piring Kotor TINGGI, 
        #     MAKA Porsi = 10 * jumlah_piring_kotor + 200
        α3 = min(mak.sedikit(jumlah_makanan), pktr.tinggi(jumlah_piring_kotor))
        z3 = 10 * jumlah_piring_kotor + 200
        result.append((α3, z3))

        # [R4] Jika Makanan BANYAK, dan Piring Kotor RENDAH,
        #     MAKA Porsi = 5 * jumlah_makanan + 2 * jumlah_piring_kotor
        α4 = min(mak.banyak(jumlah_makanan), pktr.rendah(jumlah_piring_kotor))
        z4 = 5 * jumlah_makanan + 2 * jumlah_piring_kotor
        result.append((α4, z4))

        # [R5] Jika Makanan BANYAK, dan Piring Kotor SEDANG,
        #     MAKA Porsi = 5 * jumlah_makanan + 4 * jumlah_piring_kotor + 100
        α5 = min(mak.banyak(jumlah_makanan), pktr.sedang(jumlah_piring_kotor))
        z5 = 5 * jumlah_makanan + 4 * jumlah_piring_kotor + 100
        result.append((α5, z5))

        # [R6] Jika Makanan BANYAK, dan Piring Kotor TINGGI,
        #     MAKA Porsi = 5 * jumlah_makanan + 5 * jumlah_piring_kotor + 300
        α6 = min(mak.banyak(jumlah_makanan), pktr.tinggi(jumlah_piring_kotor))
        z6 = 5 * jumlah_makanan + 5 * jumlah_piring_kotor + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_makanan, jumlah_piring_kotor):
        inferensi_values = self.inferensi(jumlah_makanan, jumlah_piring_kotor)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])