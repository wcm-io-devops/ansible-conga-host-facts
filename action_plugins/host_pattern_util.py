#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleOptionsError

import re

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()


class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super(ActionModule, self).__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self._task_vars = None

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        self._task_vars = task_vars

        result = {}

        try:
            # Get conga_facts based config (whole or tenant config)
            pattern = self._get_arg_or_var('pattern', None, True)
            fact_name = self._get_arg_or_var('fact_name', None, True)

        except AnsibleOptionsError as err:
            return self._fail_result(result, err.message)

        pattern_parts = pattern.split(":")
        cleaned_parts = []
        for pattern_part in pattern_parts:
            cleaned_part = re.sub(".*conga_variants_" , "", pattern_part)
            display.vv("pattern_part: %s" % (pattern_part))
            display.vv("cleaned_part: %s" % (cleaned_part))
            cleaned_parts.append(cleaned_part)

        result = {
            "ansible_facts" : {
                fact_name : cleaned_parts
            }
        }

        return result

    @staticmethod
    def _fail_result(result, message):
        result['failed'] = True
        result['msg'] = message
        return result

    def _get_arg_or_var(self, name, default=None, is_required=True):
        ret = self._task.args.get(name, self._task_vars.get(name, default))
        ret = self._templar.template(ret)
        if is_required and not ret:
            raise AnsibleOptionsError("parameter %s is required" % name)
        else:
            return ret
