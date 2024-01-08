import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyController:
    def __init__(self):
        # ファジー変数の定義
        self.quality = ctrl.Antecedent(np.arange(0, 101, 1), 'quality')
        self.quality_diff = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'quality_diff')
        self.size_diff = ctrl.Antecedent(np.arange(-2000, 2001, 1), 'size_diff')
        self.adjustment = ctrl.Consequent(np.arange(-20, 21, 1), 'adjustment')
        self.sharpen = ctrl.Consequent(np.arange(0, 6, 1), 'sharpen')
        self.noise = ctrl.Consequent(np.arange(0, 6, 1), 'noise')

        # メンバーシップ関数の定義
        self.quality['low'] = fuzz.trimf(self.quality.universe, [0, 0, 50])
        self.quality['medium'] = fuzz.trimf(self.quality.universe, [25, 50, 75])
        self.quality['high'] = fuzz.trimf(self.quality.universe, [50, 100, 100])
        self.quality_diff['negative'] = fuzz.trimf(self.quality_diff.universe, [-1, -0.5, 0])
        self.quality_diff['zero'] = fuzz.trimf(self.quality_diff.universe, [-0.1, 0, 0.1])
        self.quality_diff['positive'] = fuzz.trimf(self.quality_diff.universe, [0, 0.5, 1])
        self.size_diff['negative'] = fuzz.trimf(self.size_diff.universe, [-2000, -1000, 0])
        self.size_diff['zero'] = fuzz.trimf(self.size_diff.universe, [-500, 0, 500])
        self.size_diff['positive'] = fuzz.trimf(self.size_diff.universe, [0, 1000, 2000])
        self.adjustment['decrease'] = fuzz.trimf(self.adjustment.universe, [-20, -10, 0])
        self.adjustment['none'] = fuzz.trimf(self.adjustment.universe, [-5, 0, 5])
        self.adjustment['increase'] = fuzz.trimf(self.adjustment.universe, [0, 10, 20])
        self.sharpen['low'] = fuzz.trimf(self.sharpen.universe, [0, 0, 3])
        self.sharpen['high'] = fuzz.trimf(self.sharpen.universe, [2, 5, 5])
        self.noise['low'] = fuzz.trimf(self.noise.universe, [0, 0, 3])
        self.noise['high'] = fuzz.trimf(self.noise.universe, [2, 5, 5])

        # ファジー規則の定義
        rule1 = ctrl.Rule(self.quality['low'] & self.quality_diff['negative'], self.adjustment['increase'])
        rule2 = ctrl.Rule(self.quality['high'] & self.quality_diff['positive'], self.adjustment['decrease'])
        rule3 = ctrl.Rule(self.quality_diff['zero'], self.adjustment['none'])
        rule4 = ctrl.Rule(self.size_diff['positive'], self.sharpen['high'])
        rule5 = ctrl.Rule(self.size_diff['negative'], self.sharpen['low'])
        rule6 = ctrl.Rule(self.size_diff['positive'], self.noise['high'])
        rule7 = ctrl.Rule(self.size_diff['negative'], self.noise['low'])
        rule8 = ctrl.Rule(self.quality['low'] | self.quality_diff['negative'] | self.size_diff['negative'], self.adjustment['increase'])
        rule9 = ctrl.Rule(self.quality['high'] | self.quality_diff['positive'] | self.size_diff['positive'], self.adjustment['decrease'])
        rule10 = ctrl.Rule(self.quality_diff['zero'] | self.size_diff['zero'], self.adjustment['none'])
        rule11 = ctrl.Rule(self.size_diff['positive'], self.sharpen['high'])
        rule12 = ctrl.Rule(self.size_diff['negative'], self.sharpen['low'])
        rule13 = ctrl.Rule(self.size_diff['positive'], self.noise['high'])
        rule14 = ctrl.Rule(self.size_diff['negative'], self.noise['low'])
        rule_default = ctrl.Rule(~self.quality['low'] & ~self.quality['medium'] & ~self.quality['high'] &
                         ~self.quality_diff['negative'] & ~self.quality_diff['zero'] & ~self.quality_diff['positive'] &
                         ~self.size_diff['negative'] & ~self.size_diff['zero'] & ~self.size_diff['positive'],
                         [self.adjustment['none'], self.sharpen['low'], self.noise['low']])

        self.control_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule_default])
        self.control_system_sim = ctrl.ControlSystemSimulation(self.control_system)

    def compute_u(self, current_quality, current_size, setpoint_quality, setpoint_compression):
        # 入力値の範囲の検証と調整
        quality_diff = np.clip(setpoint_quality - current_quality, -1, 1)
        size_diff = np.clip(setpoint_compression - current_size, -2000, 2000)

        # ファジー制御の入力設定
        self.control_system_sim.input['quality'] = np.clip(current_quality, 0, 100)
        self.control_system_sim.input['quality_diff'] = quality_diff
        self.control_system_sim.input['size_diff'] = size_diff

        # ファジー制御の実行
        self.control_system_sim.compute()

        # 出力値の取得
        new_quality = np.clip(current_quality + self.control_system_sim.output['adjustment'], 0, 100)
        new_sharpen = self.control_system_sim.output['sharpen']
        new_noise = self.control_system_sim.output['noise']

        return new_quality, new_sharpen, new_noise
