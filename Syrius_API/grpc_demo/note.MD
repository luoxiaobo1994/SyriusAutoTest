# GRPC学习笔记

## 1.必要环境

### [官方文档](http://doc.oschina.net/grpc?t=60138)

### 第三方库：

``` python
pip install grpcio
pip install grpcio-tools
```

## 2.快速上手

### 2.1 创建一个proto文件，编写接口。

文件名称：Demo.proto，文件格式如下：

```protobuf
// 说明proto的版本。
syntax = "proto3";


// 包名
package test;


service DemoTest {// 关键字 + 服务名称 空格 大括号
    // 请求和请求对象可以不同名。 returns 后面直接括号说明返回。
    rpc DemoReq (OneRequest) returns (OneResponse) {}  // 定义请求和返回
    // 可以定义多个请求和返回
    rpc Second (SecondReq) returns (SecondResponse) {}
}

// 定义请求实体。
message OneRequest {
    //    请求的参数，类型是string，参数名是name，序号是1. 最后要加上分号。
    string name = 1;
    //    proto里int分32和64等，都没关系，到Python里面，都是int。
    int64 age = 2;
}
message OneResponse {
    //    就返回一个result
    string result = 1;
}
```

### 2.2 通过工具，将刚才编写的probo文件，生成Python脚本。

命令行终端，到当前路径下，输入以下命令，可将.proto生成.py文件。

```
python -m grpc_tools.protoc -I --python_out=. --grpc_python_out=. Demo.proto
```

输入完成后，会得到两个.py文件，分别是：
Demo_pb2.py # proto文件的名称+pb2
Demo_pb2_grpc.py # proto文件的名称+pb2_grpc
这两个文件的内容无需修改变动。

### 2.3 自行编写service和client脚本。

service.py

```python
import grpc  # 必要导包
import Demo_pb2 as pb2  # 导入pb2
import Demo_pb2_grpc as pb2_grpc  # 导入pb2_grpc
from concurrent import futures  # 用于多线程


class DemoTest(pb2_grpc.DemoTestServicer):  # 类名要是和proto里的一致。参数则是pb2_grpc.类名+Servicer。

    def DemoReq(self, request, context):  # 两个固定参数。函数名对应rpc后面的请求名称
        name = request.name  # 直接调用proto里定义的参数
        age = request.age
        result = f"My name is {name}, I'm {age} years old!"  # 只是一个常规Python变量。无特殊含义
        return pb2.OneResponse(result=result)  # 返回对应rpc的返回实体。


def run():  # 必要的运行函数
    grpc_server = grpc.server(  # 服务实例
        futures.ThreadPoolExecutor(max_workers=4)  # 最大工作线程数量。
    )
    pb2_grpc.add_DemoTestServicer_to_server(DemoTest(), grpc_server)  # 将服务添加到grpc服务中。
    host = '127.0.0.1:5000'  # 启动的host
    grpc_server.add_insecure_port(f'{host}')
    grpc_server.start()  # 启动
    grpc_server.wait_for_termination()  # 让服务持续运行，而不是脚本跑完就挂。
```

client.py

```python
import grpc
import Demo_pb2 as pb2
import Demo_pb2_grpc as pb2_grpc


def run():
    host = '127.0.0.1:5000'
    conn = grpc.insecure_channel(host)  # 连接通道。协议写法
    client = pb2_grpc.DemoTestStub(channel=conn)  # 客户端实例。 名称为：proto里的类名+Stub
    response = client.HDemoReq(pb2.DemoReq(  # 这里正好是rpc后面的 请求实例(请求体)
        name='dewei',
        age=33
    ))
    print(response.result)  # 打印结果。 调试或日志查看的，非必须。


if __name__ == '__main__':
    run()

```

### 2.4 运行

运行很简单，在client.py和service.py文件路径，打开终端。
1.运行service.py脚本。将服务启动。
2.再开一个终端，运行client.py。 就能立即完成一次请求了。


## 3.初步总结：
### 3.1 优点
    1.搭建方便
    2.代码量不大
    3.语法简单
### 3.2 缺点
    1.客户端运行之后，参数不能随意变。
    2.要测试的单个模块，需要单独起服务和客户端，不能一并起。一个目录下，只能放一个。
    3.如何与当前工作业务结合？

## 4.扩展
### 4.1 proto文件内。参数类型说明：
```text
string  字符串类型，要求是utf-8、7-bit或ascii编码的字符串。
bytes  比特类型
bool  布尔值
int32  32位整型
int64  64位整型
float  浮点类型
repated  数组，格式：repeated string data = 1;  // 全是字符串类型的参数 data
map  Python里的字典。但是键值对类型被写死。格式：map<string, string> data = 1; // 键和值都是字符串类型的字典。

```
```text
syntax = 'proto3';  // 指明proto的版本，这里是=，也要写在proto文件最开始。
// 特殊字符，关键字说明
package  //包名。 如：package Test; 

service  // 定义服务。 如：service Demo {}  
rpc  // 定义服务中的方法。 rpc DemoFun(...)
stream  // 定义方法的传输模式为：流传输。 rpc DemoFun(stream ...)
message  // 定义消息体。 如：message User{}
extend  // 扩展消息体。 定义消息体不够时，或者后续追加，使用这个关键字。 如：extend User{}
import // 导入一些插件，在proto里是字符的方式，如：import 'any'
```
```text
生成的文件说明：
_pb2_grpc.py文件介绍：
    · 用来存储没一个服务的server与客户端以及注册server的工具。
    · 客户端名为：service_name + Stub
    · 服务端名为：service_name + Servicer
    · 注册服务为：add_服务端名_to_server
    
```