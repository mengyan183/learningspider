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

    def __init__(self, username, password, execution, _eventId, lt, submit, vcode):
        # 用户名称
        self.username = username
        # 密码(md5加密)
        self.password = password
        # cas execution
        self.execution = execution
        # cas event_id
        self._eventId = _eventId
        # cas lt
        self.lt = lt
        # cas submit
        self.submit = submit
        # vcode
        self.vcode = vcode
