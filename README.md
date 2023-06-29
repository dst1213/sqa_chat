
### change log

- 2023年6月14日
```angular2html
    1. 升级gpt-3.5-turbo-16k模型，是3*16k的英文，但是效果不稳定
```

### 安装

- cp .env.template .env
- 填入openai的key【必填】和代理api地址【可选】
- pip install -r requirements.txt

### 使用：windows
- py_envs/sqa_chat/scripts/activate.bat
- python main.py

### 使用：linux
- source ~/.virtualenvs/sqa_chat/bin/activate
- python main.py

### 升级1
- pypi.org查找langchain和langchainplus-sdk，拿到最新版的whl地址
```shell
langchainplus-sdk==0.0.10
pip install https://files.pythonhosted.org/packages/11/4b/acdad55d824af550f38ae1379f5cd3c703d0076265ef2d9a41bb1d100069/langchainplus_sdk-0.0.10-py3-none-any.whl

langchain==0.0.200
pip install https://files.pythonhosted.org/packages/a8/2d/32ac18b8a9e0905d2cf7f64e9c5e58b9e03f5c0461d7ca7eac97e58cc9bb/langchain-0.0.200-py3-none-any.whl
```
### 升级2

```shell
pip install https://files.pythonhosted.org/packages/32/92/b4ce0f5c576233ccfdadce90031b64b9a12be5ed3ce9d555b28af34845bf/langchainplus_sdk-0.0.17-py3-none-any.whl

pip install https://files.pythonhosted.org/packages/dc/86/5a2caf55a324cfb7363561947ac17b701d6750802441daed94c9bb6882b1/langchain-0.0.218-py3-none-any.whl
```

### 翻译工具
```angular2html
    百度翻译-200种语言互译、沟通全世界！
    https://fanyi.baidu.com/?aldtype=16047#auto/zh
```


### 需求
- 医生字段信息(1)
https://www.kdocs.cn/l/crUA7eMgelFB