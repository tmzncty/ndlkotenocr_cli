# Copyright (c) 2022, National Diet Library, Japan
#
# This software is released under the CC BY 4.0.
# https://creativecommons.org/licenses/by/4.0/


import copy
import numpy

from .base_proc import BaseInferenceProcess


class ReadingReorderProcess(BaseInferenceProcess):
    """
    レイアウト抽出推論を実行するプロセスのクラス。
    BaseInferenceProcessを継承しています。
    """
    def __init__(self, cfg, pid):
        """
        Parameters
        ----------
        cfg : dict
            本実行処理における設定情報です。
        pid : int
            実行される順序を表す数値。
        """
        super().__init__(cfg, pid, '_reorder')
        from src.kotenseki_reading_order.tools.process import InferencerWithCLI
        self._inferencer = InferencerWithCLI(self.cfg['kotenseki_reading_order'])
        self._run_src_inference = self._inferencer.inference_wich_cli

    def is_valid_input(self, input_data):
        """
        本クラスの推論処理における入力データのバリデーション。

        Parameters
        ----------
        input_data : dict
            推論処理を実行する対象の入力データ。

        Returns
        -------
        [変数なし] : bool
            　入力データが正しければTrue, そうでなければFalseを返します。
        """
        if type(input_data['json']) is not List:
            print('LayoutExtractionProcess: input json is not List')
            return False
        return True

    def _run_process(self, input_data):
        """
        推論処理の本体部分。

        Parameters
        ----------
        input_data : dict
            推論処理を実行する対象の入力データ。

        Returns
        -------
        result : dict
            推論処理の結果を保持する辞書型データ。
            基本的にinput_dataと同じ構造です。
        """
        print('### Layout Extraction Process ###')
        output_data = copy.deepcopy(input_data)
        inference_output = self._run_src_inference(input_data['json'])

        # Create result to pass json
        result = []
        """output_data['xml'] = inference_output['xml']
        if inference_output['dump_img'] is not None:
            output_data['dump_img'] = inference_output['dump_img']"""
        output_data['json'] = inference_output['json']
        output_data['text'] = inference_output['text']
        result.append(output_data)
        return result
