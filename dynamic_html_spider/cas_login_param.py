# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
"""
    cas-server 4.0.0login 所需参数
   @author xingguo
   @date 1/11/2019 9:58 PM 
   @since 1.0.0 
"""


class CasLoginParam():
    """

       @author xingguo
       @date 1/11/2019 9:59 PM
       @since 1.0.0
    """

    def __init__(self, user_name, password, execution, event_id, lt):
        # 用户名称
        self.user_name = user_name
        # 密码(md5加密)
        self.password = password
        # cas execution
        self.execution = execution
        # cas event_id
        self.event_id = event_id
        # cas lt
        self.lt = lt
