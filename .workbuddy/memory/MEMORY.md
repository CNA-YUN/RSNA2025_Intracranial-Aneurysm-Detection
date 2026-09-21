# Project Memory — RSNA2025 Intracranial-Aneurysm-Detection (bravecowcow 2nd-place)

## 项目性质
- RSNA 2025 颅内动脉瘤检测竞赛第二名方案；两阶段：Stage1 2D 血管 ROI 提取 + Stage2 3D 多任务(分割+分类)。
- 训练框架为 `nnXNet/`（nnU-Net v2 扩展 fork），位于 `nnXNet/nnxnet/`。
- 推理 notebook（`bravecowcow-2nd-place-inference-*.ipynb`）默认依赖 Kaggle 环境的**自定义 nnunetv2 fork**（带 `_0913`、`_no_seg_return_no_filter` 等自定义模块），这些模块**不在本仓库**。

## Windows + 纯 CPU 运行要点（已核实）
- 推理可行，训练不可行（Stage2 batch=2 需 ~53GB 显存）。
- 推荐路线：用仓库自带 `nnxnet` 包做推理（已含 `predict_from_multi_axial_slices`、two-seg-with-cls、`only_forward_cls`），不要用 notebook 里的 `nnunetv2` 导入。
- 必须修改：
  1. requirements：移除 nvidia-* / cupy-cuda12x / cucim-cu12 / triton；torch/torchvision/torchaudio 换 CPU 版。
  2. 设环境变量 `nnXNet_raw` / `nnXNet_preprocessed` / `nnXNet_results` 为本地绝对路径（推理只需 results）。
  3. device 改 `cpu`，删除 `USE_NUM_GPUS=2`/`gpu_id=1`。
  4. 去掉半精度：notebook `img_cropped_tensor.half()` → `.float()`；nnXNet 推理器内部 `dtype=torch.half` 缓冲（2D_orthogonal 行251-252、two_seg 行592）改 `torch.float32`。
  5. 删 `kaggle_evaluation.rsna_inference_server`，改为本地遍历 DICOM 文件夹 + 写 CSV。
  6. `MODEL_PATHS` 改本地路径；从 Kaggle Models 下载 Stage1/Stage2/plane_2d_cls 权重。
- 性能：纯 CPU 跑 224³ + 8×TTA 很慢，建议减 TTA、仅用 fold_0。

## 关键文件
- Stage1 推理器: `nnXNet/nnxnet/inference/predict_from_raw_data_2D_orthogonal_planes_fast.py`
- Stage2 推理器: `nnXNet/nnxnet/inference/predict_from_raw_data_two_seg_with_cls_no_seg_return_no_filter.py`
- 多任务训练器: `nnXNet/nnxnet/training/nnXNetTrainer/nnXNetTrainer_ResEncoderUNet_two_seg.py`
- 自定义损失: `nnXNet/nnxnet/training/loss/awdice_loss.py` (AneurysmWeightedDiceLoss)
