import numpy as np

class FuzzyController:
    def __init__(self):
        # 初期化時には特に設定は不要です。
        pass

    def compute_u(self, current_quality, current_size, setpoint_quality, setpoint_compression):
        # 品質の調整
        quality_adjustment = self.compute_quality_adjustment(current_quality, setpoint_quality)
        new_quality = np.clip(current_quality + quality_adjustment, 1, 100)

        # シャープネスの調整
        new_sharpen = self.compute_sharpen(current_size, setpoint_compression)

        # ノイズの調整
        new_noise = self.compute_noise(current_size, setpoint_compression)

        return new_quality, new_sharpen, new_noise

    def compute_quality_adjustment(self, current_quality, setpoint_quality):
        # 品質のセットポイントと現在の品質の差に基づいて調整値を計算
        quality_diff = setpoint_quality - current_quality
        if quality_diff > 0.1:
            return 10  # 品質を上げる
        elif quality_diff < -0.1:
            return -10  # 品質を下げる
        else:
            return 0  # 変更なし

    def compute_sharpen(self, current_size, setpoint_compression):
        # シャープネスの調整
        size_diff = setpoint_compression - current_size
        if size_diff > 1000:
            return 5  # シャープネスを上げる
        elif size_diff < -1000:
            return 0  # シャープネスを下げる
        else:
            return 3  # 中間の値

    def compute_noise(self, current_size, setpoint_compression):
        # ノイズの調整
        size_diff = setpoint_compression - current_size
        if size_diff > 1000:
            return 5  # ノイズを上げる
        elif size_diff < -1000:
            return 0  # ノイズを下げる
        else:
            return 3  # 中間の値
