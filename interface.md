

[TOC]

# 一、用户类


## （1）用户注册

接口 URL：```/api/user/register```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|u_name|是|string|用户名|
|u_pwd|是|string|登录密码|
|u_type|是|int|用户类型，系统管理员(0) / 普通用户(1)|
|r_name|是|string|用户姓名|
|c_type|是|int|证件类型（中华人民共和国居民身份证，台湾居民往来大陆通行证，港澳居民来往内地通行证，军人证件，护照，香港身份证，澳门身份证）|
|c_num|是|string|证件号码|
|p_num|否|string|电话号码（11位）|
|u_level|是|int|用户级别，VIP(0) / 一般(1)|
|u_idct|否|string|用户简介|
|r_city|是|string|注册城市（要和证件匹配）|
|r_cmty|是|string|注册社区|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|boolean|成功为``True``，失败为``False``|
|u_id|string|注册用户标识|
|remark|string|备注，例如：注册失败原因|

## （2）用户登录

接口 URL：```/api/user/login```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| u_name   | 是   | string | 用户名 |
| u_pwd    | 是   | string | 密码   |

### 返回JSON

| 属性   | 类型    | 说明                                  |
| ------ | ------- | ------------------------------------- |
| result | boolean | 成功为``True``，失败为``False``       |
| u_id   | string  | 用户标识                              |
| u_type | int     | 用户类型，系统管理员(0) / 普通用户(1) |

## （3）查询用户个人信息

接口 URL：```/api/user/info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| u_id     | 是   | string | 用户标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_obj | json    | json对象 |

###  JSON数组格式

| 属性    | 类型      | 说明                                                         |
| ------- | --------- | ------------------------------------------------------------ |
| u_name  | string    | 用户名                                                       |
| u_type  | int       | 用户类型，系统管理员(0) / 普通用户(1)                        |
| r_name  | string    | 用户姓名                                                     |
| c_type  | int       | 证件类型,中华人民共和国居民身份证0，台湾居民往来大陆通行证1，港澳居民来往内地通行证2，军人证件3，护照4，香港身份证5，澳门身份证6 |
| c_num   | string    | 证件号码                                                     |
| p_num   | string    | 手机号码                                                     |
| u_level | string    | 用户级别                                                     |
| u_idct  | string    | 用户简介                                                     |
| r_city  | string    | 注册城市                                                     |
| r_cmty  | string    | 注册社区                                                     |
| r_time  | timestamp | 注册时间                                                     |
| m_time  | timestamp | 修改时间                                                     |

## （4）用户修改基本信息

接口 URL：```/api/user/modify```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|u_id|是|string|用户标识|
|u_pwd|否|string|密码|
|p_num|否|string|联系电话（11位）|
|u_idct|否|string|用户简介|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|Boolean|成功为``True``，失败为``False``|

# 二、请求类

## （1）用户发布请求信息

接口 URL：```/api/user/request/release```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|req_cmty|是|string|发布社区|
|req_uid|是|string|发布用户标识|
|req_type|是|string|请求类型（小时工 、 搬重物 、 上下班搭车 、 社区服务自愿者）|
|req_topic|是|string|请求主题|
|req_idct|是|string|请求描述|
|req_nop|是|int|请求人数|
|end_time|是|string|请求结束日期（yyyy-mm-dd）|
|req_photo|否|string|请求介绍照片|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|boolean|发布结果，成功为``True``，失败为``False``|
|req_id|string|请求标识|
|remark|string|备注，发布失败原因|

## （2）用户查询自己发布的所有请求信息

接口 URL：```/api/user/request/info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| req_uid  | 是   | string | 用户标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_arr | json    | json数组 |

### JSON数组格式

|属性|类型|说明|
|---|---|---|
|result|boolean|查询结果|
|req_cmty|string|发布社区|
|req_id|string|请求标识|
|req_uid|string|发布用户标识|
|req_type|string|请求类型（小时工 、 搬重物 、 上下班搭车 、 社区服务自愿者）|
|req_topic|string|请求主题|
|req_idct|string|请求描述|
|req_nop|int|请求人数|
|end_time|timestamp|请求结束日期|
|req_photo|string|请求介绍照片(可空)|
|req_time|timestamp|创建时间|
|m_time|string|修改时间|
|req_status|int|状态|

## （3）用户删除（已发布还没有响应者）的请求信息

