# 关于env环境配置

主要有以下三个点：

- 飞书机器人的`APP_ID`和`APP_SECRET`
- Dify工作流的`DIFY_API_KEY`
- 飞书消息卡片

其中飞书机器人和Dify工作流的相关配置参数直接在对应应用中可以找到，这里我们详细讲解一下项目中最为灵活且最有特点的消息卡片的配置

### 飞书消息卡片配置解析（通用版本）
飞书消息卡片的配置是一个灵活的结构，允许用户通过一个JSON字符串定义任意数量的消息卡片模板。每个模板都有自己的 `template_id` 和 `template_variable`，用来定义模板和模板变量。

下面是对配置结构的详细解析：

**通用配置结构**
```bash
FEISHU_CARD_TEMPLATES='{
    "custom_card_name_1": {                  
        "template_id": "TemplateID_1",        
        "template_variable": {
            "variable_name_1": "value_1",
            "variable_name_2": "value_2"
        }         
    },
    "custom_card_name_2": {                    
        "template_id": "TemplateID_2",        
        "template_variable": {                
            "variable_name_3": "value_3", 
            "variable_name_4": "value_4",
            "variable_name_5": "value_5"
        }                 
    },
    // 可以添加更多的自定义卡片模板
}'
```
在这个通用结构中：

- `custom_card_name_X`: 这是自定义的消息卡片名称，用户可以根据需要配置任意数量的卡片模板，每个卡片模板都有一个唯一的名称。
- `template_id`: 每个卡片模板都有一个唯一的 `template_id`，用来指定飞书消息卡片的模板。
- `template_variable`: 每个卡片模板可以包含多个变量，这些变量在实际使用时可以用具体的值来替换。

这种灵活性允许开发者根据不同的场景动态生成消息内容，从而提高用户互动的效率和效果。

### 如何使用消息卡片
