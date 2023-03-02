# 配置环境

> python最好使用使用虚拟化环境，这样不受本机python的其他环境影响，

环境要求：

```shell
python版本为：3.10+
# 在脚本中下面执行指令即可
pip install -r requirements.txt

# 同步本地的依赖包到requirement.txt文件中
cd {project_path} # 为项目的根路径
pip freeze > requirements.txt
```

## grpc的环境配置说明：

> 官网链接为:[点我](https://grpc.io/docs/languages/python/quickstart/)  
> 相关文档链接为:https://www.jianshu.com/p/43fdfeb105ff

```shell
# grpc 相关的 python 模块(module) 
pip install grpcio
# 安装 python 下的 protoc 编译器
pip install grpcio-tools

# 编译 proto 文件
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto

python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
--python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
--grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
-I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录
```