接口 URL：```/api/user/request/delete```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| req_id   | 是   | string | 请求标识 |

### 返回JSON

| 属性   | 类型    | 说明                                      |
| ------ | ------- | ----------------------------------------- |
| result | boolean | 删除结果，成功为``True``，失败为``False`` |

## （4）用户修改（已发布还没响应者）的请求信息

接口 URL：```/api/user/request/modify```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

| 参数名称  | 必选 | 类型   | 说明                                                         |
| --------- | ---- | ------ | ------------------------------------------------------------ |
| req_id    | 是   | string | 请求标识                                                     |
| req_type  | 否   | string | 请求类型（小时工 、 搬重物 、 上下班搭车 、 社区服务自愿者） |
| req_topic | 否   | string | 请求主题                                                     |
| req_idct  | 否   | string | 请求描述                                                     |
| req_nop   | 否   | int    | 请求人数                                                     |
| end_time  | 否   | string | 请求结束日期（yyyy-mm-dd）                                   |
| req_photo | 否   | string | 请求介绍照片                                                 |

### 返回JSON

| 属性   | 类型    | 说明                                      |
| ------ | ------- | ----------------------------------------- |
| result | boolean | 修改结果，成功为``True``，失败为``False`` |
| remark | string  | 备注，例如失败信息                        |

## （5）用户查看所属社区所有帮忙请求信息

接口 URL：```/api/user/response/request_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称  | 必选 | 类型   | 说明         |
| --------- | ---- | ------ | ------------ |
| community | 是   | string | 用户所属社区 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_arr | json    | json数组 |

###  JSON数组格式

| 属性       | 类型      | 说明                                                         |
| ---------- | --------- | ------------------------------------------------------------ |
| req_id     | string    | 请求标识                                                     |
| req_uid    | string    | 发布用户标识                                                 |
| req_type   | string    | 请求类型（小时工 、 搬重物 、 上下班搭车 、 社区服务自愿者） |
| req_topic  | string    | 请求主题                                                     |
| req_idct   | string    | 请求描述                                                     |
| req_nop    | int       | 请求人数                                                     |
| end_time   | timestamp | 请求结束日期                                                 |
| req_photo  | string    | 请求介绍照片                                                 |
| req_time   | timestamp | 请求创建时间                                                 |
| req_status | string    | 状态                                                         |

## （6）用户查看某一帮忙请求具体信息

接口 URL：```/api/user/request/spec_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| req_id   | 是   | string | 请求标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_obj | json    | json对象 |

### JSON对象格式

| 属性       | 类型      | 说明                                                         |
| ---------- | --------- | ------------------------------------------------------------ |
| req_uid    | string    | 发布用户标识                                                 |
| req_type   | string    | 请求类型（小时工 、 搬重物 、 上下班搭车 、 社区服务自愿者） |
| req_topic  | string    | 请求主题                                                     |
| req_idct   | string    | 请求描述                                                     |
| req_nop    | int       | 请求人数                                                     |
| end_time   | timestamp | 请求结束日期                                                 |
| req_photo  | string    | 请求介绍照片                                                 |
| req_time   | timestamp | 请求创建时间                                                 |
| req_status | string    | 状态                                                         |

## 

# 三、帮忙响应类

## （1）用户查看某一请求信息的所有帮忙信息

接口 URL：```/api/user/request/response_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| req_id   | 是   | string | 请求标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_arr | json    | json数组 |

###  JSON数组格式

|属性|类型|说明|
|---|---|---|
|rsp_id|string|响应标识|
|req_id|string|请求标识|
|rsp_uid|string|响应用户标识|
|rsp_idct|string|响应描述|
|rsp_time|timestamp|响应时间|
|rsp_status|int|状态（0：待接受 / 1：同意 / 2：拒绝 / 3：取消）|

## （2）用户处理响应信息

接口 URL：```/api/user/request/opt_response```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|req_id|是|string|请求标识|
|req_uid|是|string|请求用户标识|
|rsp_id|是|string|响应标识|
|rsp_uid|是|string|响应用户标识|
|option|是|boolean|是否接受响应，接受为``True``，拒绝为``False``|

### 返回JSON

| 属性   | 类型    | 说明                                                       |
| ------ | ------- | ---------------------------------------------------------- |
| result | boolean | 处理结果，成功为``True``，失败为``False``                  |
| remark | string  | 备注，例如错误信息：人数已达上限！/ 请求ID和响应ID不对应！ |

## （3）用户提交响应信息

接口 URL：```/api/user/response/release```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|req_id|是|string|请求标识|
|rsp_uid|是|string|响应用户标识|
|rsp_idct|是|string|响应描述|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|boolean|发布响应信息结果，成功为``True``，失败为``False``|
|remark|string|备注，例如失败理由|
|rsp_id|string|响应标识|

## （4）用户查看自己发布的响应信息

接口 URL：```/api/user/response/response_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明         |
| -------- | ---- | ------ | ------------ |
| rsp_uid  | 是   | string | 响应用户标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_arr | json    | json数组 |

