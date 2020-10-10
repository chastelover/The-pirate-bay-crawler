### 运行环境

**python3.5, chrome.exe, Mongo**



### 需要的包

**selenium:**`pip install selenium`

**multiprocessing:**`pip install multiprocessing`

**pymongo：**`python -m pip install pymongo`



### 使用方法

##### 打开config.py设置固定参数

|   参数名   |                           可设置值                           |
| :--------: | :----------------------------------------------------------: |
| MONGO_URL  |                 自行设置主机名（localhost）                  |
|  MONGO_DB  |               自行设置数据库名（magnetresult）               |
|    MODE    |           模式，可选*‘**search**’*  *‘**recent**’*           |
|  CONTENT   |              要搜索的内容，仅在search模式下设置              |
|   FORMAT   | 搜索的模式，可选**all,audio,video,apps,games,other**，仅在***search***模式下设置 |
| ISEXPLICIT |           是否显式进行搜索，可选***True、False***            |
|    PATH    |             chrome.exe的路径，仅在隐式搜索会使用             |



##### 运行TPB.py即可在数据库中查看结果

可以在命令行中使用`python TPB.py`或使用编译器运行执行采集，结果存入mongo中。



#### 关于作者

---



```python
Author = {
    name : "刘杨昊",
    email: "liuyanghao19s@ict.ac.cn"
}
```

