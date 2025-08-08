# import numpy as np
# import skfuzzy as fuzz

# class FuzzySleepQuality:
#     def __init__(self):
#         # Range nilai detak jantung (bpm)
#         self.heart_rate = np.arange(30, 121, 1)

#         # Membership functions untuk masing-masing fuzzy set
#         self.poor = fuzz.trimf(self.heart_rate, [30, 30, 50])
#         self.fair = fuzz.trimf(self.heart_rate, [45, 55, 65])
#         self.good = fuzz.trimf(self.heart_rate, [60, 70, 80])
#         self.very_good = fuzz.trimf(self.heart_rate, [75, 85, 95])
#         self.excellent = fuzz.trimf(self.heart_rate, [90, 120, 120])

#         # Kualitas tidur sebagai output
#         self.sleep_quality = np.arange(0, 101, 1)
#         self.output_poor = fuzz.trimf(self.sleep_quality, [0, 0, 25])
#         self.output_fair = fuzz.trimf(self.sleep_quality, [20, 35, 50])
#         self.output_good = fuzz.trimf(self.sleep_quality, [45, 60, 75])
#         self.output_very_good = fuzz.trimf(self.sleep_quality, [70, 80, 90])
#         self.output_excellent = fuzz.trimf(self.sleep_quality, [85, 100, 100])

#     def infer(self, bpm: float) -> dict:
#         # Fuzzification
#         bpm_level_poor = fuzz.interp_membership(self.heart_rate, self.poor, bpm)
#         bpm_level_fair = fuzz.interp_membership(self.heart_rate, self.fair, bpm)
#         bpm_level_good = fuzz.interp_membership(self.heart_rate, self.good, bpm)
#         bpm_level_very_good = fuzz.interp_membership(self.heart_rate, self.very_good, bpm)
#         bpm_level_excellent = fuzz.interp_membership(self.heart_rate, self.excellent, bpm)

#         # Rule base:
#         # if bpm in low range => poor sleep
#         # mid range => fair/good
#         # optimal => excellent

#         # Apply rules (Inferences)
#         rule_poor = bpm_level_poor
#         rule_fair = bpm_level_fair
#         rule_good = bpm_level_good
#         rule_very_good = bpm_level_very_good
#         rule_excellent = bpm_level_excellent

#         # Implication
#         quality_activation_poor = np.fmin(rule_poor, self.output_poor)
#         quality_activation_fair = np.fmin(rule_fair, self.output_fair)
#         quality_activation_good = np.fmin(rule_good, self.output_good)
#         quality_activation_very_good = np.fmin(rule_very_good, self.output_very_good)
#         quality_activation_excellent = np.fmin(rule_excellent, self.output_excellent)

#         # Aggregation
#         aggregated = np.fmax(quality_activation_poor,
#                      np.fmax(quality_activation_fair,
#                      np.fmax(quality_activation_good,
#                      np.fmax(quality_activation_very_good,
#                              quality_activation_excellent))))

#         # Defuzzification
#         defuzzified = fuzz.defuzz(self.sleep_quality, aggregated, 'centroid')

#         # Klasifikasi kualitas tidur
#         if defuzzified <= 25:
#             label = "Poor"
#         elif defuzzified <= 50:
#             label = "Fair"
#         elif defuzzified <= 70:
#             label = "Good"
#         elif defuzzified <= 85:
#             label = "Very Good"
#         else:
#             label = "Excellent"

#         return {
#             "bpm": bpm,
#             "score": round(defuzzified, 2),
#             "label": label
#         }



import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyKualitasTidur:
    def __init__(self):
        # === 1. Definisi Variabel ===
        self.detak_jantung = ctrl.Antecedent(np.arange(40, 121, 1), 'detak_jantung')
        self.kualitas_tidur = ctrl.Consequent(np.arange(0, 101, 1), 'kualitas_tidur')

        # === 2. Membership Function ===
        self._define_membership_functions()

        # === 3. Rule Base ===
        self.rules = self._define_rules()

        # === 4. Build Control System ===
        self.kualitas_ctrl = ctrl.ControlSystem(self.rules)
        self.simulasi = ctrl.ControlSystemSimulation(self.kualitas_ctrl)

    def _define_membership_functions(self):
        # Input: Detak Jantung
        self.detak_jantung['sangat_rendah'] = fuzz.trimf(self.detak_jantung.universe, [40, 43, 48])
        self.detak_jantung['rendah'] = fuzz.trimf(self.detak_jantung.universe, [44, 50, 60])
        self.detak_jantung['normal'] = fuzz.trimf(self.detak_jantung.universe, [58, 65, 80])
        self.detak_jantung['tinggi'] = fuzz.trimf(self.detak_jantung.universe, [77, 88, 100])
        self.detak_jantung['sangat_tinggi'] = fuzz.trimf(self.detak_jantung.universe, [98, 112, 120])

        # Output: Kualitas Tidur
        self.kualitas_tidur['buruk'] = fuzz.trimf(self.kualitas_tidur.universe, [0, 15, 30])
        self.kualitas_tidur['cukup_buruk'] = fuzz.trimf(self.kualitas_tidur.universe, [20, 35, 50])
        self.kualitas_tidur['cukup'] = fuzz.trimf(self.kualitas_tidur.universe, [40, 50, 60])
        self.kualitas_tidur['cukup_baik'] = fuzz.trimf(self.kualitas_tidur.universe, [55, 67, 80])
        self.kualitas_tidur['baik'] = fuzz.trimf(self.kualitas_tidur.universe, [75, 87, 100])

    def _define_rules(self):
        return [
            ctrl.Rule(self.detak_jantung['sangat_rendah'], self.kualitas_tidur['baik']),
            ctrl.Rule(self.detak_jantung['rendah'], self.kualitas_tidur['cukup_baik']),
            ctrl.Rule(self.detak_jantung['normal'], self.kualitas_tidur['cukup']),
            ctrl.Rule(self.detak_jantung['tinggi'], self.kualitas_tidur['cukup_buruk']),
            ctrl.Rule(self.detak_jantung['sangat_tinggi'], self.kualitas_tidur['buruk']),
        ]

    def analisis(self, bpm):
        self.simulasi.input['detak_jantung'] = bpm
        self.simulasi.compute()
        nilai_kualitas = self.simulasi.output['kualitas_tidur']

        # Kategorisasi hasil defuzzifikasi
        if nilai_kualitas < 35:
            kategori = 'Buruk'
        elif nilai_kualitas < 50:
            kategori = 'Cukup Buruk'
        elif nilai_kualitas < 65:
            kategori = 'Cukup'
        elif nilai_kualitas < 80:
            kategori = 'Cukup Baik'
        else:
            kategori = 'Baik'

        return {
            'nilai_kualitas_tidur': round(nilai_kualitas, 2),
            'kategori_kualitas_tidur': kategori
        }