###  JSON数组格式

|属性|类型|说明|
|---|---|---|
|rsp_id|string|响应标识|
|req_id|string|请求标识|
|rsp_uid|string|响应用户标识|
|rsp_idct|string|响应描述|
|rsp_time|timestamp|响应创建时间|
|rsp_status|int|状态|
|req_cmty|string|请求发布社区|
|req_uid|string|发布用户标识|
|req_type|string|请求类型（小时工 、 搬重物 、 上下班搭车 、 社区服务自愿者）|
|req_topic|string|请求主题|
|req_idct|string|请求描述|
|req_nop|int|请求人数|
|end_time|timestamp|请求结束日期|
|req_time|timestamp|请求发布时间|
|req_status|int|请求状态信息|

## （5）用户修改还未被接受的响应信息

接口 URL：```/api/user/response/modify```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|rsp_id|是|string|响应标识|
|rsp_idct| 是   |string|响应描述|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|boolean|修改响应信息结果，成功为``True``，失败为``False``|

## （6）用户删除还未被接受的响应信息

接口 URL：```/api/user/response/delete```

请求方法：```POST```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|rsp_id|是|string|响应标识|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|boolean|删除响应信息结果，成功为``True``，失败为``False``|

## （7）用户查询自己所有已经被接受的请求响应信息

接口 URL：```/api/user/response/accepted```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明         |
| -------- | ---- | ------ | ------------ |
| rsp_uid  | 是   | string | 响应用户标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_arr | json    | json数组 |

###  JSON数组格式

|属性|类型|说明|
|---|---|---|
|rsp_id|string|响应标识|
|req_id|string|请求标识|
|rsp_uid|string|响应用户标识|
|rsp_idct|string|响应描述|
|rsp_time|timestamp|响应创建时间|



# 四、管理员

## （1）返回所有用户的信息

接口 URL：```/api/admin/all_users```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型 | 说明 |
| -------- | ---- | ---- | ---- |
|          |      |      |      |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_arr | json    | json数组 |

###  JSON数组格式

| 属性    | 类型   | 说明                                                         |
| ------- | ------ | ------------------------------------------------------------ |
| u_name  | string | 用户名                                                       |
| u_type  | int    | 用户类型，系统管理员(0) / 普通用户(1)                        |
| r_name  | string | 用户姓名                                                     |
| c_type  | int    | 证件类型,中华人民共和国居民身份证0，台湾居民往来大陆通行证1，港澳居民来往内地通行证2，军人证件3，护照4，香港身份证5，澳门身份证6 |
| c_num   | string | 证件号码                                                     |
| p_num   | string | 手机号码                                                     |
| u_level | string | 用户级别                                                     |
| u_idct  | string | 用户简介                                                     |
| r_city  | string | 注册城市                                                     |
| r_cmty  | string | 注册社区                                                     |

## 

## （2）根据请求标识查询发起请求用户的基本信息

接口 URL：```/api/admin/request/user_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| req_id   | 是   | string | 请求标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_obj | json    | json对象 |

###  JSON数组格式

| 属性    | 类型   | 说明                                                         |
| ------- | ------ | ------------------------------------------------------------ |
| u_name  | string | 用户名                                                       |
| u_type  | int    | 用户类型，系统管理员(0) / 普通用户(1)                        |
| r_name  | string | 用户姓名                                                     |
| c_type  | int    | 证件类型,中华人民共和国居民身份证0，台湾居民往来大陆通行证1，港澳居民来往内地通行证2，军人证件3，护照4，香港身份证5，澳门身份证6 |
| c_num   | string | 证件号码                                                     |
| p_num   | string | 手机号码                                                     |
| u_level | string | 用户级别                                                     |
| u_idct  | string | 用户简介                                                     |
| r_city  | string | 注册城市                                                     |
| r_cmty  | string | 注册社区                                                     |

## （3）根据响应标识查询帮忙用户的基本信息

接口 URL：```/api/admin/response/user_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| rsp_id   | 是   | string | 响应标识 |

