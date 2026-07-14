from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from botpy.http import Route
import random

@register("menu", "星星旁の旷野 Alin", "AL_1Sの功能菜单", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        self.beta_config = config.get("beta_config", False)
        super().__init__(context)

    @filter.command("get_origin_message")
    async def get_origin_message(self, event: AstrMessageEvent, message_id: str):
        """[测试]获取 menu 原始消息内容"""
        if not self.beta_config:
            return

        message_str = event.message_str
        if not "menu" in message_str:
            return

        message = await self.get_kv_data(f"{message_id}originmessage", None)
        if message is None:
            yield event.plain_result(f"未找到原始消息内容（ID: {message_id}）。")
            return

        chain = event.plain_result(f"原始消息内容（ID: {message_id}）：\n\n{message}")
        # 再手动关掉 markdown
        chain.use_markdown_ = False
        yield chain

    # 处理菜单指令
    # @param event AstrMessageEvent 消息事件对象
    # @return MessageEventResult 消息事件处理结果
    @filter.command("menu",alias={'菜单', '功能菜单'})
    async def helloworld(self, event: AstrMessageEvent):
        """获取AL_1S的功能菜单"""
        try:

            # 获取 openid，用于发送消息，并在消息中显示测试ID -> openid
            if event.is_private_chat():
                openid = event.message_obj.raw_message.author.user_openid # 如果是私聊消息，则使用用户的 user_openid
            else:
                openid = event.message_obj.raw_message.group_openid # 如果是群聊消息，则使用群组的 group_openid

            # 获取随机图片 -> imgUrl
            randImgNum = random.randint(1, 54)
            imgUrl = f"https://als.cn-nb1.rains3.com/menuGraph/{randImgNum}.png"


            # 组装 Markdown 消息 -> message
            message = f"""[ ](mqqapi://markdown/node?nodeType=replace&nodeID=quoteArea&state=start&text=&index=&itemsPerRow=&itemsNum=)
    [ ](mqqapi://markdown/node?nodeType=quoteArea&nodeID=quoteArea&state=start&text=AL_1S由雨云提供云计算服务)
    ## ✨邦邦卡邦✨
    ***这里是AL_1S的功能菜单~***
    [![img #480px #270px]({imgUrl})](https://www.rainyun.com/MTAzNDk2Nw==_?s=headImg)
    👉**新功能**👈
    <qqbot-cmd-input text="/群友老婆" show="🧑‍❤️‍👩随机抽取群友老婆"/>
    <qqbot-cmd-input text="/今天吃什么" show="🍕今天吃什么"/>
    | <qqbot-cmd-input text="/心奈唱歌" show="🎶心奈唱歌"/> | <qqbot-cmd-input text="/今日运势" show=" 🔮今日运势"/> |
    | --- | --- |
    | <qqbot-cmd-input text="/抽漫画" show="🌈随机漫画"/> | <qqbot-cmd-input text="/攻略 [填写你需要查询的学生名]" show="🔍角色攻略"/> |
    | <qqbot-cmd-input text="/好感" show="❣️好感计算"/> | <qqbot-cmd-input text="/抽卡" show="📒抽卡模拟"/> |
    | <qqbot-cmd-input text="/国际服千里眼" show="👀国际千里"/> | <qqbot-cmd-input text="/国服千里眼" show="👀国服千里"/> |
    | <qqbot-cmd-input text="/天气" show="☀天气查询"/> | <qqbot-cmd-input text="/ba转生" show="✨BA转生"/> |"""
            # 如果开启了beta测试模式，则在菜单尾部添加测试模式提醒和举报/反馈/版本说明按钮及测试ID。
            if self.beta_config:
                msg_id = await self.get_kv_data("now msg_id", 0) + 1
                await self.put_kv_data("now msg_id", msg_id)
                message = message + f"""***
    > 您当前正在使用测试版本的AL_1S机器人
    > 如果您遇到了问题，请点击<qqbot-cmd-input text="/反馈 menu.{msg_id} [在这里填写你想要反馈的内容]" show="反馈" reference="true" />
    > 如果您看到了不良信息，请点击<qqbot-cmd-input text="/举报 menu.{msg_id} [在这里填写你想要举报的原因]" show="举报" reference="true" />
    > 感谢您的支持~
    > _测试ID：{openid}_
    """
                await self.put_kv_data(f"menu.{msg_id}originmessage", message)
            
            # 构造消息 payload，用于发送带按钮的 Markdown 消息 -> payload
            payload = {
                "msg_type": 2,
                "msg_id": event.message_obj.message_id,
                "markdown": {
                    "content": message
                },
                "keyboard": {
                    "content": {
                        # 🌅早安 🌙晚安
                        # ✨添加到群聊 📆BA Only展
                        # 📝使用文档
                        # ⚡给爱丽丝充电
                        "rows": [
                            {
                                "buttons": [
                                    {
                                        # 功能按钮：🌅早安 -> /早安
                                        # 使用权限：所有人
                                        "render_data": {"label": "🌅早安", "style": 1},
                                        "action": {
                                            "type": 2,
                                            "permission": {"type": 2},
                                            "data": "/早安"
                                        }
                                    },
                                    {
                                        # 功能按钮：🌙晚安 -> /晚安
                                        # 使用权限：所有人
                                        "render_data": {"label": "🌙晚安", "style": 1},
                                        "action": {
                                            "type": 2,
                                            "permission": {"type": 2},
                                            "data": "/晚安"
                                        }
                                    }
                                ]
                            },
                            {
                                "buttons": [
                                    {
                                        # 跳转按钮：✨添加到群聊 -> https://bot.q.qq.com/s/6lvs7fce2?id=102062652
                                        # 使用权限：所有人
                                        "render_data": {"label": "✨添加到群聊", "style": 1},
                                        "action": {
                                            "type": 0,
                                            "permission": {"type": 2},
                                            "data": "https://bot.q.qq.com/s/6lvs7fce2?id=102062652"
                                        }
                                    },
                                    {
                                        # 跳转按钮：📆BA Only展 -> https://docs.qq.com/doc/DY0pkVExJdXpiZ1FI
                                        # 使用权限：所有人
                                        "render_data": {"label": "📆BA Only展", "style": 1},
                                        "action": {
                                            "type": 0,
                                            "permission": {"type": 2},
                                            "data": "https://docs.qq.com/doc/DY0pkVExJdXpiZ1FI"
                                        }
                                    }
                                ]
                            },
                            {
                                "buttons": [
                                    {
                                        # 跳转按钮：📝使用文档 -> https://docs.qq.com/doc/DY2x2SEtBVUlodHlF
                                        # 使用权限：所有人
                                        "render_data": {"label": "📝使用文档", "style": 1},
                                        "action": {
                                            "type": 0,
                                            "permission": {"type": 2},
                                            "data": "https://docs.qq.com/doc/DY2x2SEtBVUlodHlF"
                                        }
                                    }
                                ]
                            },
                            {
                                "buttons": [
                                    {
                                        # 跳转按钮：⚡给爱丽丝充电 -> https://afdian.com/a/alin-sky
                                        # 使用权限：所有人
                                        "render_data": {"label": "⚡给爱丽丝充电", "style": 1},
                                        "action": {
                                            "type": 0,
                                            "permission": {"type": 2},
                                            "data": "https://afdian.com/a/alin-sky"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }


            # 直接调用QQ官方API发送，不使用 Astrbot 封装的消息发送函数
            # 这样可以确保消息中包含按钮和 Markdown 格式
            if event.is_private_chat():
                # 私聊 - 用 api._http.request 发送 POST 请求
                route = Route("POST", f"/v2/users/{openid}/messages")
                await event.bot.api._http.request(
                    route, 
                    json={
                        **payload
                    }
                )
            else:
                # 群聊 - 用 api.post_group_message 发送 POST 请求
                await event.bot.api.post_group_message(
                    group_openid=openid,
                    **payload
                )
        except Exception as e:
            logger.error(f"菜单指令处理异常：{e}")
            yield event.plain_result(f"爱丽丝出现了错误，请稍后再试。\n> 错误已自动反馈！")
