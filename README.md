# 说明
这个是NDL古籍OCRV3的改版，用于并行部署。
2024年10月5日 15:43:01建立






**原有readme文本翻译如下**

# NDL古籍OCR应用程序（ver.3）
该存储库提供了用于执行文本化的应用程序，使用NDL古籍OCR将古典籍图像转化为文本数据。

NDL古籍OCR是一种OCR技术，可从江户时期之前的日本古书、清代以前的汉籍等古籍资料的数字化图像中生成文本数据。

该程序是基于日本国立国会图书馆[令和3年度OCR相关项目](https://lab.ndl.go.jp/data_set/ocr/)所得的知识、[NDL实验室](https://lab.ndl.go.jp)的研究活动、以及人文信息学领域构建的各种数据资源独立开发的。

自2023年8月发布的[ver.2](https://github.com/ndl-lab/ndlkotenocr_cli/tree/ver.2)版本起，汉籍资料的版面识别性能得到了提升。

**在处理汉籍资料的文本化时，据报告ver.2的版面识别性能可能低于ver.1。因此，推荐在处理汉籍资料时升级至ver.3版本。**

参考文献：[永崎研宣, 等. 基于OCR高精度化的数字学术编辑版新发展. 人文计算学会议2023论文集, 2023, 2023: 177-182.（外部链接）](http://id.nii.ac.jp/1001/00231250/)

阅读顺序整序功能的性能改善参考了[令和4年度OCR相关项目](https://lab.ndl.go.jp/data_set/r4ocr/r4_software/)中获得的知识。

有关用于开发和改进该程序的数据集和方法的详细信息，请参阅[古籍资料的OCR文本化实验](https://lab.ndl.go.jp/data_set/r4ocr/r4_koten/)以及[OCR学习用数据集（一起翻刻）](https://github.com/ndl-lab/ndl-minhon-ocrdataset)。

该程序由日本国立国会图书馆以CC BY 4.0许可证公开，详情请参阅
[LICENSE](./LICENSE)。

**如果您希望继续使用截至2023年8月发布的版本，请使用[ver.1](https://github.com/ndl-lab/ndlkotenocr_cli/tree/ver.1)。**
**如果您希望继续使用截至2024年2月发布的版本，请使用[ver.2](https://github.com/ndl-lab/ndlkotenocr_cli/tree/ver.2)。**
```
git clone https://github.com/ndl-lab/ndlkotenocr_cli -b ver.1
```
```
git clone https://github.com/ndl-lab/ndlkotenocr_cli -b ver.2
```
通过更改源码获取部分的命令，如上所示，即可继续使用这些版本。

## 环境构建

### 1. 克隆存储库
请执行以下命令：
```
git clone https://github.com/ndl-lab/ndlkotenocr_cli
```

### 2. 更新主机的NVIDIA驱动
容器中将使用CUDA 11.8。

如果您的主机NVIDIA驱动版本未满足以下要求：

Linux：450.36.06以上

Windows：520.06以上

请更新与您的GPU匹配的驱动版本。

（参考信息）

我们在以下主机环境（AWS g5.xlarge实例）上进行了操作确认：

操作系统：Ubuntu 18.04.6 LTS

GPU：NVIDIA A10G

NVIDIA驱动：470.182.03


### 3. 安装docker
请根据https://docs.docker.com/engine/install/中的指引，按照您的操作系统及发行版安装docker。

### 4. 构建docker容器
Linux:
```
cd ndlkotenocr_cli
sh ./docker/dockerbuild.sh
```

Windows:
```
cd ndlkotenocr_cli
docker\dockerbuild.bat
```

### 5. 启动docker容器
Linux:
```
cd ndlkotenocr_cli
sh ./docker/run_docker.sh
```

Windows:
```
cd ndlkotenocr_cli
docker\run_docker.bat
```

### 环境构建后的目录结构（参考）
```
ndlocr_cli
├── main.py : 主Python脚本
├── cli : 用于CLI命令操作的Python脚本目录
├── src : 各推理处理的源码目录
│   ├── ndl_kotenseki_layout : 版面提取处理的源码目录
|   ├── reading_order：阅读顺序整序处理的源码目录
│   └── text_kotenseki_recognition : 字符识别处理的源码目录
├── config.yml : 推理设置的示例配置文件
├── docker : Docker环境构建脚本目录
├── README.md : 本文件
└── requirements.txt : 必要的Python包列表
```


## 教程
启动后，可以使用如下`docker exec`命令登录到容器中：

```
docker exec -i -t --user root kotenocr_cli_runner bash
```

### 执行推理处理
假设input_root目录下存在img目录，并在该目录下存有资料的图像文件夹（bookid1, bookid2,...），
```
input_root/
  └── img
      ├── page01.jpg
      ├── page02.jpg
      ・・・
      └── page10.jpg
```
可以使用以下命令执行推理：
```
python main.py infer input_root output_dir
```

执行后的输出示例如下：

```
output_dir/
  ├── input_root
  │   ├── txt
  │   │     ├── page01.txt
  │   │     ├── page02.txt
  │   │    ・・・
  │   │    
  │   └── json
  │         ├── page01.json
  │         ├── page02.json
  │        ・・・
  └── opt.json
```

各模块使用的设置值如权重文件路径等，可以通过修改`config.yml`中的内容来更改。

### 关于选项

#### 输入格式选项
执行时指定
`-s b`，可以处理以下输入格式的文件夹结构。

示例：
```
python main.py infer input_root output_dir -s b
```

输入格式
```
input_root/
  └── img
      ├── bookid1
      │   ├── page01.jpg
      │   ├── page02.jpg
      │   ・・・
      │   └── page10.jpg
      ├── bookid2
          ├── page01.jpg
          ├── page02.jpg
          ・・・
          └── page10.jpg
```
输出格式
```
output_dir/
  ├── input_root
  |     ├──bookid1
  │     |     ├── txt
  │     |     │     ├── page01.txt
  │     |     │     ├── page02.txt
  │     |     │         ・・・
  │     |     │    
  │     |     └── json
  │     |           ├── page01.json
  │     |           ├── page02.json
  │     |               ・・・
  |     ├──bookid2
  │     |     ├── txt
  │     |     │     ├── page01.txt
  │     |     │     ├── page02.txt
  │     |     │         ・・・
  │     |     │    
  │     |     └── json
  │     |           ├── page01.json
  │     |           ├── page02.json
  │                    ・・・
  └── opt.json
```

#### 输出图像尺寸信息选项
执行时指定
`-a`，将会在输出的json中添加图像尺寸信息。

示例：
```
python main.py infer input_root output_dir -a
```

**注意**
启用此选项后，输出的json格式将如下所示：
```
{
  "contents":[
    （各字符串矩形的坐标、识别的字符串等）
  ],
  "imginfo": {
    "img_width": （原图像的宽度）,
    "img_height": （原图像的高度）,
    "img_path":（原图像的目录路径）,
    "img_name":（原图像名称）
  }
}
```



#### 选项信息的保存
在输出目录中，执行时指定的选项信息将保存在`opt.json`中。


## 关于模型的再训练
截至2024年2月，我们公开了版面识别模型及字符串识别模型的再训练步骤。

关于版面识别模型，请参阅[train-layout.ipynb](/src/ndl_kotenseki_layout/train-layout.ipynb)以及[cococonverter-NDLDocL.ipynb](/src/ndl_kotenseki_layout/cococonverter-NDLDocL.ipynb)。

关于字符串识别模型，请参阅[train.py](/src/text_kotenseki_recognition/train.py)。