### 返回JSON

| 属性     | 类型    | 说明     |
| -------- | ------- | -------- |
| result   | boolean | 查询结果 |
| info_obj | json    | json对象 |

###  JSON数组格式

| 属性    | 类型   | 说明                                                         |
| ------- | ------ | ------------------------------------------------------------ |
| u_name  | string | 用户名                                                       |
| u_type  | int    | 用户类型，系统管理员(0) / 普通用户(1)                        |
| r_name  | string | 用户姓名                                                     |
| c_type  | int    | 证件类型,中华人民共和国居民身份证0，台湾居民往来大陆通行证1，港澳居民来往内地通行证2，军人证件3，护照4，香港身份证5，澳门身份证6 |
| c_num   | string | 证件号码                                                     |
| p_num   | string | 手机号码                                                     |
| u_level | string | 用户级别                                                     |
| u_idct  | string | 用户简介                                                     |
| r_city  | string | 注册城市                                                     |
| r_cmty  | string | 注册社区                                                     |

## （4）管理员查询一定条件的请求帮忙信息的状态*

接口 URL：```/api/admin/requset_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称   | 必选 | 类型      | 说明             |
| ---------- | ---- | --------- | ---------------- |
| req_cmty   | 否   | string    | 更多操作发布社区 |
| req_id     | 否   | string    | 请求标识         |
| req_uid    | 否   | string    | 发布用户标识     |
| req_type   | 否   | string    | 请求类型         |
| req_time   | 否   | timestamp | 创建时间         |
| req_status | 否   | int       | 状态             |

### 返回JSON

|属性|类型|说明|
|---|---|---|
|req_id|string|请求标识|
|req_status|int|状态|

## （5）管理员查询一定条件的接受请求信息*

接口 URL：```/api/admin/response_info```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称 | 必选 | 类型   | 说明         |
| -------- | ---- | ------ | ------------ |
| req_id   | 否   | string | 请求标识     |
| req_uid  | 否   | string | 发布用户标识 |
| rsp_uid  | 否   | string | 响应用户标识 |
| agc_time | 否   | string | 达成日期     |

### 返回JSON

|属性|类型|说明|
|---|---|---|
|req_id|string|接受请求的请求标识|
|req_uid|string|发布用户标识|
|rsp_uid|string|响应用户标识|
|agc_time|timestamp|达成日期|
|req_fee|int|发布者支付中介费|
|rsp_fee|int|响应者支付中介费|
|agc_fee|int|单笔请求中介费|

## （6）管理员查询已完成请求的中介费

接口 URL：```/api/admin/fee```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

| 参数名称     | 必选 | 类型      | 说明         |
| ------------ | ---- | --------- | ------------ |
| start_time   | 是   | timestamp | 开始时间     |
| end_time     | 是   | timestamp | 结束时间     |
| ~~req_id~~   | 否   | string    | 请求标识     |
| ~~req_uid~~  | 否   | string    | 发布用户标识 |
| ~~rsp_uid~~  | 否   | string    | 响应用户标识 |
| ~~agc_time~~ | 否   | timestamp | 达成日期     |

### 返回JSON

|属性|类型|说明|
|---|---|---|
|agency_fee|int|累计中介费用|



## （7）管理员查询已完成请求的中介费月份统计数据

接口 URL：```/api/admin/statistics```

请求方法：```GET```

编码方式：```raw(json)```

### 请求参数

|参数名称|必选|类型|说明|
|----|----|----|----|
|start_time|是|timestamp|起始时间|
|end_time|是|timestamp|终止时间|

### 返回JSON

|属性|类型|说明|
|---|---|---|
|result|boolean| 查询结果 |
|info_arr|JSON|JSON数组|

### JSON数组格式

| 属性      | 类型            | 说明             |
| --------- | --------------- | ---------------- |
| the_month | string(yyyy-mm) | 月份             |
| trx_num   | int             | 当月累计成交笔数 |
| agc_fee   | int             | 当月累计中介费   |

### 